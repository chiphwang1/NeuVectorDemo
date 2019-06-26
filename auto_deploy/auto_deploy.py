#!/usr/bin/env python


import os
import time


def kube_create_svc_deployment(deployment_list):
    for deployment in deployment_list:
        os.system("kubectl create -f ./{}".format(deployment))
        time.sleep(3)


def create_namespace(namespace):
    os.system("kubectl create ns {}".format(namespace))



def main():

    deployment_list = ["redis-pod.yaml","nodejs-pod.yaml","api_server.yaml", "exploit.yaml",
                 "iodine_client.yaml", "mysql-pod.yaml", "nginx-pod.yaml"]
    namespace = "demo"

    create_namespace(namespace)
    kube_create_svc_deployment(deployment_list)

if __name__ == '__main__':
    main()
