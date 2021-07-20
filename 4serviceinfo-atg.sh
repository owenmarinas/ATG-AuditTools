#!/bin/bash
# to be executed locally eg ht --ssh-args='-q' --noheader --no-info-summary --sudo -s serviceinfo-atg.sh --script-args service  1137633
# owen.marinasom

serv=$1
### Im I weblogic? (Get weblogic Vserion and patch)
if test -d /opt/app/weblogic
then
   webllogichost=1
   echo -e "$serv JVM"
   ps -o command -u ecom |grep $serv | tr ' ' '\n\t' | sort -u
   echo -e "End of $serv JVM"
fi



