import os
import socket

HOST = socket.gethostname()
PORT = 12372
SERVER_LOG_PATH = 'log/server.log'
CLIENT_LOG_PATH = 'log/client.log'

PATH_LOGGING_CALL_FUNC = os.getcwd()+'/log/calling_func.txt'

term_or_file = 'file' # terminal or file
