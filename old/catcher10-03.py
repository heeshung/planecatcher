import sys,time,requests
from daemon import Daemon

class catcher(Daemon):
	def run(self):
		str="flight"
		airlines=['flight":"000','flight":"N1','flight":"N2','flight":"N3','flight":"N4','flight":"N5','flight":"N6','flight":"N7','flight":"N8','flight":"N9',
		"AAL","NAX","DAL","FDX","UAL","JBU","ASA","SWA","NKS","WGT","EDG","CLU","NJE","NSH","GTI","SDU",
		"WIG","LOF","JIA","GJS","EJA","ICE","YZR","TOM","RSP","RIX","LJY","JAS","FTH","IFA","SVL","EDC",
		"DCM","ASH","UPS","UAE","AFR","TCX","ACA","SKV","AFL","TSC","JZA","ROU","UJC","EJM","SKW","OPT",
		"CSN","CES","CAL","CCA","EIN","AIC","AAY","AUA","BAW","CPA","ELY","EWG","BSK","ETH","DLH","IBK",
		"NRS","DJT","TAI","POE","IBE","BOS","SAS","SWR","TAP","VIR","WOW","SIA","CPZ","EDV","RPA","SKV",
		"ENY","ASQ","PDT","ASH","UCA","AWI","CJT","ABX","BOX","PAC","SOO","DHK","BCS","FFT","WJA","ARG",
		"AMX","SLI","AEA","ISS","ASL","AZA","ANA","AAR","AVA","ONE","LRC","AHY","BEL","KAP","CAP","BWA",
		"CAY","CMP","MSR","ETD","EVA","FIN","CHH","HAL","AIJ","JAL","KLM","KQA","KAL","KAC","TAM","LAN",
		"LNE","LOT","PAL","QFA","QTR","RJA","RAM","SVA","SAA","SCX","TAE","TCX","THY","AUI","UZB","VIV",
		"VOI","VOC","CXA","XLF","CAO","AZQ","NCA","CKS","CLX","ICL","XOJ","VJT","LXJ","WWI","TWY","HRT",
		"GTH","ECJ","LBQ","ASP","GAJ","COL","TMC","LTD","CNK","GPD","COL","PRD","DPJ","PJC","JTL","SWG",
		"FWK","ERY","JME","WSN","FSY","GRN","CST","TAY","XSR","TFF","GEC","RLI","XLS"]

		planecache=[]
		linecounter=0
		dayhold=time.strftime("%Y%m%d")
		#startsuccess = requests.post('https://api.pushover.net/1/messages.json', data = {'token':'asgznvqc8fus68yzu9gmhhepe23rde','user':'uybm1se7j935kr5cxg8m7yc3gjq61k','message':'Started successfully.','title':'Planecatcher'})
		while 1:
			f = open("/run/dump1090-fa/aircraft.json","r")
			#iterate through raw lines
			for line in f:
				#find lines with flight
				if (line.find(str)!=-1):
					#find flights without regular airlines
					if (any(n in line for n in airlines)==False):
						timestr = time.strftime("%Y%m%d")
						wrf = open("/root/planecatcher/archive/"+timestr+"-raw.dat","a+")
						wrf.write(line)
						wrf.close()
						#flush planecache when new day
						if (timestr!=dayhold):
							planecache=[]
							dayhold=timestr
							#testf = open("/root/planecatcher/archive/"+timestr+"newmin","a+")
							#testf.write("A")
							#testf.close()
						#if not in planecache add to unique flights
						if (any(line[12:18] in x for x in planecache)==False):
							planecache.append(line[12:18])
							orgf = open("/root/planecatcher/archive/"+timestr+"-flights.dat","a+")
							#check if flight is blank
							if (line[30:38].isspace()==True):
								pushmessage = time.strftime("%H:%M:%S")+" "+line[12:18]+"\n"
								#hexpush = requests.post('https://api.pushover.net/1/messages.json', data = {'token':'asgznvqc8fus68yzu9gmhhepe23rde','user':'uybm1se7j935kr5cxg8m7yc3gjq61k','message':pushmessage,'title':'Planecatcher','priority':'-1'})
								orgf.write(pushmessage)
							else:
								pushmessage = time.strftime("%H:%M:%S")+" "+line[30:38]+" ("+line[12:18]+")"+"\n"
								pushurl = "https://flightaware.com/live/flight/"+line[30:38]
								flightpush = requests.post('https://api.pushover.net/1/messages.json', data = {'token':'asgznvqc8fus68yzu9gmhhepe23rde','user':'uybm1se7j935kr5cxg8m7yc3gjq61k','message':pushmessage,'title':'Planecatcher','priority':'-1','url_title':'View on FlightAware','url':pushurl})
								orgf.write(pushmessage)
							orgf.close()
			f.close()
			time.sleep(5)

if __name__ == "__main__":
    daemon = catcher('/tmp/planecatcher.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
