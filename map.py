
# Reading database.txt file from nas and storing the contents in content list
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
