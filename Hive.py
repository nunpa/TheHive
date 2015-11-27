#!/usr/bin/env python
import socket
import sys
import os
import time
import curses

os.system('clear')

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

#following from Python cookbook, #475186
def has_colours(stream):

    if not hasattr(stream, "isatty"):

        return False

    if not stream.isatty():

        return False # auto color only on TTYs

    try:

        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2

    except:

        return False

has_colours = has_colours(sys.stdout)


def colour_out(text, colour=WHITE):

        if has_colours:
                seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
                sys.stdout.write(seq)
        else:
                sys.stdout.write(text)



servers = ["127.0.0.1"]
port =  9999
data = "ECHO"

while 1:

    for server in servers:

        data = ''
        # Create a socket (SOCK_STREAM means a TCP socket)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)

        try:
            # Connect to server and send data
            sock.connect((server, port))
            sock.sendall(data + "\n")

            # Receive data from the server and shut down
            received = sock.recv(1024)

            data =  str(received).split(";")
            colour_out(server+"  #  ", BLUE)

            for stat in data:

                fine = stat.split(":")
                stat_name =  fine[0]


                if stat_name == 'CPU':

                    if float(fine[1]) <= 80:

                        color = GREEN

                    elif float(fine[1]) >= 80 and float(fine[1]) <= 90:

                        color = YELLOW

                    else:

                        color = RED

                    colour_out(fine[0]+" : ", WHITE)
                    colour_out(fine[1]+" % ", color)


                elif stat_name == 'HD':

                    value = fine[1].split(",")

                    if float(value[1]) >= 25:

                        color = GREEN

                    elif float(value[1]) <= 25 and float(value[1]) >= 10:

                        color =YELLOW

                    else:

                        color = RED

                    colour_out(fine[0]+" : ", WHITE)
                    colour_out(value[0]+" - "+value[1]+" % ", color)


                elif stat_name == 'NUP':

                        colour_out(fine[0]+" : ", WHITE)
                        colour_out(fine[1]+" MB/s ", CYAN)


                elif stat_name == 'NDOWN':

                        colour_out(fine[0]+" : ", WHITE)
                        colour_out(fine[1]+" MB/s ", CYAN)


                elif stat_name == 'RAM':

                    if float(fine[1]) <= 80:

                        color = GREEN

                    else:

                        color = RED

                    colour_out(fine[0]+" : ", WHITE)
                    colour_out(fine[1]+" % ", color)


                elif stat_name == 'SWAP':

                    if float(fine[1]) <= 50:

                        color = GREEN

                    elif float(fine[1]) >= 50 and float(fine[1]) <= 80:

                        color = YELLOW

                    else:

                        color = RED

                    colour_out(fine[0]+" : ", WHITE)
                    colour_out(fine[1]+" % ", color)


                elif stat_name == 'USERS':

                    colour_out(fine[0]+" : ", WHITE)
                    colour_out(fine[1], MAGENTA)

            print "\r"

        except Exception, e:

                colour_out(server+" # ", RED)
                print "\r"
                #print e
                #sys.stdout.write("\a")

        finally:

            sock.close()

    time.sleep(5)
    print "----------------------------------------"
