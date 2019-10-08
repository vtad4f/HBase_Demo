# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 21:38:19 2019

@author: Ed, Vince
"""

from reviews import Parse, Review
from starbase import Connection
from requests.exceptions import ConnectionError
import sys


class Dir:
   INPUT     = "in"
   TEST      = "test"
   
class Table:
   NAME      = "Review"
   TEST      = "Test"
   
class ColFamily:
   USER      = "User"
   PROD      = "Product"
   ALL       - [USER, PROD]
   
class Col:
   USER_NAME = "Name"
   HELPFUL   = "Helpful"
   SCORE     = "Score"
   TIME      = "Time"
   SUMMARY   = "Summary"
   TEXT      = "Text"
   ALL       = [USER_NAME, HELPFUL, SCORE, TIME, SUMMARY, TEXT]
   
class FullCol:
   USER_NAME = "{0}.{1}".format(ColFamily.USER, Col.USER_NAME)
   HELPFUL   = "{0}.{1}".format(ColFamily.PROD, Col.HELPFUL  )
   SCORE     = "{0}.{1}".format(ColFamily.PROD, Col.SCORE    )
   TIME      = "{0}.{1}".format(ColFamily.PROD, Col.TIME     )
   SUMMARY   = "{0}.{1}".format(ColFamily.PROD, Col.SUMMARY  )
   TEXT      = "{0}.{1}".format(ColFamily.PROD, Col.TEXT     )
   ALL       = [USER_NAME, HELPFUL, SCORE, TIME, SUMMARY, TEXT]
   
   
def KeepTrying(func):
   """
      BRIEF  This decorator calls the fcn until there is no ConnectionError
   """
   def Wrapper(*args, **kwargs):
      while True:
         try:
            return func(*args, **kwargs)
         except ConnectionError:
            pass
   return Wrapper
   
   
class HBase(Connection):
   """
      BRIEF  Just a wrapper for the hbase connection
   """
   version = 1
   
   def __init__(self):
      """
         BRIEF  Establish a connection
      """
      super(HBase, self).__init__(port = "8085")
      
   def ForceCreateTable(self, table_name, *col_names):
      """
         BRIEF  Create the table
      """
      table = self.table(table_name)
      if (table.exists()):
         table.drop()
      table.create(*col_names)
      assert(table.exists)
      return table
      
   @staticmethod
   @KeepTrying
   def PopulateTable(reviews, table):
      """
         BRIEF  Do a batch insert if possible
      """
      batch = table.batch()
      if batch:
         HBase._InsertReviews(reviews, batch)
         batch.commit(finalize = True)
      else:
         HBase._InsertReviews(reviews, table)
         
   @staticmethod
   def _InsertReviews(reviews, table):
      """
         BRIEF  Add all the reviews to the table
      """
      for review in reviews:
         HBase._InsertReview(review, table)
         HBase.version += 1 # Same user can review a movie twice!
         
   @staticmethod
   @KeepTrying
   def _InsertReview(review, table):
      """
         BRIEF  Add a single review to the table
      """
      table.insert(
         review[Review.USER_ID] + review[Review.MOVIE_ID],
         {
            FullCol.USER_NAME : review[Review.USER_NAME],
            FullCol.HELPFUL   : review[Review.HELPFUL  ],
            FullCol.SCORE     : review[Review.SCORE    ],
            FullCol.TIME      : review[Review.TIME     ],
            FullCol.SUMMARY   : review[Review.SUMMARY  ],
            FullCol.TEXT      : review[Review.TEXT     ]
         },
         HBase.version # Use same version per row for both column families
      )
      
      
if __name__ == '__main__':
   
   import os
   
   # Connect
   hb = HBase()
   
   # Force create table
   table = hb.ForceCreateTable(Table.TEST, *ColFamily.ALL)
   
   # Insert reviews into table
   Parse(os.path.join('..', Dir.TEST, 'movies.txt'), 1000, HBase.PopulateTable, table)
   
   # Check results
   row = table.fetch('A141HP4LYPWMSRB003AI2VGA')
   print(row)
   sys.stdout.flush()
   
   for row in table.fetch_all_rows():
      print(row)
      sys.stdout.flush()
      break
      
   # TODO - insert duplicate (with a different version)
   # TODO - query to be sure both are present in the table
   
   # TODO - aggregate query for 'helpfulness'
   # TODO - aggregate query for 'score'
   
   # TODO - query that involves sorting
   # TODO - two queries that show analytics from 'review text' and 'review summary'
   
   # TODO - submit with screenshot
   
   