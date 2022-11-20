import json
import datetime

def decoder(it):
    it = it.decode('utf-8')
    it = json.loads(it)
    return dict(it)


def encoder(it):
    it = json.dumps(it)
    it = it.encode('utf-8')
    return it
