#!/bin/bash

# install python 2.7
sudo yum update
sudo yum install scl-utils
sudo yum install centos-release-scl-rh
sudo yum install python27
sudo scl enable python27 bash
export PYTHONPATH=/usr/lib/python2.7/site-packages/:$PYTHONPATH

# sudo yum makecache
# sudo yum install yum-utils
# sudo yum install https://centos7.iuscommunity.org/ius-release.rpm
# sudo yum makecache
# sudo yum install python36u

# sudo yum install python-pip
# sudo pip install starbase

# run hbase commands
# cat src/hbase_cmds.txt | hbase shell -n

