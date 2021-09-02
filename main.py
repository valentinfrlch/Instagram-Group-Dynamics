import os
import urllib
import json
import time
from pathlib import Path


path = "/home/kali/Desktop/People/"
tagged = ""
wtagged = ""
followers = ""
followings = ""


def extract(text):
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


for person in os.walk(path):
	if ("handle" in person[2]) and (Path(person[0] + '/connections').is_dir() == False):	
		file = open(person[0] + "/handle")
		handle = file.readline()
		print(handle)
		try:
			tagged = os.popen("cd /home/kali/tools/Osintgram && python3 main.py " + handle + " -c tagged").read()
			wtagged = os.popen("cd /home/kali/tools/Osintgram && python3 main.py " + handle + " -c wtagged").read()
			followers = os.popen("cd /home/kali/tools/Osintgram && python3 main.py " + handle + " -c followers").read()
			followings = os.popen("cd /home/kali/tools/Osintgram && python3 main.py " + handle + " -c followings").read()
		except (urllib.error.HTTPError, json.decoder.JSONDecodeError) as e:
			break
		



		#Tagged List, offline connection
		close = extract(tagged) + extract(wtagged)
		#Virtual List, only follow each other on IG, no offline connection
		virtual = extract(followers) + extract(followings)
		
		os.makedirs(person[0] + "/connections", exist_ok=True)
		print(close, virtual)
		
		with open(person[0] + "/connections/virtual", "w") as virtualFile:
			for account in virtual:
				virtualFile.write(account + "\n")
		
		with open(person[0] + "/connections/close", "w") as closeFile:
			for account in close:
				closeFile.write(account + "\n")
		time.sleep(15)
