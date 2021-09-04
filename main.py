import os
import time
from pathlib import Path
import networkx as nx
from pyvis.network import Network
from src.Osintgram import Osintgram
from instagram_private_api import ClientCookieExpiredError, ClientLoginRequiredError, ClientError, ClientThrottledError
import pandas as pd

path = "/home/kali/Desktop/People/"
tagged = ""
wtagged = ""
followers = ""
followings = ""


def extract(text, mode="virtual"):
	if mode == "close":
		lines = text.split("\n")
		handles = []
		for line in lines:
			try:
				handle = line.split("|")[3].strip()
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
			time.sleep(3)
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
					virtualFile.write(account + "\n")
			
			with open(person[0] + "/connections/close", "w") as closeFile:
				for account in close:
					closeFile.write(account + "\n")
			print("success")
			time.sleep(10)

def map(node="handle", type="real"):
	"""""
	node: Use real (node="real") names or the respective instagram handles (node="handle")
	"""""
	connections = []
	for person in os.walk(path):
		name = ""
		virtualList = []
		closeList = []
		if Path(person[0] + '/connections').is_dir():
			if node == "real":
				name = os.path.basename(person[0]).replace("\xa0", " ")
			else:
				file = open(person[0] + "/handle")
				name = file.readline()
			virtual = open(person[0] + "/connections/virtual")
			close = open(person[0] + "/connections/close")
			virtualLines = virtual.readlines()
			closeLines = close.readlines()
			for line in virtualLines:
				connections.append([name, line.strip()])
			for line in closeLines:
				closeList.append([name, line.strip()])
			#connections.append([name, virtualList, 1]) #closeList
			#break

	df = pd.DataFrame(connections, columns=['Source', 'Target'])
	G = nx.from_pandas_edgelist(df, source="Source", target="Target")
	net = Network(notebook=True, height='750px', width='100%', bgcolor="#121212", font_color='white')
	net.from_nx(G)
	net.toggle_physics(False)
	net.show("Instagram-Social-Dynamics.html")



#map()
get()
