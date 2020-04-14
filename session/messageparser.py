#!/usr/bin/python3


def parse(message_in, session):
    admin_orders = {"die": df_session.kill,
                    "login": df_session.login,
                    "nv": df_session.new_vote,
                    "ev": df_session.kill_vote,

                    }
    public_orders = {"!v": df_session.new_vote,
                     "!r": df_session.get_results
                     }
    server_orders = {"Ping timeout": session.reconnect,
                     "PING :": session.ping}
    print(message_in.split(" "))
    message_in = message_in.split(" ")

    if "Ping timeout" in message_in:
        session.reconnect()

    if message_in[0] in server_orders or :
        server_orders[message_in[0]]()

    if "PRIVMSG" in message_in:
        name = message_in.split('!', 1)[0][1:]
        message = message_in.split('PRIVMSG', 1)[1].split(':', 1)[1]

        print("#" * 10)
        print(name, message)

        if message.startswith(session.nick) and name in session.admin:
            command = message.split(" ", 2)[2].split()
            try:
                admin_orders[command[0]](command[1:])
            except IndexError:
                admin_orders[command[0]]()
        if message[:2] in public_orders:
            command = message.split(" ", 1)[1].split()
            print(command)
            try:
                public_orders[command[0]](command[1:])
            except IndexError:
                public_orders[command[0]]()

