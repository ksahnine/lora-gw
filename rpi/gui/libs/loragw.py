__author__  = "Kadda SAHNINE"
__contact__ = "ksahnine@gmail.com"
__license__ = 'GPL v3'

import threading 
import logging 
import subprocess 
import time 
 
class LoRaGateway(threading.Thread): 
    def __init__(self, logLevel = logging.DEBUG): 
        threading.Thread.__init__(self) 
        self.daemon = True 
        self._stopevent = threading.Event() 
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()
        self.logger.setLevel(logLevel)

    def run(self): 
        self.running = True
	startCmd = "nohup /home/pi/repo/rpi/bin/start-lora-gw.sh & echo $! > /tmp/loragw.pid"
	ps = subprocess.Popen(startCmd, shell=True, stdout=subprocess.PIPE)
        self.logger.log(logging.DEBUG, "Demarrage passerelle LoRa")
        for line in iter(ps.stdout.readline,''):
            # sortie standard
            l = line.rstrip()
            self.logger.log(logging.DEBUG, "%s" % (l))

    def stop(self): 
 	stopCmd  = "sudo pkill -TERM -P `cat /tmp/loragw.pid` && rm -f /tmp/loragw.pid"
	ps = subprocess.Popen(stopCmd, shell=True, stdout=subprocess.PIPE)
        out = ps.stdout.read()
        ps.stdout.close()
        ps.wait()
        self.logger.log(logging.DEBUG, "Arret passerelle LoRa")
        self._stopevent.set()
