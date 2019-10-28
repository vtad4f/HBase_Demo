# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 21:38:19 2019

@author: Ed, Vince
"""

from mock_hbase import MockTable
from hbase import HBase, ColFamily, FullCol
from reviews import Parse, Review
from mock import patch
import os
import re
import sys


class Regex:
   WORD = re.compile(r'[A-Za-z0-9_-]+', re.MULTILINE)


@patch('hbase.HBase.ForceCreateTable', side_effect=[MockTable()])
@patch('starbase.Connection')
def MockTest(*args):
   """
      BRIEF  Test using a fake starbase
   """
   Test()
   
   
def Test():
   """
      BRIEF  Test using a smaller movies.txt (just the first 500 lines)
   """
   Main('test', 'test')
   
   
def Main(table_name, input_dir):
   """
      BRIEF  Main is a function so that we can use mock.patch
   """
   input_path = os.path.join('..', input_dir, 'movies.txt')
   
   # Populate the table by parsing the reviews input file
   table = HBase.ForceCreateTable(table_name, *ColFamily.ALL, host='maria_dev@127.0.0.1', port = "8080")
   first_review = Parse(input_path, 1000, HBase.PopulateTable, table)
   
   # Put multiple data for some specific entry which allows versioning.
   # Get one or more versions for that entry to see if it works.
   DuplicateQuery(table, first_review)
   
   # Aggregate queries for 'helpfulness' and 'score'
   AggregateQuery(table, FullCol.HELPFUL)
   AggregateQuery(table, FullCol.SCORE)
   
   # Query that involves sorting
   SortingQuery(table)
   
   # Queries that show analytics from 'summary' and 'text'
   AnalyticsQuery(table, FullCol.SUMMARY)
   AnalyticsQuery(table, FullCol.TEXT)
   
   
def DuplicateQuery(table, review):
   """
      BRIEF  Confirm that the review was added twice, each time with a new id
   """
   row_key = review[Review.USER_ID] + review[Review.MOVIE_ID]
   for row in table.fetch(row_key):
      print(row)
   print(' ')
   sys.stdout.flush()
   
   
def AggregateQuery(table, full_col_name):
   """
      BRIEF  Get the average value for the col for all rows & versions (just numerator if fraction)
   """
   total = 0
   count = 0.0
   for row in table.fetch_all_rows():
      total += int(float(row[full_col_name].split('/')[0]))
      count += 1.0
   print("(Aggregate) Average({0}) = {1}".format(full_col_name, total / count))
   print(' ')
   sys.stdout.flush()
   
   
def SortingQuery(table):
   """
      BRIEF  Sort all the rows retrieved
   """
   for row in sorted("{0:<5} {1:<10} {2}".format(row[FullCol.HELPFUL], row[FullCol.TIME], row[FullCol.USER_NAME]) for row in table.fetch_all_rows()):
      print(row)
   print(' ')
   sys.stdout.flush()
   
   
def AnalyticsQuery(table, full_col_name):
   """
      BRIEF  Get the average word count for all rows & versions
   """
   total = 0
   count = 0.0
   for row in table.fetch_all_rows():
      total += len(Regex.WORD.findall(row[full_col_name]))
      count += 1.0
   print("(Analytics) AverageWordCount({0}) = {1}".format(full_col_name, total / count))
   print(' ')
   sys.stdout.flush()
   
   
if __name__ == '__main__':
   """
      BRIEF  Main execution
   """
   MockTest()
   # Test() # Uncomment once the VM is fixed
   # Main('reviews', 'in') # uncomment once Test works # TODO - submit with screenshot
   
   
   