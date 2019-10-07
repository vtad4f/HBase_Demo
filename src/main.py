# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 21:38:19 2019

@author: Ed, Vince
"""

from reviews import Parse, Review
from starbase import Connection
from requests.exceptions import ConnectionError


class Table:
   NAME      = "Review"
   
class Family:
   USER      = "User"
   PROD      = "Product"
   
class Col:
   USER_NAME = "Name"
   HELPFUL   = "Helpful"
   SCORE     = "Score"
   TIME      = "Time"
   SUMMARY   = "Summary"
   TEXT      = "Text"
   
class FullCol:
   USER_NAME = "{0}.{1}".format(Family.USER, Col.USER_NAME)
   HELPFUL   = "{0}.{1}".format(Family.PROD, Col.HELPFUL  )
   SCORE     = "{0}.{1}".format(Family.PROD, Col.SCORE    )
   TIME      = "{0}.{1}".format(Family.PROD, Col.TIME     )
   SUMMARY   = "{0}.{1}".format(Family.PROD, Col.SUMMARY  )
   TEXT      = "{0}.{1}".format(Family.PROD, Col.TEXT     )
   
class HBase(Connection):
   """
      BRIEF  Just a wrapper for the hbase connection
   """
   
   def __init__(self):
      """
         BRIEF  Establish a connection
      """
      super(HBase, self).__init__(port = "8085")
      
   def CreateTable(self, table_name, *col_names):
      """
         BRIEF  Create the table
      """
      table = self.table(table_name)
      if (table.exists()):
         table.drop()
      table.create(*col_names)
      return table
      
   @staticmethod
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
      global i
      print(i)
      i += 1
      
      for review in reviews:
         
         again = True
         while again:
            try:
               table.insert(review[Review.USER_ID] + review[Review.MOVIE_ID], {
                  FullCol.USER_NAME : review[Review.USER_NAME],
                  FullCol.HELPFUL   : review[Review.HELPFUL  ],
                  FullCol.SCORE     : review[Review.SCORE    ],
                  FullCol.TIME      : review[Review.TIME     ],
                  FullCol.SUMMARY   : review[Review.SUMMARY  ],
                  FullCol.TEXT      : review[Review.TEXT     ]
               })
               again = False
            except ConnectionError:
               pass
               
if __name__ == '__main__':
   
   import os
   
   # Connect
   hb = HBase()
   
   # Force create
   table = hb.CreateTable(Table.NAME, Family.USER, Family.PROD)
   
   i=0
   
   # Batch insert reviews
   path = os.path.join('..', 'in', 'movies.txt')
   Parse(path, 1000, HBase.PopulateTable, table)
   
   