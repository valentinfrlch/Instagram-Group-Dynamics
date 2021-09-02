import os
import urllib

path = "/home/kali/Desktop/People/"

def split(text):
	lines = text.split("\n")
	handles = []
	for line in lines:
		try:
			handle = line.split("|")[3].strip()
			if handle != "Username":
				handles.append(handle)
		except IndexError:
			nope = 0
	return handles


for person in os.walk(path):
	if "handle" in person[2]:
		file = open(person[0] + "/handle")
		handle = file.readline()
		try:
			tagged = os.popen("cd /home/kali/tools/Osintgram && python3 main.py " + handle + " -c tagged").read()
			wtagged = os.popen("cd /home/kali/tools/Osintgram && python3 main.py " + handle + " -c wtagged").read()
			followers = os.popen("cd /home/kali/tools/Osintgram && python3 main.py " + handle + " -c followers").read()
			followings = os.popen("cd /home/kali/tools/Osintgram && python3 main.py " + handle + " -c followings").read()
		except urllib.error.HTTPError:
			break
		close = []
		virtual = []
		
		#Tagged List, offline connection
		taggedList = split(tagged)
		print(taggedList)
		wtaggedList = taggedList.extend(split(wtagged))
		close.append(wtaggedList)
		#Virtual List, only follow each other on IG, no offline connection
		followersList = split(followers)
		followingsList = followersList.extend(split(followings))
		virtual.append(followingsList)
			
		print(close, virtual)
