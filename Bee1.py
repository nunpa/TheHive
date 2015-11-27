#!/usr/bin/env python
import os
from collections import namedtuple
import time
import SocketServer
import psutil

psutil_version =  psutil.__version__

def get_ram():

    if  float( psutil.__version__[0:3]) > 0.5:

        mem_ram = psutil.virtual_memory()
        mem_swap = psutil.swap_memory()
    else:

        mem_ram = psutil.phymem_usage()
        mem_swap = psutil.virtmem_usage()

    readable =  "RAM:"+str(mem_ram.percent)+";"
    readable = readable+"SWAP:"+str(mem_swap.percent)+";"

    return readable


def get_users():

    if float( psutil.__version__[0:3]) > 0.5:

        if int(psutil_version[0]) < 2:

            users = psutil.get_users()

        elif int(psutil_version[0]) >= 2:

            users = psutil.users()


        unique_users = []

        for user in users:

            if user[0] not in unique_users:

                unique_users.append(user[0])

        if len(unique_users)>=1:

            for username in unique_users:

                readable = username+" "

            return "USERS:"+readable
            
        else:

           return "none"

    else:

        return "unknow"

def get_network():

    if int(psutil_version[0]) >= 1:

        net1 = psutil.net_io_counters(pernic=True)
        time.sleep(2)
        net2 = psutil.net_io_counters(pernic=True)

    else:

        net1 = psutil.network_io_counters(pernic=True)
        time.sleep(2)
        net2 = psutil.network_io_counters(pernic=True)

    sent1 = net1['eth0'].bytes_sent
    received1 = net1['eth0'].bytes_recv

    sent2 = net2['eth0'].bytes_sent
    received2 = net2['eth0'].bytes_recv

    upload =round((((float(sent2-sent1)/1024)/1024)/2),2)
    download =round((((float(received2-received1)/1024)/1024)/2),2)

    readable = "NUP:"+str(upload)+";NDOWN:"+str(download)+";"

    return readable


def disk_usage(path):

    st = os.statvfs(path)
    free = (((st.f_bavail * st.f_frsize)/1024)/1024)
    total =  (((st.f_blocks * st.f_frsize)/1024)/1024)
    used = (((st.f_blocks - st.f_bfree) * st.f_frsize/1024)/1024)
    if free > 1024:
        #a gigas
        readable = str(free/1024)+" GB"
    else:
        readable = str(free)+" MB"

    percent = readable+","+str(round (( (float(free) /float(total) ) * 100),2))
    return percent


def my_status():

    cores = os.sysconf("SC_NPROCESSORS_ONLN")

    load= str(os.getloadavg())
    load = load.split(',')
    load  = str((float(load[1])/cores)*100)

    hards = ('/')
    response = ''

    response = response+"CPU:"+load+";"
    response = response+get_ram()
    response = response+get_network()

    for hd in hards:

        response = response+"HD:"+disk_usage(hd)+";"

    response = response+get_users()

    return response


class MyTCPHandler(SocketServer.BaseRequestHandler):


    def handle(self):

        self.data = self.request.recv(1024).strip()
        respuesta= str(my_status())
        self.request.sendall(respuesta)
        #print respuesta


if __name__ == "__main__":

    HOST, PORT = "0.0.0.0", 9999
    SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
