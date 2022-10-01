import logging

logging.basicConfig(
    filename = "server.log",
    format = "%(levelname)-10s %(asctime)s %(message)s",
    level = logging.INFO
)

log = logging.getLogger('server.' + __name__)