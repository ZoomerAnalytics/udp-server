import os
import re
import sys
import json
import socket
import logging

from datetime import datetime

is_in_debug_mode = os.getenv('UDP_SERVER_DEBUG', 0)
debug_mode_state = 'ON' if is_in_debug_mode else 'OFF'

logging.basicConfig(
    level=logging.DEBUG if is_in_debug_mode else logging.INFO,
    filename="/var/log/udp-server.log",
    format="%(asctime)s %(levelname)s %(message)s"
)

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 1234

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    logging.info("Socket created")
except socket.error:
    logging.critical("Failed to create socket. Error code is '%s'. Message is '%s'" % (str(msg[0]), msg[1]))
    sys.exit(2)


try:
    s.bind((SERVER_HOST, SERVER_PORT))
    logging.info("Socket successfully binded")
except socket.error:
    logging.critical("Bind failed. Error code is '%s'. Message is '%s'" % (str(msg[0]), msg[1]))
    sys.exit(2)

logging.info("Server has started successfully and operating on host %s and port %s" % (SERVER_HOST, SERVER_PORT))
logging.info("DEBUG mode is %s", debug_mode_state)

while 1:
    d = s.recvfrom(1024)
    data = d[0] # data
    addr = d[1] # client's address

    if not data:
        break

    #[17/06/2016 12:30] Time to move
    # message = re.match(r'\[(?P<event_datetime>.*)\] (?P<event_message>.*)', data)
    message = data

    if message is None:
        error_message = "Error: wrong message format. Must be '[DD/MM/YYYY HH:MM] <MESSAGE BODY>'\n"
        logging.error(error_message)
    else:
        logging.debug("Received a message. Sender's address is '%s', message is '%s'" % (addr, data))

        message_dict = message.groupdict()
        try:
            timestamp = datetime.strptime(message_dict['event_datetime'], '%d/%m/%Y %H:%M').strftime("%s")
        except Exception as e:
            error_message = "Can't convert the given datetime '%s' to timestamp." % message_dict['event_datetime']
            logging.error(error_message)

        else:
            result = {}
            result['timestamp'] = timestamp
            result['message'] = message_dict['event_message']
            sys.stdout.write(json.dumps(result) + '\n')

            logging.debug("Client's address is '%s', result is '%s'" % (addr, result))

s.close()
