import csv
import os


with open('mask.csv', 'r', newline='') as maskcsv:
    # open the csv for reading
    reader = csv.DictReader(maskcsv)
    # get array of all photos
    photos_base = 'mask_photos_1819'
    photos = os.listdir(photos_base)
    photos.sort()
    # photos = photos[1:]
    # iterate over photos and spreadsheet simultaneously
    index = 0
    for row in reader:
        print(row['first'] + ' ' + row['last'] + ' - START: ' + str(index + 1))
        # if index + 1 != int(photos[index][9:14]):
        #     input('ERROR - csv: ' + str(index + 1) + ' != photos: ' + str(int(photos[index][9:14])))
        for p in range(index, int(row['photo_end'])):
            new_name = 'portland' + str(p) + '-' + row['id'] + '.jpg'
            print('  ' + str(p) + ' ' + photos[p] + ' -> ' + new_name)
            os.rename(photos_base + '/' + photos[p], photos_base + '/' + new_name)
        if row['photo_end'] != str(0):
            index = int(row['photo_end'])

