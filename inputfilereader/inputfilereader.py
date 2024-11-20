f = open("C:\Git\Vis_2024/test.fdd", "r")

filecontent = f.read().splitlines()
f.close()

numOfRigidBodies = 0
currentBlockType = ""
currentTextBlock = []

for line in filecontent:
    if(line.find("$") >= 0): #new block found
        if(currentBlockType != ""):
            if(currentBlockType == "RIGID_BODY"):
                numOfRigidBodies += 1
            currentBlockType = ""

    if(line.find("RIGID_BODY", 1, len("RIGID_BODY")+1) >= 0):
       
       currentBlockType = "RIGID_BODY"
    currentTextBlock.clear

currentTextBlock.append(line)

print(numOfRigidBodies)