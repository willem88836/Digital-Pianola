import os

should_print = True

def togglePrint(message):
    if should_print: 
        print(message)

def printArray(message, path):
    file = open("data\\" + path, "a")
    for m in message: 
        file.write(str(m) + "\n")
    file.close(); 


def relative_path(filename) -> str:
    return os.path.join(os.path.dirname(__file__), filename)
