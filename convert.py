import os
import csv
import numpy
import sqlite3
import shutil
import code
import pandas

# CONFIG
#Directory of photos
originDir = "./Portland Mask/"
exportDir = "./EXPORT/"
emailFile = "emails.txt"
csvFile = "Portland Mask.csv"

startIndex = 1 #Index origin 0 (row # - 1)

first = 0
last = 1
wwuid = 2
photoIdx = 3

# Import Data
print('setting things up...')
data = pandas.io.parsers.read_csv(csvFile).as_matrix()
data = data.astype(str)

data = numpy.delete(data, numpy.arange(startIndex), 0)
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

# PORTLAND CAMPUS MASK photos

print("Changing filenames...")

for idx, val in enumerate(data):

    photos = val[photoIdx].replace('"', '').replace("'","").split(', ')
    for i, photoName in enumerate(photos):
        # Debug info
        print(exportDir + photoName + ".jpg   --->   " +  exportDir + photoName + "-" + val[wwuid] + ".jpg")
        try:
            os.rename(exportDir + photoName + ".jpg", exportDir + photoName + "-" + val[wwuid] + ".jpg")
        except OSError as err:
            # code.interact(local=locals())
            print("Photo ERROR", photoName, err)
            pass
        except:
            code.interact(local=locals())
            print("ERROR on ", val)

print("FINISHED")
