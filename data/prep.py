import csv

with open('factors.csv') as f:
    reader = csv.reader(f)
    l = list(reader)
    l.reverse()
    out = open('out.csv', 'w')
    writer = csv.writer(out)
    for row in l:
        writer.writerow(row)
