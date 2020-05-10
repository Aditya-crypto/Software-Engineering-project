# Reading database.txt file from nfs and storing the contents in content list
def MapBuilder():
	with open('database.txt') as f:
		content = f.read().splitlines()   

        # creating a dictionary to map camera id's with nearest police stations
        m = dict()
        for i in range(len(content)):
		cam_id = content[i].split(':')
                m[int(cam_id[0])] = list()
                nearby_stations = cam_id[1].split('||')
                for i in range(len(nearby_stations)):
			m[int(cam_id[0])].append(nearby_stations[i])
	return m

# Reading location.txt file from nfs and storing the contents in content list
def LocationMapBuilder():
	with open('location.txt') as f:
		content = f.read().splitlines()   

	# creating a dictionary to map camera id's with their location
	m = dict()
	for i in range(len(content)):
		cam_id = content[i].split(':')
		m[int(cam_id[0])] = cam_id[1]
	return m

def CreateList():
	with open('NFSdata.txt') as f:
		content = f.readline()
		content = content.rstrip("\n")
                nfs_info = content.split(";")
       return nfs_info
