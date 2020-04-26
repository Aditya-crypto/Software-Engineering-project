import kdtree

class Nearest_Police_Station:
	'''
	Function to populate a Database of nearest police stations to a camera location.
	Uses K nearest Neighbour algo to find the nearest police stations.
	Uses KD tree to prune the search space and make it faster.
	'''
	def Police_Station_DB(self):
		
		with open("C:\\Users\\ADITYA MOHAN GUPTA\\Desktop\\smai\\location.txt",newline = '') as item:
		   temp = item.read()
		   list_of_lines = temp.split('\n')

		dic = {}
		for item in list_of_lines:
		   x = item.split(':')
		   dic[int(x[0])]= float(x[2]),float(x[3])

		points = []
		query_points = []

		# Condition, just for assumption purpose. that all IDs greater than 50 are police station IDs
		
		for k in dic.keys():
			if k > 50:
				points.append(dic[k])
			else:
				query_points.append(dic[k]) 

		root = kdtree.create(points,dimensions=2)

		with open("C:\\Users\\ADITYA MOHAN GUPTA\\Desktop\\smai\\ip.txt") as item:
		   temp = item.read()
		   listt = temp.split('\n')

		ip_map = {}
		for item in listt:
		   x = item.split(':')
		   ip_map[int(x[0])]= x[1]

		nn_map = {}
		for point in query_points:
			ans = root.search_knn(point = point ,k=5,dist = None)
			nn = []
			ip_nn = []
			for i in range(5):
				print(ans)
				a = str(ans[i][0])
				start = a.find('(')
				end = a.find(')')
				temp = a[start:end+1]
				res = tuple(float(num) for num in temp.replace('(', '').replace(')', '').replace('...', '').split(', ')) 
				nn.append(res)
			for j in nn:
				key = list(dic.keys())[list(dic.values()).index(j)]
				ip_nn.append(ip_map[key])
				nn_map[(list(dic.keys())[list(dic.values()).index(point)])] = ip_nn   

		f = open("db.txt","w+")
		map_keys = nn_map.keys()
		for i in map_keys:
		  f.write(str(i) + ":" + ((listt[i-1]).split(':'))[1])
		  li = nn_map[i]
		  f.write(li[0])
		  f.write("||" + li[1])
		  f.write("||" + li[2])
		  f.write("||" + li[3])
		  f.write("||" + li[4])
		  f.write("\n")  
		f.close()


