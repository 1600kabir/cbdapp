import csv


f3 = []
l3 = []
def parse(filename):
	with open(filename) as csvDataFile:
		csvReader = csv.reader(csvDataFile)
		for row in csvReader:
			f = row[2:5]
			l = row[5:8]
			if "0" not in f: 
				if l.count("0") == 3:
					f3.append(row[0])
			if "0" not in l: 
				if f.count("0") == 3:
					l3.append(row[0])

	

