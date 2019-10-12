"""
   @author: Vince
"""

from collections import OrderedDict


class MockTable(OrderedDict):
   """
      BRIEF  A class that pretends to be an HBase table
   """
   
   def __init__(self):
      """
         BRIEF  Just construct an empty set
      """
      super(MockTable, self).__init__()
      
   def batch(self):
      """
         BRIEF  Examples do an if check on this return
      """
      return None
      
   def insert(self, row_id, col_dict, version):
      """
         BRIEF  Add a row
      """
      if not row_id in self:
         self[row_id] = OrderedDict()
      self[row_id][version] = col_dict
      
   def fetch(self, row_id):
      """
         BRIEF  Get matching rows
      """
      return '\n'.join(map(str, self[row_id].items()))
      
      