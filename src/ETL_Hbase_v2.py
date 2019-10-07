# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 21:38:19 2019

@author: Ed, Vince
"""

from reviews import Parse, Review
from starbase import Connection


class Table:
   NAME      = "Review"
   
class ColFamily:
   USER      = "User"
   PROD      = "Product"
   
class Col:
   USER_NAME = "Name"
   HELPFUL   = "Helpful"
   SCORE     = "Score"
   TIME      = "Time"
   SUMMARY   = "Summary"
   TEXT      = "Text"
   
   
class HBase(Connection):
   """
      BRIEF  Just a wrapper for the hbase connection
   """
   
   def __init__(self):
      """
         BRIEF  Establish a connection
      """
      super(HBase, self).__init__("127.0.0.1", "8085")
      
   def CreateTable(self, table_name, *col_names):
      """
         BRIEF  Create the table
      """
      table = self.table(table_name)
      if (table.exists()):
         table.drop()
      table.create(*col_names)
      return table
      
      
def PopulateTable(reviews, table):
   """
      BRIEF  Copy all the date from the file to the table
   """
   batch = table.batch()
   for review in reviews:
      batch.insert(
         
         # unique row key (assuming user can't review same movie twice!)
         review[Review.USER_ID] + review[Review.MOVIE_ID],
         
         # Column families
         {
            { "{0}.{1}".format(ColFamily.USER, Col.USER_NAME) : review[Review.USER_NAME]},
            { "{0}.{1}".format(ColFamily.PROD, Col.HELPFUL  ) : review[Review.HELPFUL  ]},
            { "{0}.{1}".format(ColFamily.PROD, Col.SCORE    ) : review[Review.SCORE    ]},
            { "{0}.{1}".format(ColFamily.PROD, Col.TIME     ) : review[Review.TIME     ]},
            { "{0}.{1}".format(ColFamily.PROD, Col.SUMMARY  ) : review[Review.SUMMARY  ]},
            { "{0}.{1}".format(ColFamily.PROD, Col.TEXT     ) : review[Review.TEXT     ]}
         }
      )
   batch.commit(finalize = True)
   
   
if __name__ == '__main__':
   
   import os
   
   # Connect
   hb = HBase()
   
   # Force create
   table = hb.CreateTable(Table.NAME, ColFamily.USER, ColFamily.PROD)
   
   # Batch insert reviews
   path = os.path.join('..', 'test', 'movies.txt')
   Parse(path, 10**5, PopulateTable, table)
   
   