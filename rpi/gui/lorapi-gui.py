# -*- coding: utf-8 -*-
__author__  = "Kadda SAHNINE"
__contact__ = "ksahnine@gmail.com"
__license__ = 'GPL v3'

from flask import Flask, request, render_template, url_for, send_from_directory, redirect
from flask.helpers import locked_cached_property
import subprocess

iface     = "en1"
statusCmd = "ps -eaf | grep MacOS/Safari | grep -v grep"
stopCmd   = ["killall","Safari"]
startCmd  = ["open","http://www.google.fr"]

app = Flask(__name__)

def execCmd(cmd):
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out = ps.stdout.read()
    ps.stdout.close()
    ps.wait()

    return out

def get_ip_address(ifname):
    cmd = 'ifconfig ' + ifname + ' | grep "inet " | cut -d" " -f2'
    ip = execCmd(cmd)
    return ip

def isGwUp():
    # Etat de la passerelle
    out = execCmd(statusCmd)

    status = False
    if out != "" :
        status = True
    
    return status

def startGw():
    # Demarrage de la passerelle LoRa
    cmd = startCmd
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                              stderr = subprocess.PIPE,
                              stdin  = subprocess.PIPE)
    out,err = p.communicate()

    if err != None:
        return False

    return True

def stopGw():
    # Arret de la passerelle LoRa
    cmd = stopCmd
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                              stderr = subprocess.PIPE,
                              stdin  = subprocess.PIPE)
    out,err = p.communicate()
    
    if err != None:
        return False

    return True

def wifiAddress():
    # Adresse interface WiFi
    ifname = iface
    return get_ip_address(ifname)    

def hostname():
    # Hostname
    
    return execCmd("hostname")   

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)

@app.route('/dist/<path:path>')
def send_dist(path):
    return send_from_directory('dist', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/bower_components/<path:path>')
def send_bower_components(path):
    return send_from_directory('bower_components', path)

@app.route('/')
def index():
    page = 'index'

    status = isGwUp()
    ip = wifiAddress()
    host = hostname()

    return render_template('index.html', gwUp=status, ip=ip, host=host)

@app.route('/configure')
def configure():
    page = 'configure'
    return render_template('configure.html')

@app.route('/wifi/list')
def networks():
    networks = ['Virgin', 'Free', 'Bouygues', 'SFR']
    return render_template('wifi-list.html', networks=networks)

@app.route('/wifi/connect', methods=['POST'])
def wifiConnect():
    ssid = request.form['ssid']
    password = request.form['password']
    #wifi = request.get_json(silent=True)
    #print "SSID : %s / %s" % (wifi.ssid, wifi.password)
    print "SSID : %s / %s" % (ssid, password)
    return render_template('wifi-list.html', status='OK')

@app.route('/gateway/<command>')
def gwCommand(command):
    if command.strip() == 'start':
        startGw()

    if command.strip() == 'stop':
        stopGw()

    return redirect('/')

if __name__ == '__main__':
    app.run('0.0.0.0', 8080, debug=True)
