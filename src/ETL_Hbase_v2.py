# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 21:38:19 2019

@author: Ed, Vince
"""

from starbase import Connection


class HBase(Connection):
   """
      BRIEF  Just a wrapper for the hbase connection
   """
   
   def __init__(self):
      """
         BRIEF  Establish a connection
      """
      super().__init__("127.0.0.1", "8000")
      
      
   def CreateTable(self, table_name, *col_names):
      """
         BRIEF  Create the table
      """
      table = self.table(table_name)
      if (table.exists()):
         table.drop()
      table.create(*col_names)
      return table
      
      
   def PopulateTable(self, path, table):
      """
         BRIEF  Copy all the date from the file to the table
      """
      batch = table.batch()
      with open(path, 'r') as f:
         for line in f:
            userID, movieID, rating, _ = line.split() # TODO - Not so hard-coded
            batch.insert(userID, {'rating': {movieID: rating}})
      batch.commit(finalize = True)
      
      
if __name__ == '__main__':
      
   hb = HBase()
   
   table = hb.CreateTable('ratings', 'rating')
   assert(table.exists())
   
   hb.PopulateTable(os.path.join('in', 'TODO'), table)
   
   print(table.fetch('1'))
   print(table.fetch('33'))
   
   