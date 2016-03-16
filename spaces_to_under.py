import sys
import os

""" replaces the spaces in file names by underscores ('_')
works with any number of files/folders dragged and dropped on the script"""

def newname(path): #returns the path with spaces in the file name replaced with '_' if spaces in the file name, else false
    output = path.split('\\')
    output[-1] = output[-1].replace(' ', '_') if ' ' in output[-1] else False
    return '\\'.join(output) if output[-1] else False

r = n = 0
i = 1
while True :
    try :
        if newname(sys.argv[i]) :
            os.rename(sys.argv[i], newname(sys.argv[i]))
            print ('{0} -> {1}'.format(sys.argv[i].split('\\')[-1], newname(sys.argv[i]).split('\\')[-1]))
            r += 1
        else :
            print('{0} -> Not renamed'.format(sys.argv[i].split('\\')[-1]))
            n += 1
        i += 1
    except IndexError :
        break


input('\ndone, {0} file(s) renamed, {1} file(s) ignored, press enter to close program'.format(r,n))
