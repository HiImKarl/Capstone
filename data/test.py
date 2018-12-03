import csv

l = []
with open('farma_new.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        l.append([row[0], float(row[1]) / 100, float(row[2]) / 100, float(row[3]) / 100, float(row[4]) / 100])


with open('improved.csv', 'w') as f:
    writer = csv.writer(f)
    for row in l:
        writer.writerow(row)

