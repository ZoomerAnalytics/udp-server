import os
import sys
import socket
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[logging.StreamHandler()]
)

SERVER_HOST = '0.0.0.0'
SERVER_PORT = os.environ.get('UDP_SERVER_PORT', 10000)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    logging.info("Socket created")
except socket.error as ex:
    logging.error(ex)
    sys.exit(2)


try:
    s.bind((SERVER_HOST, SERVER_PORT))
    logging.info("Socket successfully binded")
except socket.error as ex:
    logging.critical(ex)
    sys.exit(2)

while 1:
    package = s.recvfrom(1024)
    message = package[0]
    address = package[1]

    if message:
        logging.info('%s [%s]' % (message.decode('utf-8'), address[0]))

s.close()
