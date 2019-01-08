def hexdecoder(hexinput):
	alphabet="ABCDEFGHJKLMNPQRSTUVWXYZ"
	hexcode="0x"+hexinput
	offset = int(hexcode,16)-10485761

	reg="N"
	dig1=int(offset/101711)+1
	reg+=str(dig1)
	offset=offset%101711

	if (offset>600):
		offset-=601
		dig2=int(offset/10111)
		reg+=str(dig2)
		offset=offset%10111

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
		if (offset<=24):
			reg+=alphabet[offset-1]
		else:
			offset-=25
			reg+=str(int(round(offset)))

	elif (offset<=600 and offset>0):
		offset-=1
		alphaindex1=int(offset/25)
		alphaindex2=offset%25
		reg+=alphabet[alphaindex1]
		if (alphaindex2>0):
			alphaindex2-=1
			reg+=alphabet[alphaindex2]

	return reg

while 1:
	hexinput=raw_input()
	print hexdecoder(hexinput)
