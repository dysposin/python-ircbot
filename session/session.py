#!/usr/bin/python3
from session import config, messageparser
from vote import elections

class Session:

    def __init__(self, irc_socket,
                 server=config.server,
                 channels=config.channels,
                 nick=config.nick,
                 admin=config.admin,
                 max_reconnect=config.max_reconnect,
                 passwd=config.passwd):
        self.server = server
        self.channels = channels
        self.nick = nick
        self.admin = admin
        self.max_reconnect = max_reconnect
        self.passwd = passwd
        self.irc_socket = irc_socket
        self.alive = True

        self.election = elections.Elections()
        self.startup()

    def startup(self):
        for i in range(self.max_reconnect):
            if self.connect():
                break
        for channel in self.channels:
            self.join_channel(channel)


    def reconnect(self):
        for i in range(self.max_reconnect):
            if self.connect():
                break


    def connect(self):
        print("Connecting {}...".format(self.server))

        for port in range(6667, 6669):
            try:
                self.irc_socket.connect((self.server, port))
                self.irc_socket.send(bytes("USER {0} {0} {0} {0}\n".format(self.nick), "UTF-8"))
                self.irc_socket.send(bytes("NICK {}\n".format(self.nick), "UTF-8"))
            except Exception as e:
                print("Port {} did not respond.\n{}".format(port, e))
                if port == 6669:
                    return 0
        return 1

    def login(self, passwd, id):
        if passwd == self.passwd:
            self.admin.append(id)

    def join_channel(self, channel):
        print("Joining channel {}...".format(channel))
        self.irc_socket.send(bytes("JOIN {}\n".format(channel), "UTF-8"))
        message = ""
        while "End of NAMES list" not in message:
            message = self.irc_socket.recv(2048).decode("UTF-8")
            message = message.strip('\n\r')
            if message != "":
                print("ch: ", message)
        print("Joined channel {}".format(channel))


    def ping(self, daemon):
        print("PONG!")
        self.irc_socket.send(bytes("PONG :{}\n".format(daemon), "UTF-8"))


    def receive_message(self):
        message_in = self.irc_socket.recv(2048).decode("UTF-8").strip('\n\r')
        messageparser.parse(message_in, self)


    def send_message(self, message, target):
        self.irc_socket.send(bytes("PRIVMSG {} :{}\n".format(target, message), "UTF-8"))


    def alive(self):
        return self.alive

    def kill(self):
        self.alive = False

    def new_vote(self, name, positions=3):
        self.elections.add_election(name, positions)

    def get_results(self, name=None):
        self.election.results(name)

    def kill_vote(self, name):
        self.elections.close_election(name)