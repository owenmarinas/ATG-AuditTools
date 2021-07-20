#!/bin/bash
# to be executed locally eg ht --ssh-args='-q' --noheader --no-info-summary --sudo -s hostinfo-atg.sh 1137633
# owen.marinas@.com |

echo -e "1-Status of `hostname`"
#echo -e "\n2-Overview"
#echo -e "\n3-Infrastructure"
#echo -e "\n4-Applications"

### Im I dynamo ?(get OracleVersion)
if [ "`ps xa|grep -i [d]ynamo |wc -l`" -gt "0" ]
then
   dynamohost=1
   echo -e "411 OracleVersion"
   dynamouri=`netstat -alpn|awk '{print $4}'|grep 20080|head -n1`
   dynamopath='/dyn/admin/atg/dynamo/admin/en/running-products.jhtml'
   dynver=`for i in admin admin123 admin1234 ; do curl -sl -u admin:$i  http://$dynamouri/$dynamopath | grep -A6 DAS-UI |sed -e 's/<[^>]*>//g'|grep -E ^[1..9];done`
   echo -e  "\t$dynver"
fi

### Im I endeca? (Get Endeca Baase Version)
if test -d /opt/app/endeca
then
   endecahost=1
   echo -e "412 EndecaBaseLevel"
   enddecaver=`ls /opt/app/endeca/CAS/ | grep -E '[0-9]'`
   #enddecaver=`/opt/app/endeca/MDEX/11.3.2/bin/dgraph --version`
   echo -e "\t$enddecaver"
   echo -e "412 EndecaPatchT&F"
   endmd5=`pp/endeca/ToolsAndFrameworks/11.3.2.0.0/server/webapps/.war|awk '{print $1}'`
   case "$endmd5" in
       endPatch="patch17"
     ;;
     *)
     endPatch="Unknow"
     ;;
   esac
   echo $endPatch
   echo -e "\n"
   #echo -e "\n6 NFS Mounts"
   #Mounts=`nfsstat -m|grep -v Flags`
   #echo -e "\t$Mounts""
fi

### Im I weblogic? (Get weblogic Vserion and patch)
if test -d /opt/app/weblogic
then
   webllogichost=1
   echo -e "413 Weblogic"
   jj=`java -cp /opt/app/weblogic/wlserver/server/lib/weblogic.jar weblogic.version |grep 'WebLogic Server'`
   echo -e "4131 WeblogicVer\n\t$jj"
   opat=`su ecom /opt/app/weblogic/OPatch/opatch lsinventory |grep 'Patch  [^0-9]*'|sort|head -n1`
   echo -e "4132 OPatch\n\t$opat"
   echo -e "414 NFSVer"
   NfsVer=`nfsstat -m | tr ',' '\n'|grep ver|sort -u `
   while IFS= read -r line; do echo -e "\t$line"; done <<< "$NfsVer"
   echo -e "415 JDK"
   jv=$((java -version) 2>&1)
   #echo -e "\t$jv"
   while IFS= read -r line; do echo -e "\t$line"; done <<< "$jv"

   ###Im I vormetrix
   if test -d /opt/vormetric/
   then
     echo -e "416 Vormetric"
     if ls /opt/vormetric/DataSecurityExpert/agent/key/log/install.key.log* 1> /dev/null 2>&1
     then
       VorMetVer=`grep 'Agent Version' /opt/vormetric/DataSecurityExpert/agent/key/log/install.key.log*|sort -u`
       echo -e "\t$VorMetVer"
     else
       echo "Can't find Vormetric Version"
     fi
   fi
   echo -e "\n5-OS"
   echo -e "51 ulimits"
   lim=`grep -v '#\|^[[:blank:]]*$'  /etc/security/limits.conf`
   while IFS= read -r line; do echo -e "\t$line"; done <<< "$lim"
   #echo -e "\n6 NFS Mounts"
   #Mounts=`nfsstat -m|grep -v Flags`
   #while IFS= read -r line; do echo -e "\t$line"; done <<< "$Mounts"
fi
