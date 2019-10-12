"""
   @author: Vince
"""

from reviews import Review
from starbase import Connection
from requests.exceptions import ConnectionError


class ColFamily:
   USER      = "User"
   PROD      = "Product"
   ALL       = [USER, PROD]
   
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
   
   
class HBase():
   """
      BRIEF  Just a static class for HBase table interaction
   """
   version = 1
   
   @staticmethod
   def ForceCreateTable(table_name, *col_names, **kwargs):
      """
         BRIEF  Create the table
      """
      c = Connection(**kwargs)
      table = c.table(table_name)
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
      assert(len(reviews))
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
      HBase._InsertReview(reviews[0], table) # Deliberately inserted twice!
      HBase.version += 1
      
      for review in reviews:
         HBase._InsertReview(review, table)
         HBase.version += 1
         
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
      
      