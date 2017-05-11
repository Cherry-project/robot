python startup.py > journal/robot.log 2>&1 &
echo $! > journal/save_pid.txt
echo "server up and running, pid : " `cat journal/save_pid.txt`