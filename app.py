from flask import Flask, request
import requests
import re
import os
import json
import sys
import time
requests.packages.urllib3.disable_warnings()


def create_capture(workload_id,token,controller_ip):
    print(token)
    url = "https://"+ controller_ip + ":10443/v1/sniffer?f_workload="+ workload_id
    headers = {'content-type': 'application/json','X-Auth-Token': token}
    payload = {"sniffer" : {"file_number": 50}}
    r = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
    print(r.text)
    return (r)



def delete_capture(sniffer_id, controller_ip, token):
    headers = {'content-type': 'application/json','X-Auth-Token': token}
    url = "https://"+ controller_ip + ":10443/v1/sniffer/stop/"+ sniffer_id
    time.sleep(7)
    r = requests.patch(url, headers=headers, verify=False)
    print(r)
    return(r)


def convert_token(token):
    token_string = str(token.text)
    token_dict=json.loads(token_string)
    return(token_dict['result']['id'])

def send_to_slack(payload_data):
    url = "https://hooks.slack.com/services/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"
    headers = {'content-type': 'application/json'}
    message = "Critical MySQL Attack Detected, Action: Packet Capture Taken: " + str(payload_data)
    payload= {'text' : message}
    r = requests.post(url, data=json.dumps(payload), verify=False, headers=headers)
    print (" slack response is {}".format(r))


def create_payload(req_data, sniffer_id):
    alert_dict = {}
    s = req_data['text']
    alert_string = re.split(',', s)
    for field in alert_string:
        id  = re.split('=', field)
        alert_dict[id[0]] = id[1]
    payload = {"Time" : alert_dict['reported_at'],"Type": "Threat", "Attack  Name" : alert_dict['name'], "client name": alert_dict['client_workload_name'], 
            'server name' : alert_dict['server_workload_id'], "capture_id" : sniffer_id}
    return payload

    



app = Flask(__name__) #create the Flask app

@app.route('/test', methods=['POST'])
def send_api():
    token = sys.argv[1]
    controller_ip = sys.argv[2]
    #print(request._dict_.keys())
    req_data = request.get_json()
    print (req_data)
    s = req_data['text']
    print("*******************************")
    alert_string = re.split(',', s)
    print("#################################")
    for i in alert_string:
        if  "INFO" in i:
            print(i)
            for id in alert_string:
                if  "client_workload_id" in id:
                    workload_id= re.split('=', id)
                    print(workload_id)
                    print(" {} and id is {}". format(workload_id[0], workload_id[1]))
                    r = create_capture(workload_id[1],token,controller_ip)
                    print(r)
                    sniffer_id = convert_token(r)
                    payload = create_payload(req_data, sniffer_id)
                    send_to_slack(payload)
                    delete_capture(sniffer_id,controller_ip, token)
                    print(r)



    return("accepted")

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
