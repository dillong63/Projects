#Code written by Dillon Geary for CSC 49008 final project

from urllib.request import urlopen
from time import sleep
import json

#ALL below check one of the parking spots

#opens the url
#parses the json
#returns 1 or 0 as status of open or closed
#if this fails, catch so that everything does not crash

def statusPS1(cur):
    try:
        htmlps1= urlopen('http://dweet.io/get/latest/dweet/for/DGPS1').read()
        myJSON = json.loads(htmlps1)
        content=myJSON["with"][0]["content"]
        val = list(content.values())[0]
        v1 = int(val)
        if(v1!=cur):
            return v1
        else:
            return cur
    except:
        print('Error in reading sensor 1, returned previous value')
        return cur
        
        
def statusPS2(cur):
    try:
        htmlps1= urlopen('http://dweet.io/get/latest/dweet/for/DGPS2').read()
        myJSON = json.loads(htmlps1)
        content=myJSON["with"][0]["content"]
        val = list(content.values())[0]
        v1 = int(val)
        if(v1!=cur):
            return v1
        else:
            return cur
    except:
        print('Error in reading sensor 2, returned previous value')
        return cur
        
def statusPS3(cur):
    try:
        htmlps1= urlopen('http://dweet.io/get/latest/dweet/for/DGPS3').read()
        myJSON = json.loads(htmlps1)
        content=myJSON["with"][0]["content"]
        val = list(content.values())[0]
        v1 = int(val)
        if(v1!=cur):
            return v1
        else:
            return cur
    except:
        print('Error in reading sensor 3, returned previous value')
        return cur
