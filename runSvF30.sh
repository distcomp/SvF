#!/bin/bash
pyomo --version
#export SVF_HOME=/home/sokol/C/_SvF
#export PYTHONPATH=$SVF_HOME/Lib26
#echo "PYTHONPATH="$PYTHONPATH
#echo "SVF_HOME="$SVF_HOME

# Write correct path below !!!
export SVFLIBPATH=/mnt/hgst2/ext4/git_work/SvF/Lib30

echo $1
echo  "python "$SVFLIBPATH"/_START.py" 

python $SVFLIBPATH/_START.py $1

#exit_code=$?

#echo 'exit_code:'
#echo $exit_code
#echo '########## RUN StartModel.py #####################', $exit_code

#if [ $exit_code -eq 0 ]
#then
#   python StartModel.py
#else
#   echo "что-то пошло не так"
#fi
#python StartModel.py

#python $SVF_HOME/Lib26/_START26n.py >> SvF.out

#########################  http://citforum.ru/programming/shell/gl4.shtml    ####################
