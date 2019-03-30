
from http.client import HTTPSConnection
import http.client
from base64 import b64encode
from html.parser import HTMLParser
from time import sleep
import ssl
import csv

class MyHTMLParser(HTMLParser):
    eth_string ="Wired Devices"
    string_2g = "2.4G Wireless Devices (Wireless intruders also show up here)"
    string_5g = "5G Wireless Devices (Wireless intruders also show up here)"
    def __init__(self): 
        HTMLParser.__init__(self)
        self.row=[]
        self.devices_eth = []
        self.devices=[];
        self.devices_5g = []
        self.current_tag = ''
        self.trFound=False
        self.freq=0
        

    def handle_starttag(self,tag,attrs):
        self.current_tag=tag
        if tag == 'tr':
            self.trFound=True;
            
       
    def handle_endtag(self, tag):
        if tag == 'tr':
            #print("Encountered an end tag :", tag, " at frequency", self.freq)
            self.trFound=False;
            if self.freq == 1:
                self.devices_eth.append(self.row);
            elif self.freq == 2:
                self.devices.append(self.row);
            elif self.freq == 3:
                self.devices_5g.append(self.row);
                
            self.row=[];


    def handle_data(self, data):
        if ((self.current_tag == 'span' and data !="Refresh") or self.current_tag == 'b') and data.strip():
            if data == MyHTMLParser.eth_string or data == MyHTMLParser.string_2g or data == MyHTMLParser.string_5g:
                self.freq += 1;
            self.row.append(data)
        
    def get_eth(self):
        return self.devices_eth
    
    def get_devices(self):
        return self.devices

    def get_5g(self):
        return self.devices_5g

h1 = HTTPSConnection('ROUTER_IP, 
                     8443,
                     context = ssl._create_unverified_context() 
) 

headers= {
    "Host": "ROUTER_IP:8443",
    "User-Agent": "YOUR_AGENT",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Authorization": "Basic (replace this with a base64 encode of "username:password")",
    "Connection": "keep-alive",
    "Referer": "https://ROUTER_IP:8443/",
    "Upgrade-Insecure-Requests": "1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}
print("Sending request to the server to get cookie (we might not need one)");
h1.request('GET','/',headers=headers);
res = h1.getresponse();
if res.getheader('set-cookie'):
    cookie = res.getheader('set-cookie')
    print(cookie)
    headers['Cookie']=cookie
    print("Got cookie ;)");

print("sending request to DEV_device2.html page");
h1.request('GET','/DEV_device2.htm',headers=headers) 
res = h1.getresponse();

# OK, we're finally done getting the data :) 

data = res.read()

parser = MyHTMLParser()


parser.feed(data.decode('ascii'));
my_eth=parser.get_eth();
my_devices=parser.get_devices();
my_5g=parser.get_5g();
my_eth = filter(None, my_eth);
my_devices=filter(None,my_devices);
my_5g=filter(None,my_5g);
print('#' * 80);
for row in my_eth:
    counter=0
    for col in row:
        counter+=1;
        

        print(col.strip(), end = "")
        if counter < len(row):
            print(", ",end="");
    print()

print("#" * 80);
print()
print('#' * 80);
for row in my_devices:
    counter=0
    if len(row) < 5 and len(row) > 1:
        row.insert(0,"--");
    for col in row:
        counter+=1;
        if counter == 1:
            print("%15s" % col.strip(), end = "");
        else:
            print(col.strip(), end = "");
        if counter < len(row):
            print(", ",end="");
    print()

print("#" * 80);
print()
print('#' * 80);
for row in my_5g:
    counter=0
    if len(row) < 5 and len(row) > 1:
        row.insert(0,"--");
    for col in row:
        counter+=1;
        if counter == 1:
            print("%15s" % col.strip(), end = "");
        else:
            print(col.strip(), end = "");
        if counter < len(row):
            print(", ",end="");
    print()

print("#" * 80);
