# -*- coding: UTF-8 -*-
import requests
import re
from http.server import BaseHTTPRequestHandler
import json

def getdata(name):
    gitpage = requests.get("https://github.com/" +name)
    data = gitpage.text
    datadatereg = re.compile(r'data-date="(.*?)"/>')
    datacountreg = re.compile(r'data-count="(.*?)" data-date')
    datadate = datadatereg.findall(data)
    datacount = datacountreg.findall(data)
    datacount =list(map(int, datacount))
    contributions = sum(datacount)
    datalist=[]
    for index,item in enumerate(datadate):
        itemlist = {"date":item,"count":datacount[index]}
        datalist.append(itemlist)
    returndata = {
        "tatal":contributions,
        "contributions":[
            datalist
      ]

    }
    return returndata

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        path = self.path
        user = path.split('?')[1]
        data = getdata(user)
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
        return
