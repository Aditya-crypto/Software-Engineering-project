def CreateList():
	with open('NFSdata.txt') as f:
		content = f.readline()
		content = content.rstrip("\n")
                nas_info = content.split(";")
       return nas_info
