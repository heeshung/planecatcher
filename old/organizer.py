filetoopen=input()
f = open(filetoopen,"r")
w = open("org","a+")

hexcache=[]
for line in f:
	if (any(line[12:18] in x for x in hexcache)==False):
		hexcache.append(line[12:18])
		w.write(line)
		print line[30:36]
f.close()
w.close()
