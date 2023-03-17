#!/bin/bash
pyomo --version
#export SVF_HOME=/home/sokol/C/_SvF
#export PYTHONPATH=$SVF_HOME/Lib26
#echo "PYTHONPATH="$PYTHONPATH
#echo "SVF_HOME="$SVF_HOME



echo $1
echo  "python /home/vladimirv/git_work/SvF/SvFlib/_START.py"

#python /home/sokol/C/SvF/Lib30/_START.py $1
#python /home/sokol/D/SvF/SvFlib/_START.py $1
python /home/vladimirv/git_work/SvF/SvFlib/_START.py $1

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
