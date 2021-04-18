
should_print = True

def togglePrint(message):
    if should_print: 
        print(message)


def printArray(message, path):

    file = open("data\\" + path, "a")
    for m in message: 
        file.write(str(m) + "\n")
    file.close(); 
