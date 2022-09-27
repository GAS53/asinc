import json

def in_put(it):
    di = json.load(it)
    if it['action'] == 'echo':
        echo(di)

def echo(di):
    
