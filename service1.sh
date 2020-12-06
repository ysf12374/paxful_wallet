
#set -x

PID=`ps ax | grep twitter_user.py`
option="${1}"


case ${option} in

stop)




if  [[ -f /proc/$PID/exe  ]]
 then
kill -9 $PID
echo "app stoped"
echo $PID killed

else
echo " app is already stopped. "
fi





          ;;

start)
     if [ $PID > 0 ]; then
     echo " app is running please stop it first"
     else

     nohup python3.7 twitter_user.py &
     sleep 1
     fi
          ;;

status )
     if [[ $PID > 0 ]]; then
     echo " app is running in PID $PID "
     else
     echo "app is not running"
     fi

          ;;
     *)
          echo "please use start|stop|status"
          ;;
esac
