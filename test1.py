import os
import requests
requests.packages.urllib3.disable_warnings()
import json
import sys
import app



def get_neuvector_token(username,password,controller_ip):
    url = "https://"+controller_ip+":10443/v1/auth"
    headers = {'content-type': 'application/json'}
    payload = {"password" : {"username" : username, "password" : password}}
    r = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
    return (r)


def convert_token(token):
    token_string = str(token.text)
    token_dict=json.loads(token_string)
    return(token_dict['token']['token'])


def store_env(token, controller_ip):
    os.environ['contoller_token'] = token
    os.environ['controller_ip'] = controller_ip

def main():
    username = sys.argv[1]
    password = sys.argv[2]
    controller_ip = sys.argv[3]
    token_txt = get_neuvector_token(username, password, controller_ip)
    token= convert_token(token_txt)
    store_env(token,controller_ip)
    os.system("python3 app.py {} {}".format(token,controller_ip))




if __name__ == '__main__':
    main()

