import socket
import sys
import os
import time

os.system('clear')

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WHITE= '\033[37m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    BLINK = '\033[5m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CYAN =  '\033[96m'


servers = ["127.0.0.1","192.168.1.39"]
port =  9999
data = "ECHO"

while 1:

    for server in servers:

        data = ''
        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to server and send data
            sock.connect((server, port))
            sock.sendall(data + "\n")

            # Receive data from the server and shut down
            received = sock.recv(1024)

            data =  str(received).split(";")
            output = bcolors.BLUE+bcolors.BLUE+server+"  #  "

            for stat in data:

                fine = stat.split(":")
                stat_name =  fine[0]

                if stat_name == 'CPU':

                    if float(fine[1]) <= 80:

                        output = output+str( bcolors.WHITE)
                        output = output+fine[0]+" : "
                        output = output+str( bcolors.GREEN)
                        output = output+fine[1]
                        output = output+"% "


                    elif float(fine[1]) >= 80 and float(fine[1]) <= 90:

                        output = output+str( bcolors.WHITE)
                        output = output+fine[0]+"  : "
                        output = output+str( bcolors.YELLOW)
                        output = output+fine[1]
                        output = output+"% "

                    else:

                        output = output+str( bcolors.FAIL)
                        output = output+fine[0]+"  : "
                        output = output+str( bcolors.BLINK)
                        output = output+fine[1]
                        output = output+"% "
                        output = output+str( bcolors.ENDC)



                elif stat_name == 'HD':

                    value = fine[1].split(",")

                    if float(value[1]) >= 25:

                        output = output+str( bcolors.WHITE)
                        output = output+fine[0]+" : "
                        output = output+str( bcolors.GREEN)
                        output = output+value[0]+" - "+value[1]
                        output = output+"% "


                    elif float(value[1]) <= 25 and float(value[1]) >= 10:

                        output = output+str( bcolors.WHITE)
                        output = output+fine[0]+"  : "
                        output = output+str( bcolors.YELLOW)
                        output = output+value[0]+" - "+value[1]
                        output = output+"% "

                    else:

                        output = output+str( bcolors.FAIL)
                        output = output+fine[0]+"  : "
                        output = output+str( bcolors.BLINK)
                        output = output+value[0]+" - "+value[1]
                        output = output+"% "
                        output = output+str( bcolors.ENDC)

                elif stat_name == 'NUP':

                        output = output+str( bcolors.WHITE)
                        output = output+fine[0]+" : "
                        output = output+str( bcolors.CYAN)
                        output = output+fine[1]
                        output = output+" MB/s "

                elif stat_name == 'NDOWN':

                        output = output+str( bcolors.WHITE)
                        output = output+fine[0]+" : "
                        output = output+str( bcolors.CYAN)
                        output = output+fine[1]
                        output = output+" MB/s "

                elif stat_name == 'RAM':

                        output = output+str( bcolors.WHITE)
                        output = output+fine[0]+" : "
                        output = output+str( bcolors.CYAN)
                        output = output+fine[1]
                        output = output+" % "

                elif stat_name == 'SWAP':

                        output = output+str( bcolors.WHITE)
                        output = output+fine[0]+" : "
                        output = output+str( bcolors.CYAN)
                        output = output+fine[1]
                        output = output+" % "

            output = output+str( bcolors.ENDC)
            print output

        except Exception, e:

                print bcolors.FAIL+"unable to connect to "+server
                #print e
                #sys.stdout.write("\a")

        finally:
            sock.close()

    time.sleep(5)
