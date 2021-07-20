#!/usr/bin/env python3

# Authenticate racker || read passwdsafe project page
# login wo weblogic console || generate serverTable File on disc


import requests

#from requests import request, session
import urllib3
import lxml.html
import sys
from raxauth import raxauth
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

'''
sudo yum -y install python3 ; sudo -H pip3 install --upgrade pip ; sudo -H pip3 install requests keyring lxml
python3 -c "import keyring.util.platform_; print(keyring.util.platform_.config_root())"
cat /home/vagrant/.config/python_keyring/keyringrc.cfg
 [backend]
 default-keyring=keyrings.alt.file.PlaintextKeyring
git clone git@github.rackspace.com:devnull/rax_auth.git
cd ~/rax_auth/
sudo python3 setup.py install
'''

def gettoken():
    '''racker auth via passwd/RSA and return Rackspace Auth Token'''
    try:
        token = None
        print('\nEntering Auth')
        token = raxauth.get_racker_token_rsa()
        #token  = raxauth.get_racker_token(username="owen9865", password="", interactive=False, app_name='sso')
    except:
        print("Authentication error, the user does not have valid authentication details")
        sys.exit(0)
    return token

def getpwsafeprojectidname(token, Project_id):
    '''access passwordSafe and return list of credentials of a projectID'''
    pwsafebaseurl = "https://passwordsafe.corp..com"
    headers = {"X-AUTH-TOKEN":token,"Content-Type":"text/html","Accept":"application/json"}
    PathProj = "/projects/{0}.json?page=0".format(Project_id)
    urlproj = "%s%s" % (pwsafebaseurl,PathProj)
    try:    #connect to get the project ID
        pwresult = requests.get(urlproj, headers = headers, verify=False)
        if str(pwresult.status_code) == '200':
            #print("ID: ", pwresult.json()['project']['id'])
            result = str(pwresult.json()['project']['name'])
        else:
            result = str("the project ",Project_id, " does not exist")
            #print(pwresult.status_code)
    except:
        result = "Can't access passwdSafe project page"
    return(result.replace(" ",""))

def getlistoftabs(token, Project_id):
    PathCred = "/projects/{0}/credentials.json?page=0".format(Project_id)
    pwsafebaseurl = "https://passwordsafe.corp.com"
    headers = {"X-AUTH-TOKEN":token,"Content-Type":"text/html","Accept":"application/json"}
    urlcred = "%s%s" % (pwsafebaseurl,PathCred)
    try:    #connect to get the credentials
        listofenv=UniqListOfEnv=[]
        pwcresult = requests.get(urlcred, headers = headers, verify=False)
        for item in pwcresult.json():
            listofenv.append(item['credential']['category'])
        UniqListOfEnv = sorted(set(listofenv))
    except:
        print("Can't access passwdSafe")
    return(UniqListOfEnv, pwcresult)

def getservertable(WeblbaseUrl, WeblUser,WeblPasswd ):
    print('\n',WeblbaseUrl, WeblUser,WeblPasswd)
    proxies = {'http': 'socks5://127.0.0.1:12345', 'https': 'socks5://127.0.0.1:12345'}
    LoginURL = WeblbaseUrl + 'login/LoginForm.jsp'
    j_securityURL = WeblbaseUrl + 'j_security_check'
    ServerTableURL = WeblbaseUrl + 'console.portal?_nfpb=true&_pageLabel=CoreServerServerTablePage'
    nnames = servers = []
    try:
        session = requests.session()
        login = session.get(LoginURL, proxies=proxies, verify=False)
        login_html = lxml.html.fromstring(login.text)
        hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
        form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
        cookie = session.cookies.get_dict()
        form['j_username'] = WeblUser
        form['j_password'] = WeblPasswd
        print('\nAUTH_FORM',form)
        print('\nCOOKIE ',cookie)
        response = session.post(j_securityURL, data=form, cookies=cookie, proxies=proxies, verify=False)
        #print('\nresponse.status_code\n',response.status_code)
        #print('\nresponse.text\n',response.text)
        print('\nresponse.headers\n',response.headers)
        print('\nresponse.request.headers\n',response.request.headers)

        if 'Authentication Denied' in response.text:
            print("post ","POST Authentication Denied")
        else:
            print ('POST Authentication OK')
    except:
        print("Can't access weblogic console on POST")
    try:
        result = session.get(ServerTableURL, cookies=cookie, proxies=proxies, verify=False)
        #print(result.status_code)
        #print(result.content)
        session.close()
        servertable=lxml.html.fromstring(result.text) #the servertable page in HTML format
        nnames=servertable.xpath('//td[@scope="row"]/a')   #get the column Names
        mchine=servertable.xpath('//td[contains(@*,"machineName")]')  # get the Machine Column
        lport=servertable.xpath('//td[contains(@*,"listenPort")]')    # get the ListeningPort Column
    except:
        print("Can't access weblogic console on GET ServerTableURL")
    print(len(nnames))
    for i in range(0, len(nnames)):
       servers.append(nnames[i].text + ' ' + mchine[i].text + ' ' + lport[i].text + '\n')
    return(servers)

def servers2file(servers, PIDName):
    ServersFile = str(PIDName) + "_ATG_" + EnvTab  + '.txt'
    try:
        f = open(ServersFile, 'w')
        for line in servers:
           f.write(line)
        f.close()
    except:
         print("Can't write to disk",ServersFile)
    return(ServersFile)

#Main
token = gettoken()
#print(token)
if len(sys.argv) > 1:
    Project_id = sys.argv[1]
else:
    Project_id = None


if not Project_id:
    Project_id=str(input("PasswordSafe Client ID: "))
print(Project_id)
pname= getpwsafeprojectidname(token,Project_id)
ListOfEnv, credentdata = getlistoftabs(token, Project_id)
if len(sys.argv) > 2:
    EnvTab = sys.argv[2]
else:
    print(ListOfEnv)
    EnvTab = str(input("Select a Tab: "))
print(EnvTab)
for item in credentdata.json():
    if item['credential']['category'] == EnvTab and "_weblogic_password" in item['credential']['description']:
        #print(item['credential']['description'], "found in passwordsafe")
        webluser = str(item['credential']['username'])
        weblpasswd = str(item['credential']['password'])
        weblbaseurl = str(item['credential']['url'] + "/")

serverlist = getservertable(weblbaseurl, webluser, weblpasswd)
if len(serverlist) > 0:
    print(servers2file(serverlist, getpwsafeprojectidname(token, Project_id)))
else:
    print('serverList empty')
#print(serverlist)


