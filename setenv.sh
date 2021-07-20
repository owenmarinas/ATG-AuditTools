#
#  eg. ls /opt/app/build/scripts/brand/
#  eg. for i in dev01.properties dev02.properties ; do /home/rack/owen9865/setenv.sh $i client ; done
#
DESTDIR=/home/rack/owen9865
mkdir -p ${DESTDIR}
cd /opt/app/build/scripts/brand/${2}
#    $1 is properties file
source $1

#  $2 is BRAND
export BRAND=$2

# EnvType is the Col1 before DOT
export ENV_TYPE=`echo $1 | awk -F. '{print $1}'`

export USR_CONF=/opt/app/build/scripts/.credentials/${BRAND}/${ENV_TYPE}/${USER_CONF}
export USR_KEY=/opt/app/build/scripts/.credentials/${BRAND}/${ENV_TYPE}/${USER_KEY}
export PROG_DIR=${DESTDIR}

echo -e "\n $1    $BRAND  $ENV_TYPE"
echo -e "\n $USR_CONF $USR_KEY $PROG_DIR"
#cd /home/rack/owen9865
/opt/app/weblogic/oracle_common/common/bin/wlst.sh /home/rack/owen9865/wlst-info-gather.py

