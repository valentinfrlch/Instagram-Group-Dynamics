import os
lookup = open("/home/kali/Documents/lookup")
lookupNames = []
lookupHandles = []
path = "/home/kali/Desktop/People/"


for n in lookup:
    lookupNames.append(n.split(":")[0].strip())
    lookupHandles.append(n.split(":")[1].strip())

for person in os.walk(path):
    if ("handle" not in person[2]):
        name = str(os.path.basename(person[0]))
        name = name.replace("\xa0", " ")
        if (name in lookupNames):
            print(name)
            handleFile = open(person[0] + "/handle", "w")
            handleFile.write(lookupHandles[lookupNames.index(name)])
