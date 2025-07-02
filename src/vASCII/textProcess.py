#Function that creates an array of colors out of a given string from a video
def lineToArr(line):
    colors = [None] * len(line)
    skip = False
    color = None

    lastBracket = 0
    count = 0
 
    #don't. change. this. 
    for i in range(len(line)):
        if skip:
            skip = False
            continue

        char = line[i]

        if char == "[" and line[i] != "H":
            lastBracket = i
            skip = True

        if char == "m":
            colorArr = line[lastBracket + 6 : i]
            color = colorArr.split(";")
            skip = True

        if char == " ":
            colors[count] = color
            count += 1
            skip = True

    return colors


#get the "difference" between two lines, i.e. what is needed to transition from the second to the first through printing
def getLineDiff(lineOne, lineTwo, color):
    result = ""
    count = 0

    if color:
        lOne = lineToArr(lineOne)
        lTwo = lineToArr(lineTwo)

        for i in range(len(lOne)):
            p1 = lOne[i]
            p2 = lTwo[i]

            if p1 == None:
                break

            if p1 == p2:
                count += 2
            else:
                if count != 0:
                    result += f"\033[{count}C"
                result += f"\033[48;2;{p1[0]};{p1[1]};{p1[2]}m  "
                count = 0
    else:
        for i in range(len(lineOne)):
            p1 = lineOne[i]
            p2 = lineTwo[i]

            if p1 == p2:
                count += 1
            else:
                if count > 0:
                    result += " " if count == 1 else f"\033[{count}C"
                    count = 0
                    
                result += p1

    result += "\n"
    return result
