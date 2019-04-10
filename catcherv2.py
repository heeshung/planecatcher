#PlaneCatcher v2.0 created by Heeshung

#Aircraft registration calculation algorithms ported to Python from https://github.com/openskynetwork/dump1090-hptoa/blob/master/public_html/registrations.js
#Algorithms licensed under GPL, v2 or later -  Copyright (C) 2012 by Salvatore Sanfilippo <antirez@gmail.com>

#Daemon script ported from https://web.archive.org/web/20160305151936/http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/


import sys,time,requests
from daemon import Daemon

class catcher(Daemon):
	def run(self):
		def findcountry(hexcode):
			countries=["USCiv","SE","IR","ZW","GM","CH","IL","MZ","BF","TR","JO","ZA","ST",
			"YU","LB","EG","DZ","CY","MY","LY","BS","IE","PH","MA","BB","IS","PK","TN",
			"BZ","LU","SG","BW","CO","MT","LK","BI","CR","MC","SY","CM","CU","SM","CN",
			"KM","SV","AU","CG","GT","AL","IN","CI","GY","HR","JP","GA","HT","LV","TH",
			"ET","HN","LT","VN","GQ","VC","MD","YE","GH","JM","SK","BH","GN","NI","SI",
			"BN","GW","PA","UZ","AE","LS","DO","UA","SB","KE","TT","BY","PG","LR","SR",
			"EE","TW","MG","AG","MK","ID","MW","GD","BA","MV","MX","GE","MH","ML","VE",
			"TJ","CK","MR","RU","AM","AS","MU","USMil","NE","NA","AZ","NA","ER","KG","CA",
			"UG","TM","NZ","QA","IT","FJ","CF","ES","BT","NR","RW","FR","FM","LC","SN",
			"DE","MN","TO","SC","UK","KZ","KI","SL","AT","PW","VU","SO","BE","AF","SZ",
			"BG","BD","AR","SD","DK","MM","BR","TZ","FI","KW","CL","TD","GR","LA","EC",
			"TG","HU","NP","PY","ZM","NO","OM","PE","CD","NL","KH","UY","AO","PL","SA",
			"BO","BJ","PT","KR","CV","CZ","KP","DJ","RO","IQ"]
		
			hexranges=[0xA00000,0xADF7C8,0x4A8000,0x4AFFFF,0x730000,0x737FFF,0x004000,0x0043FF,0x09A000,0x09AFFF,0x4B0000,
			0x4B7FFF,0x738000,0x73FFFF,0x006000,0x006FFF,0x09C000,0x09CFFF,0x4B8000,0x4BFFFF,0x740000,0x747FFF,0x008000,0x00FFFF,
			0x09E000,0x09E3FF,0x4C0000,0x4C7FFF,0x748000,0x74FFFF,0x010000,0x017FFF,0x0A0000,0x0A7FFF,0x4C8000,0x4C83FF,0x750000,
			0x757FFF,0x018000,0x01FFFF,0x0A8000,0x0A8FFF,0x4CA000,0x4CAFFF,0x758000,0x75FFFF,0x020000,0x027FFF,0x0AA000,0x0AA3FF,
			0x4CC000,0x4CCFFF,0x760000,0x767FFF,0x028000,0x02FFFF,0x0AB000,0x0AB3FF,0x4D0000,0x4D03FF,0x768000,0x76FFFF,0x030000,
			0x0303FF,0x0AC000,0x0ACFFF,0x4D2000,0x4D23FF,0x770000,0x777FFF,0x032000,0x032FFF,0x0AE000,0x0AEFFF,0x4D4000,0x4D43FF,
			0x778000,0x77FFFF,0x034000,0x034FFF,0x0B0000,0x0B0FFF,0x500000,0x5003FF,0x780000,0x7BFFFF,0x035000,0x0353FF,0x0B2000,
			0x0B2FFF,0x7C0000,0x7FFFFF,0x036000,0x036FFF,0x0B4000,0x0B4FFF,0x501000,0x5013FF,0x800000,0x83FFFF,0x038000,0x038FFF,
			0x0B6000,0x0B6FFF,0x501C00,0x501FFF,0x840000,0x87FFFF,0x03E000,0x03EFFF,0x0B8000,0x0B8FFF,0x502C00,0x502FFF,0x880000,
			0x887FFF,0x040000,0x040FFF,0x0BA000,0x0BAFFF,0x503C00,0x503FFF,0x888000,0x88FFFF,0x042000,0x042FFF,0x0BC000,0x0BC3FF,
			0x504C00,0x504FFF,0x890000,0x890FFF,0x044000,0x044FFF,0x0BE000,0x0BEFFF,0x505C00,0x505FFF,0x894000,0x894FFF,0x046000,
			0x046FFF,0x0C0000,0x0C0FFF,0x506C00,0x506FFF,0x895000,0x8953FF,0x048000,0x0483FF,0x0C2000,0x0C2FFF,0x507C00,0x507FFF,
			0x896000,0x896FFF,0x04A000,0x04A3FF,0x0C4000,0x0C4FFF,0x508000,0x50FFFF,0x897000,0x8973FF,0x04C000,0x04CFFF,0x0C6000,
			0x0C6FFF,0x510000,0x5103FF,0x898000,0x898FFF,0x050000,0x050FFF,0x0C8000,0x0C8FFF,0x511000,0x5113FF,0x899000,0x8993FF,
			0x054000,0x054FFF,0x0CA000,0x0CA3FF,0x512000,0x5123FF,0x8A0000,0x8A7FFF,0x058000,0x058FFF,0x0CC000,0x0CC3FF,0x513000,
			0x5133FF,0x05A000,0x05A3FF,0x0D0000,0x0D7FFF,0x514000,0x5143FF,0x900000,0x9003FF,0x05C000,0x05CFFF,0x0D8000,0x0DFFFF,
			0x515000,0x5153FF,0x901000,0x9013FF,0x05E000,0x05E3FF,0x100000,0x1FFFFF,0x600000,0x6003FF,0x902000,0x9023FF,0x060000,
			0x0603FF,0xADF7C9,0xAFFFFF,0x062000,0x062FFF,0x201000,0x2013FF,0x600800,0x600BFF,0x064000,0x064FFF,0x202000,0x2023FF,
			0x601000,0x6013FF,0xC00000,0xC3FFFF,0x068000,0x068FFF,0x601800,0x601BFF,0xC80000,0xC87FFF,0x06A000,0x06A3FF,0x300000,
			0x33FFFF,0xC88000,0xC88FFF,0x06C000,0x06CFFF,0x340000,0x37FFFF,0x680000,0x6803FF,0xC8A000,0xC8A3FF,0x06E000,0x06EFFF,
			0x380000,0x3BFFFF,0x681000,0x6813FF,0xC8C000,0xC8C3FF,0x070000,0x070FFF,0x3C0000,0x3FFFFF,0x682000,0x6823FF,0xC8D000,
			0xC8D3FF,0x074000,0x0743FF,0x400000,0x43FFFF,0x683000,0x6833FF,0xC8E000,0xC8E3FF,0x076000,0x0763FF,0x440000,0x447FFF,
			0x684000,0x6843FF,0xC90000,0xC903FF,0x078000,0x078FFF,0x448000,0x44FFFF,0x700000,0x700FFF,0x07A000,0x07A3FF,0x450000,
			0x457FFF,0x702000,0x702FFF,0xE00000,0xE3FFFF,0x07C000,0x07CFFF,0x458000,0x45FFFF,0x704000,0x704FFF,0xE40000,0xE7FFFF,
			0x080000,0x080FFF,0x460000,0x467FFF,0x706000,0x706FFF,0xE80000,0xE80FFF,0x084000,0x084FFF,0x468000,0x46FFFF,0x708000,
			0x708FFF,0xE84000,0xE84FFF,0x088000,0x088FFF,0x470000,0x477FFF,0x70A000,0x70AFFF,0xE88000,0xE88FFF,0x08A000,0x08AFFF,
			0x478000,0x47FFFF,0x70C000,0x70C3FF,0xE8C000,0xE8CFFF,0x08C000,0x08CFFF,0x480000,0x487FFF,0x70E000,0x70EFFF,0xE90000,
			0xE90FFF,0x090000,0x090FFF,0x488000,0x48FFFF,0x710000,0x717FFF,0xE94000,0xE94FFF,0x094000,0x0943FF,0x490000,0x497FFF,
			0x718000,0x71FFFF,0x096000,0x0963FF,0x498000,0x49FFFF,0x720000,0x727FFF,0x098000,0x0983FF,0x4A0000,0x4A7FFF,0x728000,
			0x72FFFF]
		
			for a in range(0,len(hexranges),2):
				if (hexranges[a]<hexcode<hexranges[a+1]):
					return countries[a/2]
			return "nocountry"
		
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
		filteredairlines=["GGT","EDU","PWA","CWG","VET","GJE","ABD","MLN","DRL","REN","AXQ","NEW","NOJ","MMD",
		"NAX","WGT","EDG","CLU","NJE","NSH","GTI","SDU","WIG","LOF","JIA","GJS","EJA","ICE","YZR","TOM","RSP",
		"RIX","LJY","JAS","FTH","IFA","SVL","EDC","DCM","ASH","UPS","UAE","AFR","TCX","ACA","SKV","AFL","TSC",
		"JZA","ROU","UJC","EJM","OPT","CSN","CES","CAL","CCA","EIN","AIC","AUA","BAW","CPA","ELY","EWG","BSK",
		"ETH","DLH","IBK","NRS","DJT","TAI","POE","IBE","BOS","SAS","SWR","TAP","VIR","WOW","SIA","CJT","NWS",
		"BOX","PAC","SOO","DHK","BCS","WJA","ARG","AMX","SLI","AEA","ISS","ASL","AZA","ANA","AAR","AVA","ONE",
		"LRC","AHY","BEL","BWA","CAY","CMP","MSR","ETD","EVA","FIN","CHH","HAL","AIJ","JAL","KLM","KQA","KAL",
		"KAC","TAM","LAN","LNE","LOT","PAL","QFA","QTR","RJA","RAM","SVA","SAA","SCX","TAE","THY","AUI","AMQ",
		"UZB","VIV","VOI","VOC","CXA","XLF","CAO","AZQ","NCA","CLX","ICL","XOJ","VJT","WWI","TWY","HRT","TFL",
		"GTH","ECJ","ASP","GAJ","TMC","LTD","CNK","GPD","COL","PRD","DPJ","PJC","JTL","SWG","FWK","ERY","PEG",
		"JME","WSN","FSY","GRN","CST","TAY","XSR","TFF","GEC","RLI","XLS","BVR","LXJ","MHV","CFG","VLZ","SIO",
		"LDX","LXG","DSO","ICV","AOJ","ADN","VCG","JAF","LEA","JEF","GMA","IJM","SVW","EXU","GES","VCN","DCS",
		"MLM","ABW","ANZ","EAU","RCH","PAT","EXS","KNT","CAZ","KCE","EDW","NDR","KFE","KTK","SHE","GLJ","JET",
		"EAV","PNC","NDL","JCL","AYY","FYL","ULC","FEX","ABP","JDI","TEU","FPG","MJF","EUW","BMW","RZO","PBR",
		"JTS","DCW","MPH","AHO","DGX","EFF","CLF","IXR","QQE","NOS","CPI","DGX","QAJ","LMJ","TBJ","AAB","GCK"]
		filteredcountries=["USCiv","USMil"]
		filteredhexcodes=["780926","7101e0","0c4146","0aa004","0aa001","0d8137","780979","564795","500141","60698b",
		"780705","293d7c","0c414f","0c4152","0c414c","0c414b","0c4153","0c4154","0d0aea","5000ce","5000e6","500141",
		"50012a","50012a","780043","43ec0e","7103e8","0ac379","0d823b","5000c0","500155","7c48a2","484349","c012c7",
		"4d21d8","50016b","43eb77","5000f1","0d02f7"]
		
		desiredregs=["N367HP","N80991","N851TB","N8050J","N6189Q","N4468N","C-GXII","C-FWTF"]
		desiredairlines=["WWW","MPE","BOE","RRR"]
		desiredhexcodes=["adfdf9","adfdf8","ae1170","ae020d"]
		
		planecache=[]
		allplanecache=[]
		dayhold=time.strftime("%Y%m%d")
		#startsuccess = requests.post('https://api.pushover.net/1/messages.json', data = {'token':'asgznvqc8fus68yzu9gmhhepe23rde','user':'uybm1se7j935kr5cxg8m7yc3gjq61k','message':'Started successfully.','title':'Planecatcher'})
		while 1:
			f = open("/run/dump1090-fa/aircraft.json","r")
			#iterate through raw lines
			for line in f:
				#find lines with flight
				if (line.find(searchstr)!=-1):
					desiredtraits=False
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
					#find country from hexcode
					try:
						hexcountry=findcountry(hexinput)
					except:
						continue
					#check if registration can be found
					if (nreg!=0):
						hasregistration=True
					#check for desired traits
					if ((line[30:33] in desiredairlines)==True or (line[12:18] in desiredhexcodes)==True):
						desiredtraits=True
					#check for desired registration
					if (hasregistration==True):
						if ((nreg in desiredregs)==True):
							desiredtraits=True
					#filter out specific hex codes first
					if ((line[12:18] in filteredhexcodes)==True):
						process=False

					#filter out countries and common airlines and for flights without numbers
					elif (desiredtraits==False):
						if ((hexcountry in filteredcountries)==True or (line[30:33] in filteredairlines)==True or any(char.isdigit() for char in line[30:38])==False):
							process=False
		
					
					timestr = time.strftime("%Y%m%d")
					#flush planecache when new day
					if (timestr!=dayhold):
						planecache=[]
						allplanecache=[]
						dayhold=timestr
					
					#if not in planecache add to unique flights
					if ((line[12:18] in allplanecache)==False):
						allplanecache.append(line[12:18])
						orgf = open("/root/planecatcher/archive/"+timestr+"-allflights.dat","a+")
						#check if flight is blank or is sr_icao
						if (line[30:38].isspace()==True or line[30:38]=='sr_icao"'):
							if (hasregistration==True):
								pushmessage = time.strftime("%H:%M:%S")+" "+line[12:18]+" ("+nreg+")"
							else:
								pushmessage = time.strftime("%H:%M:%S")+" "+line[12:18]
							if (hexcountry!="nocountry"):
								pushmessage+=" ["+hexcountry+"]"
							pushmessage+="\n"
							orgf.write(pushmessage)
						else:
							if (hasregistration==True):
								pushmessage = time.strftime("%H:%M:%S")+" "+line[30:38]+" ("+nreg+")"
							else:
								pushmessage = time.strftime("%H:%M:%S")+" "+line[30:38]+" ("+line[12:18]+")"
							if (hexcountry!="nocountry"):
								pushmessage+=" ["+hexcountry+"]"
							pushmessage+="\n"
							orgf.write(pushmessage)
						orgf.close()
		
					if (process==True):
						wrf = open("/root/planecatcher/archive/"+timestr+"-raw.dat","a+")
						wrf.write(line)
						wrf.close()
						
						#if not in planecache add to unique flights
						if ((line[12:18] in planecache)==False):
							planecache.append(line[12:18])
							orgf = open("/root/planecatcher/archive/"+timestr+"-flights.dat","a+")
							pushurl = "https://flightaware.com/live/modes/"+line[12:18]+"/redirect"
							#check if flight is blank or is sr_icao
							if (line[30:38].isspace()==True or line[30:38]=='sr_icao"'):
								if (hasregistration==True):
									pushmessage = time.strftime("%H:%M:%S")+" "+line[12:18]+" ("+nreg+")"
								else:
									pushmessage = time.strftime("%H:%M:%S")+" "+line[12:18]
								if (hexcountry!="nocountry"):
									pushmessage+=" ["+hexcountry+"]"
								hexpush = requests.post('https://api.pushover.net/1/messages.json', data = {'token':'asgznvqc8fus68yzu9gmhhepe23rde','user':'uybm1se7j935kr5cxg8m7yc3gjq61k','message':pushmessage,'title':'PlaneCatcher','priority':'-1','url_title':'View on FlightAware','url':pushurl})
								pushmessage+="\n"
								orgf.write(pushmessage)
							else:
								if (hasregistration==True):
									pushmessage = time.strftime("%H:%M:%S")+" "+line[30:38]+" ("+nreg+")"
								else:
									pushmessage = time.strftime("%H:%M:%S")+" "+line[30:38]+" ("+line[12:18]+")"
								if (hexcountry!="nocountry"):
									pushmessage+=" ["+hexcountry+"]"
								flightpush = requests.post('https://api.pushover.net/1/messages.json', data = {'token':'asgznvqc8fus68yzu9gmhhepe23rde','user':'uybm1se7j935kr5cxg8m7yc3gjq61k','message':pushmessage,'title':'PlaneCatcher','priority':'-1','url_title':'View on FlightAware','url':pushurl})
								pushmessage+="\n"
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
