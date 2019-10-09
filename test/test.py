from starbase import Connection
from requests.exceptions import ConnectionError
import sys

HBASE_PORTS = set(map(str, [ # cloudera 5.14.x & 5.2.x & 6.3.x
   16000, # Master
   16010, # Master
   16020, # RegionServer
   16030, # RegionServer
   60000, # Master
   60010, # Master
   60020, # RegionServer
   60030, # RegionServer
   2181 , # HQuorumPeer
   2888 , # HQuorumPeer
   3888 , # HQuorumPeer
   8080 , # REST
   20550, # REST
   8085 , # REST UI
   9090 , # Thrift Server
   9095 , # Thrift Server
   11060, # hbase-solr-indexer
]))

valid_ports = []
for port in HBASE_PORTS:
   try:
      c = Connection(port = port)
      t = c.table('tbl')
      t.create('col')
      t.drop()
      valid_ports.append(port)
      print("Connection success! port {0}".format(port))
   except ConnectionError:
      print("Connection failed!  port {0}".format(port))
   sys.stdout.flush()
   
for port in valid_ports:
   print("{0}\nport={1}\n{0}".format('-'*50, port))

   c = Connection(port = port)
   t = c.table('table3')

   print('t.create', t.create('column1', 'column2', 'column3'))
   print('t.exists', t.exists())
   print('t.add_columns', t.add_columns('column4', 'column5', 'column6', 'column7'))
   print('t.drop_columns', t.drop_columns('column6', 'column7'))
   print('t.columns', t.columns())
   print('t.drop', t.drop())

   print('t.insert', t.insert(
      'my-key-1',
      {
         'column1': {'key11': 'value 11', 'key12': 'value 12', 'key13': 'value 13'},
         'column2': {'key21': 'value 21', 'key22': 'value 22'},
         'column3': {'key32': 'value 31', 'key32': 'value 32'}
      }
   ))
   print('t.fetch', t.fetch('my-key-1'))
   print('t.fetch', t.fetch('my-key-1', ['column1', 'column2']))
   print('t.fetch', t.fetch('my-key-1', {'column1': ['key11', 'key13'], 'column3': ['key32']}))
   print('t.fetch', t.fetch('my-key-1', ['column1:key11', 'column1:key13', 'column3:key32']))
   print('t.fetch', t.fetch('my-key-1', ['column1:key11', 'column1:key13', 'column3:key32'], perfect_dict=False))


   print('t.insert', t.insert(
      'my-key-1a',
      {
         'column1:key11': 'value 11', 'column1:key12': 'value 12', 'column1:key13': 'value 13',
         'column2:key21': 'value 21', 'column2:key22': 'value 22',
         'column3:key32': 'value 31', 'column3:key32': 'value 32'
      }
   ))
   print('t.fetch', t.fetch('my-key-1a'))


   print('t.update', t.update(
      'my-key-1',
      {
         'column4': {'key41': 'value 41', 'key42': 'value 42'}
      }
   ))
   print('t.fetch', t.fetch('my-key-1'))


   print('t.remove', t.remove('my-key-1', 'column4'))
   print('t.fetch', t.fetch('my-key-1'))


   print('t.remove', t.remove('my-key-1'))
   print('t.fetch', t.fetch('my-key-1'))

