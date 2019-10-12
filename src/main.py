# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 21:38:19 2019

@author: Ed, Vince
"""

from hbase import HBase, ColFamily
from reviews import Parse, Review
from mock import patch, MagicMock
import os
import sys


def Main(table_name, input_dir):
   """
      BRIEF  Main is a separate function so that we can use mock.patch
   """
   input_path = os.path.join('..', input_dir, 'movies.txt')
   
   # Populate the table by parsing the reviews input file
   table = HBase.ForceCreateTable(table_name, *ColFamily.ALL, port = "8085")
   first_review = Parse(input_path, 1000, HBase.PopulateTable, table)
   
   # Check results
   row = table.fetch('A141HP4LYPWMSRB003AI2VGA') # first entry
   print(row)
   sys.stdout.flush()
   
   for row in table.fetch_all_rows():
      print(row)
      sys.stdout.flush()
      break
      
   # TODO - query to be sure both are present in the table
   
   # TODO - aggregate query for 'helpfulness'
   # TODO - aggregate query for 'score'
   
   # TODO - query that involves sorting
   # TODO - two queries that show analytics from 'review text' and 'review summary'
   
   # TODO - submit with screenshot
   
def InsertDuplicate(table):
   """
      BRIEF  
   """
   
   
def AggregateQuery(col):
   """
      BRIEF  
   """
   
   
def Test():
   """
      BRIEF  Test using a smaller movies.txt (just the first 500 lines)
   """
   Main('test', 'test')
   
   
@patch('hbase.HBase.ForceCreateTable')
@patch('starbase.Connection')
def MockTest(*args):
   """
      BRIEF  Test using a fake starbase
   """
   Test()
   
   
if __name__ == '__main__':
   """
      BRIEF  Main execution
   """
   MockTest()
   # Test() # Uncomment once the VM is fixed
   # Main('reviews', 'in') # uncomment once Test works

   
   