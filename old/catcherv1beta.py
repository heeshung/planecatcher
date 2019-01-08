import sys,time,requests
from daemon import Daemon

class catcher(Daemon):
	def run(self):
		def hexdecoder(hexcode):
			setzs=[0x008011,676,26,"ZS-",0,0x00c4b8]
			setfg=[0x390000,1024,32,"F-G",0,0x396739]
			setfh=[0x398000,1024,32,"F-H",0,0x39e739]
			setdaa=[0x3c4421,1024,32,"D-A",0,0x3c7f5a]
			setdab=[0x3c0001,676,26,"D-A",10140,0x3c1d0c]
			setdba=[0x3c8421,1024,32,"D-B",0,0x3cbf5a]
			setdbb=[0x3c2001,676,26,"D-B",10140,0x3c3d0c]
			setdc=[0x3cc000,676,26,"D-C",0,0x3d04a7]
			setde=[0x3d04a8,676,26,"D-E",0,0x3d494f]
			setdf=[0x3d4950,676,26,"D-F",0,0x3d8df7]
			setdg=[0x3d8df8,676,26,"D-G",0,0x3dd29f]
			setdh=[0x3dd2a0,676,26,"D-H",0,0x3e1747]
			setdi=[0x3e1748,676,26,"D-I",0,0x3e5bef]
			setoo=[0x448421,1024,32,"OO-",0,0x44eb5a]
			setcf=[0xc00001,676,26,"C-F",0,0xc044a8]
			setcg=[0xc044a9,676,26,"C-G",0,0xc08950]
			setci=[0xc08951,676,26,"C-I",0,0xc0cdf8]
			setoy=[0x458421,1024,32,"OY-",0,0x45eb5a]
			setoh=[0x460000,676,26,"OH-",0,0x4644a7]
			setsx=[0x468421,1024,32,"SX-",0,0x46eb5a]
			setcs=[0x490421,1024,32,"CS-",0,0x496b5a]
			setyr=[0x4a0421,1024,32,"YR-",0,0x4a6b5a]
			settc=[0x4b8421,1024,32,"TC-",0,0x4beb5a]
			setjy=[0x740421,1024,32,"JY-",0,0x746b5a]
			setap=[0x760421,1024,32,"AP-",0,0x766b5a]
			set9v=[0x768421,1024,32,"9V-",0,0x76eb5a]
			setyk=[0x778421,1024,32,"YK-",0,0x77eb5a]
			setvh=[0x7c0000,1296,36,"VH-",0,0x7c822d]
			setlv=[0xe01041,4096,64,"LV-",0,0xe1a69a]


			mappings=[setzs,setfg,setfh,setdaa,setdab,setdba,setdbb,setdc,setde,setdf,setdg,setdh,setdi,setoo,setcf,setcg,setci,setoy,setoh,
			setsx,setcs,setyr,settc,setjy,setap,set9v,setyk,setvh,setlv]

			#regrange order: N-Number,RA,CU,HL1,HL2,HL3,JA
			regrange=[0xa00001,0xadf7c7,0x140000,0x1586a0,0x0b03e8,0x0b07d0,0x71ba00,0x71bf99,0x71c000,0x71c099,0x71c200,0x71c299,0x840001,0x8781cf]

			if (regrange[0] <= hexcode <= regrange[1]):

				alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ'

				offset = hexcode-10485761

				reg="N"

				dig1=int(offset/101711)+1
				reg+=str(dig1)
				offset = offset%101711

				if (offset>600):
					offset-=601
					dig2=int(offset/10111)
					reg+=str(dig2)
					offset = offset%10111


				if (offset>600):
					offset-=601
					dig3=int(offset/951)
					reg+=str(dig3)
					offset=offset%951



				if (offset>600):
					offset-=601
					dig4=int(offset/35)
					reg+=str(int(round(dig4)))
					offset=offset%35
					if (offset>0):
						if (offset<=24):
							reg+=alphabet[offset-1]
						else:
							offset-=25
							reg+=str(int(round(offset)))


				elif (offset<=600 and offset >0):
					offset-=1
					alphaindex1 = int(offset/25)
					alphaindex2 = offset%25
					reg+=alphabet[alphaindex1]
					if (alphaindex2>0):
						alphaindex2-=1
						reg+=alphabet[alphaindex2]

				return reg

			elif (regrange[2]<=hexcode<=regrange[3] or regrange[4]<=hexcode<=regrange[5]):
				if (regrange[2]<=hexcode<=regrange[3]):
					numpre="RA-"
					numstart=regrange[2]
					numfirst=0
				else:
					numpre="CU-T"
					numstart=regrange[4]
					numfirst=1000
				reg=numpre+str(hexcode-numstart+numfirst)
				return reg

			elif(regrange[6]<=hexcode<=regrange[11]):
				if (regrange[6]<=hexcode<=regrange[7]):
					reg="HL"+str(hex(hexcode-0x71ba00+0x7200))[2:]
				elif(regrange[8]<=hexcode<=regrange[9]):
					reg="HL"+str(hex(hexcode-0x71c000+0x8000))[2:]
				elif(regrange[10]<=hexcode<=regrange[11]):
					reg="HL"+str(hex(hexcode-0x71c200+0x8200))[2:]
				return reg

			elif(regrange[12]<=hexcode<=regrange[13]):
				limalphabet='ABCDEFGHJKLMNPQRSTUVWXYZ'
				offset=hexcode-0x840000
				reg="JA"

				dig1=int(offset/22984)
				if (dig1<0 or dig1>9):
					return 0

				reg+=str(dig1)
				offset=offset%22984

				dig2=int(offset/916)
				if (dig2<0 or dig2>9):
					return 0

				reg+=str(dig2)
				offset=offset%916

				if (offset<340):
					dig3=int(offset/34)
					reg+=str(dig3)
					offset=offset%34

					if (offset<10):
						return reg+str(offset)
					else:
						offset-=10
						return reg+limalphabet[offset]
				else:
					offset-=340
					let3=int(offset/24)
					return reg+limalphabet[let3]+limalphabet[offset%24]

			else:
				alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
				for a in range(len(mappings)):
					if (mappings[a][0]<=hexcode<=mappings[a][5]):
						offset = hexcode-mappings[a][0]+mappings[a][4]
						vara=int(offset/mappings[a][1])
						offset=offset%mappings[a][1]
						varb=int(offset/mappings[a][2])
						offset=offset%mappings[a][2]
						varc=offset
						if (vara<0 or varb<0 or varc<0 or vara>=26 or varb>=26 or varc>=26):
							return 0
						else:
							reg=mappings[a][3]+alphabet[vara]+alphabet[varb]+alphabet[varc]
							return reg
				return 0


		searchstr="flight"
		airlines=["GGT","EDU","PWA","CWG","VET","GJE","ABD","MLN","DRL","REN","AXQ","NEW","NOJ","MMD","PEG",
		"NAX","WGT","EDG","CLU","NJE","NSH","GTI","SDU","WIG","LOF","JIA","GJS","EJA","ICE","YZR","TOM","RSP",
		"RIX","LJY","JAS","FTH","IFA","SVL","EDC","DCM","ASH","UPS","UAE","AFR","TCX","ACA","SKV","AFL","TSC",
		"JZA","ROU","UJC","EJM","OPT","CSN","CES","CAL","CCA","EIN","AIC","AUA","BAW","CPA","ELY","EWG","BSK",
		"ETH","DLH","IBK","NRS","DJT","TAI","POE","IBE","BOS","SAS","SWR","TAP","VIR","WOW","SIA","SKV","CJT",
		"BOX","PAC","SOO","DHK","BCS","WJA","ARG","AMX","SLI","AEA","ISS","ASL","AZA","ANA","AAR","AVA","ONE",
		"LRC","AHY","BEL","BWA","CAY","CMP","MSR","ETD","EVA","FIN","CHH","HAL","AIJ","JAL","KLM","KQA","KAL",
		"KAC","TAM","LAN","LNE","LOT","PAL","QFA","QTR","RJA","RAM","SVA","SAA","SCX","TAE","TCX","THY","AUI",
		"UZB","VIV","VOI","VOC","CXA","XLF","CAO","AZQ","NCA","CLX","ICL","XOJ","VJT","LXJ","WWI","TWY","HRT",
		"GTH","ECJ","ASP","GAJ","COL","TMC","LTD","CNK","GPD","COL","PRD","DPJ","PJC","JTL","SWG","FWK","ERY",
		"JME","WSN","FSY","GRN","CST","TAY","XSR","TFF","GEC","RLI","XLS","BVR","LXJ","MHV","CFG","VLZ","SIO",
		"LDX","LXG","DSO"]


		desiredregs=["N718BA","N747BC","N780BA","N249BA","N367HP","N80991","N851TB"]
		desiredairlines=["OAE","WWW"]

		planecache=[]
		dayhold=time.strftime("%Y%m%d")
		#startsuccess = requests.post('https://api.pushover.net/1/messages.json', data = {'token':'asgznvqc8fus68yzu9gmhhepe23rde','user':'uybm1se7j935kr5cxg8m7yc3gjq61k','message':'Started successfully.','title':'Planecatcher'})
		while 1:
			f = open("/run/dump1090-fa/aircraft.json","r")
			#iterate through raw lines
			for line in f:
				#find lines with flight
				if (line.find(searchstr)!=-1):
					desiredairline=False
					desiredreg=False
					regtype="NODECODE"
					hasregistration=False
					process=True
					hexrawinput="0x"+line[12:18]
					#check hex validity
					try:
						hexinput=int(hexrawinput,16)
					except:
						continue

					#find aircraft registration
					try:
						nreg=hexdecoder(hexinput)
					except:
						continue
					#check if registration can be found
					if (nreg!=0):
						hasregistration=True
					#check for desired airline
					if (any(line[30:33] in g for g in desiredairlines)==True):
						desiredairline=True
					#check for desired registration
					if (hasregistration==True):
						if (any(nreg in s for s in desiredregs)==True):
							desiredreg=True
					#filter out N and C and common airlines
					if (desiredairline==False and desiredreg==False):
						if (hasregistration==True):
							if (nreg[0]=="N" or nreg[0]=="C" or any(line[30:33] in n for n in airlines)==True):
								process=False
						elif (any(line[30:33] in n for n in airlines)==True):
							process=False
					if (process==True):
						timestr = time.strftime("%Y%m%d")
						wrf = open("/root/planecatcher/archive/"+timestr+"-raw.dat","a+")
						wrf.write(line)
						wrf.close()
						#flush planecache when new day
						if (timestr!=dayhold):
							planecache=[]
							dayhold=timestr
						#if not in planecache add to unique flights
						if (any(line[12:18] in x for x in planecache)==False):
							planecache.append(line[12:18])
							orgf = open("/root/planecatcher/archive/"+timestr+"-flights.dat","a+")
							pushurl = "https://flightaware.com/live/modes/"+line[12:18]+"/redirect"
							#check if flight is blank
							if (line[30:38].isspace()==True):
								if (hasregistration==True):
									pushmessage = time.strftime("%H:%M:%S")+" "+line[12:18]+" ("+nreg+") "+"\n"
								else:
									pushmessage = time.strftime("%H:%M:%S")+" "+line[12:18]+"\n"
								hexpush = requests.post('https://api.pushover.net/1/messages.json', data = {'token':'asgznvqc8fus68yzu9gmhhepe23rde','user':'uybm1se7j935kr5cxg8m7yc3gjq61k','message':pushmessage,'title':'Planecatcher','priority':'-1','url_title':'View on FlightAware','url':pushurl})
								orgf.write(pushmessage)
							else:
								if (hasregistration==True):
									pushmessage = time.strftime("%H:%M:%S")+" "+line[30:38]+" ("+nreg+")"+"\n"
								else:
									pushmessage = time.strftime("%H:%M:%S")+" "+line[30:38]+" ("+line[12:18]+")"+"\n"
								flightpush = requests.post('https://api.pushover.net/1/messages.json', data = {'token':'asgznvqc8fus68yzu9gmhhepe23rde','user':'uybm1se7j935kr5cxg8m7yc3gjq61k','message':pushmessage,'title':'Planecatcher','priority':'-1','url_title':'View on FlightAware','url':pushurl})
								orgf.write(pushmessage)
							orgf.close()
			f.close()
			time.sleep(2)

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
