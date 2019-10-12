# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 21:38:19 2019

@author: Ed, Vince
"""

from reviews import Parse
from hbase import HBase, ColFamily
from mock import patch, MagicMock
import os
import sys


def Main(table_name, input_dir):
   """
      BRIEF  Main is a separate function so that we can use mock.patch
   """
   table = HBase.ForceCreateTable(table_name, *ColFamily.ALL, port = "8085")
   Parse(os.path.join('..', input_dir, 'movies.txt'), 1000, HBase.PopulateTable, table)
   
   # Check results
   row = table.fetch('A141HP4LYPWMSRB003AI2VGA') # first entry
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

   
   