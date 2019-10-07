# HBase_Demo

### HW2 : HBase, Due Oct 12
- Download “movies.txt.gz” From the link https://snap.stanford.edu/data/web-Movies.html.
- Insert this data to the HBase:
- Keep two column familys: (i) User (contains columns ‘userid’ and ‘profilename’) (ii) Product (contains remaining columns)
- Create a unique row keys for each entry (see which column, OR, concatenation of which two columns can be considered as row key) 15%
- Create versions for some column family.
- Put multiple data for some specific entry which allows versioning. (Put command)
- Get one or more versions for that entry to see if it works. (Get command)	15%
- Write an aggregate query that involves column ‘helpfulness’
- Write an aggregate query that involves column ‘score’	30%
- Write a query that involves sorting	15%
- Write two queries that shows some analytics from the ‘review text’ and ‘review summary’	20%
- Submit your queries with the screenshots of the sample output (either from terminal / programming IDE)	5%

### General Information (Cloudera):

* Operating System:         Mac -> Microsoft Remote Desktop, Windows -> Default Remote Desktop, Ubuntu -> Remmina
* Machine:                  cqs-cs6304-xxx.ats.mst.edu
* User:                     cloudera
* Default Password:         stu-pass
* Change Password Command:  sudo passwd cloudera

* "Firefox already running" error solve by command:     
* killall -SIGTERM firefox
* If HBase doesn't work and shows the error: "Can't get master address from ZooKeeper; znode data == null"
* sudo /sbin/service hbase-master restart # On Master host
* sudo /sbin/service hbase-regionserver restart # On all RS hosts
