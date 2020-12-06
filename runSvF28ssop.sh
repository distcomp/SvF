#!/bin/bash
pyomo --version
#export SVF_HOME=/home/sokol/C/_SvF
#export PYTHONPATH=$SVF_HOME/Lib26
#echo "PYTHONPATH="$PYTHONPATH
#echo "SVF_HOME="$SVF_HOME



echo $1
echo  "pytho Lib28/_START.py"

python Lib28/_START.py $1
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
