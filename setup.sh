#!/bin/bash

PY27_DIR=/usr/lib/python2.7/site-packages/

# install python 2.7
if [[ ! -d $PY27_DIR ]]; then
   sudo yum update
   sudo yum install scl-utils
   sudo yum install centos-release-scl-rh
   sudo yum install python27
   sudo scl enable python27 bash
else
   echo "python 2.7 is already installed"
fi

# use python 2.7
if [[ -d $PY27_DIR && $PYTHONPATH != *$PY27_DIR* ]]; then
   export PYTHONPATH=$PY27_DIR:$PYTHONPATH
else
   echo "python 2.7 is already in PYTHONPATH"
fi

# install hbase for python
if ! $(python -c "import starbase" 2> /dev/null) ; then
   python -m pip install starbase
else
   echo "starbase is already pip-installed"
fi

# download large input file
if [[ -d in && ! -f in/movies.txt ]]; then
   cd in
   curl https://snap.stanford.edu/data/movies.txt.gz -o movies.txt.gz
   gunzip movies.txt.gz
   command rm -f movies.txt.gz
   cd -
elif [[ ! -d in ]]; then
   echo "Run 'mkdir in', then re-run setup.sh"
else
   echo "Large input file already exists"
fi

# Why does a read-only state get applied sometimes?
sudo chmod -R 777 .

