import os
import time
from pathlib import Path
from networkx.algorithms.shortest_paths import weighted
from numpy.core.fromnumeric import size
from pyvis.network import Network
import pandas as pd

path = "/home/kali/Desktop/People/"
tagged = ""
wtagged = ""
followers = ""
followings = ""

lookupNames = []
lookupHandles = []
lookup = open("/home/kali/Documents/lookup")
for n in lookup:
    lookupNames.append(n.split(":")[0].strip())
    lookupHandles.append(n.split(":")[1].strip())


def extract(text, mode="virtual"):
	if mode == "close":
		lines = text.split("\n")
		handles = []
		for line in lines:
			try:
				handle = line.split("|")[3].encode().strip()
				if handle != "Username":
					handles.append(handle)
			except IndexError:
				nope = 0
	else:
		lines = text.split("\n")
		handles = []
		for line in lines:
			try:
				handle = line.split("|")[2].strip()
				if handle != "Username":
					handles.append(handle)
			except IndexError:
				nope = 0
	return handles


def get():
	for person in os.walk(path):
		if ("handle" in person[2]) and (Path(person[0] + '/connections').is_dir() == False):	
			file = open(person[0] + "/handle")
			handle = file.readline()
			print(handle)
			check = os.popen("cd /home/kali/tools/Instagram-Social-Dynamics && python3 main.py " + handle + " -c tagged")
			time.sleep(8)
			if check.close() is not None:
				print("skipping...")
				continue
			tagged = os.popen("cd /home/kali/tools/Instagram-Social-Dynamics && python3 main.py " + handle + " -c tagged").read()
			wtagged = os.popen("cd /home/kali/tools/Instagram-Social-Dynamics && python3 main.py " + handle + " -c wtagged").read()
			followers = os.popen("cd /home/kali/tools/Instagram-Social-Dynamics && python3 main.py " + handle + " -c followers").read()
			followings = os.popen("cd /home/kali/tools/Instagram-Social-Dynamics && python3 main.py " + handle + " -c followings").read()

			#Tagged List, offline connection
			close = extract(tagged, "close") + extract(wtagged, "close")
			close = list(dict.fromkeys(close))
			#Virtual List, only follow each other on IG, no offline connection
			virtual = extract(followers) + extract(followings)
			virtual = list(dict.fromkeys(virtual))

			os.makedirs(person[0] + "/connections", exist_ok=True)
			
			with open(person[0] + "/connections/virtual", "w") as virtualFile:
				for account in virtual:
					virtualFile.write(str(account) + "\n")
			
			with open(person[0] + "/connections/close", "w") as closeFile:
				for account in close:
					closeFile.write(str(account) + "\n")
			print("success")
			time.sleep(10)
			
def compatibility(x,y):
	# x and y are 2d-lists containing followers and followings
	# assuming connections are equal for followers and folowings
	# This function returns a compatibility score, which indicates how compatible given people x and y are.
	# it can be assumed that people are more likely to be friends with people similar to them. So if person x is friends with a friend of person y,
	# the score is higher.
	# x = [[a, c, c], [a, d]]
	xconnections = x[0] + x[1]
	yconnections = y[0] + y[1]
	
	# to intersect work with sets rather than lists
	xconnections = set(xconnections)
	yconnections = set(yconnections)
	
	common = xconnections.intersection(yconnections)
	compatibility = common/(len(xconnections) + len(yconnections))
	
	return compatibility
	
	

def map(node="real", type="real", mode="normal"):
	"""""
	node: Use real (node="real") names or the respective instagram handles (node="handle")
	"""""
	connections = []
	for person in os.walk(path):
		name = ""
		if Path(person[0] + '/connections').is_dir():
			if node == "real":
				name = os.path.basename(person[0]).encode()
			else:
				file = open(person[0] + "/handle")
				name = file.readline()
			virtual = open(person[0] + "/connections/virtual")
			close = open(person[0] + "/connections/close")
			virtualLines = virtual.readlines()
			closeLines = close.readlines()
			for line in virtualLines:
				if line.strip() in lookupHandles and line.strip() != name:
					connections.append([name, line.strip(), 1])
			for line in closeLines:
				if line.strip() in lookupHandles and line.strip() != name:
					connections.append([name, line.strip(), 10])

	df = pd.DataFrame(connections, columns=['Source', 'Target', "weight"])
	net = Network(notebook=True, height='100%', width='100%', bgcolor="#121212", font_color='white')
	
	sources = df['Source']
	targets = df['Target']
	weights = df['weight']
	edge_data = zip(sources, targets, weights)
	for e in edge_data:
		src = e[0]
		dst = e[1]
		w = e[2]

		net.add_node(src, src, title=src, size=8)
		net.add_node(dst, dst, title=dst, size=8)
		net.add_edge(src, dst, weights=w)

	if mode == "normal":
		net.set_options("""
		var options = {
	"nodes": {
		"shadow": {
      	"enabled": true
    	},
		"borderWidthSelected": 6,
		"color": {
		"border": "rgba(0,156,233,0.2)",
		"highlight": {
			"border": "rgba(0,255,163,1)",
			"background": "rgba(246,252,255,1)"
		}
		},
		"shapeProperties": {
		"borderRadius": 2
		}
	},
	"edges": {
		"color": {
		"inherit": true
		},
		"smooth": {
		"type": "continuous",
		"forceDirection": "none"
		}
	},
	"physics": {
		"barnesHut": {
		"springLength": 495,
		"damping": 1,
		"avoidOverlap": 1
		},
		"maxVelocity": 1,
		"minVelocity": 0.01
	}
	}
	""")
	else:
		net.show_buttons()
	net.show("Instagram-Social-Dynamics.html")



#map()
get()
