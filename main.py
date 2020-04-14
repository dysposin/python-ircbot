#!/usr/bin/python3
import socket
from session import session, message
from vote import vote

def main():

    df_session = session.Session(irc_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM))

    while df_session.alive:

        message_in = df_session.receive_message()




if __name__=="__main__":
    main()
