import os
import csv
import numpy
import sqlite3
import shutil
import code


# CONFIG
#Directory of photos
originDir = "./Mask 2017/"
exportDir = "./EXPORT/"
emailFile = "emails.txt"

startIndex = 718 #Index origin 0 (row # - 1)
stop = 3192 # The id of the photo to stop at.

first = 0
last = 1
wwuid = 2
year = 3
gender = 4
faculty = 5
department = 6
photo = 7

# Import Data
print('setting things up...')
data = numpy.loadtxt(fname="id2photo.csv", delimiter=",", dtype=str)
# remove headers
data = numpy.delete(data, numpy.arange(startIndex), 0)
data = numpy.append(data, [["","","","","","","",str(stop)]], axis = 0)
conn = sqlite3.connect('./databases/people.db')

def wwuid2email(student):
    if student[0]:
        result = conn.execute('select * from profiles where wwuid="%s"' % student[wwuid]).fetchone()
        try:
            if result or result != None:
                return result[3] + '@wallawalla.edu'
            else:
                return student[first] + "." + student[last] + "@wallawalla.edu"
        except:
            print("ERROR Returning default", student)
            return student[first] + "." + student[last] + "@wallawalla.edu"
    else:
        print("WWUID NOT DEFINED", student)
        return student[first] + "." + student[last] + "@wallawalla.edu"

print("Working on Emails")
csv = ""
for idx, val in enumerate(data):
    csv += wwuid2email(val).replace(" ","") + "; "
try:
    os.remove(emailFile)
except OSError:
    pass
with open(emailFile, 'w') as f:
    f.write('')
    f.write(csv)
    f.close()


print("Moving Files...")
shutil.rmtree(exportDir, ignore_errors=True)
shutil.copytree(originDir, exportDir)

# Walla Walla Campus Mask

print("Changing filenames...")
for filename in os.listdir(exportDir):
    os.rename(exportDir + filename, exportDir + filename[9:])

for idx, val in enumerate(data):
    current = int(val[photo])
    if(not(data[idx + 1][photo])):
        nextV = current + 1
    else:
        nextV = int(data[idx + 1][photo])
    # TODO: change this to reflect end case
    while (not(current >= nextV) and not(current > stop)):
        try:
            os.rename(exportDir + str("{0:0=5d}".format(current)) + ".jpg",exportDir + str("{0:0=5d}".format(current)) + "-" + str("{0:0=7d}".format(int(val[wwuid]))) + ".jpg")
        except OSError as err:
            print("ERROR on ", current, ".jpg , ", err)
            pass
        except:
            print("ERROR on ", data[idx], current)
            pass
        #code.interact(local=locals())
        current += 1


print("FINISHED")
