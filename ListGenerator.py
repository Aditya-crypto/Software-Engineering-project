def CreateList():
	with open('NAS_data.txt') as f:
		content = f.readline()
		content = content.rstrip("\n")
                nas_info = content.split(";")
       return nas_info
