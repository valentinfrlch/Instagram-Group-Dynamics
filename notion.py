notion = open("/media/sf_Data/notion")
all = open("/media/sf_Data/lookup")
allList = []
notionList = []


for a in notion:
    both = a.strip().split(":")
    try:
        notionList.append(both[1].strip())
    except IndexError:
        err = 0

for x in all:
    allList.append(x.strip())

for element in notionList:
    if element in allList:
        allList.remove(element)


print(allList)
print("------------------")
print(notionList)

with open("/media/sf_Data/final", "w") as file:
    for handle in allList:
        file.write(handle + "\n")
