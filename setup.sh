#!/bin/bash

# install python 2.7
if [[ "$(python --version 2>&1)" != *'2.7'* ]]; then
   sudo yum update
   sudo yum install scl-utils
   sudo yum install centos-release-scl-rh
   sudo yum install python27
   sudo scl enable python27 bash
fi

# use python 2.7
PY27_DIR=/usr/lib/python2.7/site-packages/
if [[ -d $PY27_DIR && $PYTHONPATH != *$PY27_DIR* ]]; then
   export PYTHONPATH=$PY27_DIR:$PYTHONPATH
fi

# install hbase for python
if ! $(python -c "import starbase" 2> /dev/null) ; then
   python -m pip install starbase
fi

# example hbase cmds
# cat src/hbase_cmds.txt | hbase shell -n

