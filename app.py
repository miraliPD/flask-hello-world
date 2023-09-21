import json
import time
from flask import Flask
import requests
app = Flask(__name__)


def electro():
    l = []
    server_list = json.loads(requests.get("https://elcdn.ir/app/servers.json", headers={"User-Agent": ""}).content.replace(b'\n', b'').replace(b',]', b']'))
    link_api = json.loads(requests.get("https://wg.elcdn.ir/getWGKey", headers={"User-Agent": ""}).content.replace(b'\n', b''))
    for conf in server_list:
        link_pub = json.loads(requests.get(conf["configLink"], headers={"User-Agent": ""}).content.replace(b'\n', b''))
        name = conf["name"].strip().split(" ")[0] + ".conf"
        AllowedIPs = link_pub['routes']
        AllowedIPs = AllowedIPs.replace(",,",",")
        AllowedIPs = AllowedIPs if AllowedIPs[len(AllowedIPs)-1] != "," else AllowedIPs[0:len(AllowedIPs)-1]
        base = "[Interface]\n"
        base += f"PrivateKey = {link_api['private_key']}\n"
        base += f"Address = {link_api['ip']}\n"
        base += f"DNS = {link_pub['dns']}\n\n"
        base += "[Peer]\n"
        base += f"PublicKey = {link_pub['publickey']}\n"
        base += f"PresharedKey = {link_api['psk']}\n"
        base += f"Endpoint = {link_pub['endpoint']}\n"
        base += f"AllowedIPs = {AllowedIPs}\n"
        l.append({"name": name , "data": base})
    if server_list:
        return l
    else:
        return False


def radar():
    list = []
    l = []
    setting = requests.get("https://gw.radar.game/getSettings", headers={"User-Agent": ""}).json()
    server_list = requests.get("https://gw.radar.game/list", headers={"User-Agent": ""}).json()
    AllowedIPs = setting["result"]["routes"]
    AllowedIPs = AllowedIPs.replace(",,",",")
    AllowedIPs = AllowedIPs if AllowedIPs[len(AllowedIPs)-1] != "," else AllowedIPs[0:len(AllowedIPs)-1]
    for server in server_list["result"]:
        req = requests.get(server['domain'], headers={"User-Agent": ""}).json()
        name = server['domain'].split("://")[1].split(".")[0] + ".conf"
        config = {
            'name': name,
            'PrivateKey':req["result"]["private_key"],
            'Address':req["result"]["ip"],
            'DNS':server["dns"][0],
            'PublicKey':req["result"]["settings"]["public_key"],
            'PresharedKey':req["result"]["psk"],
            'Endpoint':req["result"]["settings"]["endpoint"],
            'AllowedIPs':AllowedIPs
        }
        list.append(config)
       
     
    for conf in list:
        base = "[Interface]\n"
        base += f"PrivateKey = {conf['PrivateKey']}\n"
        base += f"Address = {conf['Address']}\n"
        base += f"DNS = {conf['DNS']}\n\n"
        base += "[Peer]\n"
        base += f"PublicKey = {conf['PublicKey']}\n"
        base += f"PresharedKey = {conf['PresharedKey']}\n"
        base += f"Endpoint = {conf['Endpoint']}\n"
        base += f"AllowedIPs = {conf['AllowedIPs']}\n"
        l.append({"name": conf["name"], "data": base})
    if list:
        return l
    else:
        return False






@app.route("/")
def home():
    
    return f'<center><h1 style="background:black;"><a style="color:white" href="/loading1">استخراج کانفیگ الکترا</a></h1><hr><h1 style="background:black;"><a style="color:white" href="/loading2">استخراج کانفیگ رادار</a></h1><h3 style="margin-top:20px;background:darkgreen;color:red">Coded by MiraliPD</h3></center>'



@app.route("/get1")
def get1():
    if electro() != False:
        data = '<h1 style="background:black;color:white;padding:8px">کانفیگ الکترا</h1><hr>'
        for conf in electro():
            data += f'<a style="font-size:15px;font-weight:bold" href="data:text/plain;charset=utf-8,{conf["data"]}" download="{conf["name"]}"> {conf["name"]} - دانلود کانفیگ</a><br>'
        return f'<center>{data}<hr><h1 style="background:black;"><a style="color:white" href="/">برگشت</a></h1></center>'
    else:
        return "Error"



@app.route("/get2")
def get2():
    if radar() != False:
        data = '<h1 style="background:black;color:white;padding:8px">کانفیگ رادار</h1><hr>'
        for conf in radar():
            data += f'<a style="font-size:15px;font-weight:bold" href="data:text/plain;charset=utf-8,{conf["data"]}" download="{conf["name"]}"> {conf["name"]} - دانلود کانفیگ</a><br>'
        return f'<center>{data}<hr><h1 style="background:black;"><a style="color:white" href="/">برگشت</a></h1></center>'
    else:
        return "Error"



@app.route("/loading1")
def loading1():
    l = '<h1 style="color: red;position: absolute;transform: translate(-50%, -50%);left: 50%;top: 50%;padding: 25px;border: 1px solid;border-radius: 15px;box-shadow: -3px 4px 3px 0px #aaa;">... لطفا صبر کنید</h1>'
    return f"{l} <script>var timer = setTimeout(function() {{window.location='/get1'}}, 10);</script>" 

@app.route("/loading2")
def loading2():
    l = '<h1 style="color: red;position: absolute;transform: translate(-50%, -50%);left: 50%;top: 50%;padding: 25px;border: 1px solid;border-radius: 15px;box-shadow: -3px 4px 3px 0px #aaa;">... لطفا صبر کنید</h1>'
    return f"{l} <script>var timer = setTimeout(function() {{window.location='/get2'}}, 10);</script>" 





if __name__ == '__main__':
   app.run()
