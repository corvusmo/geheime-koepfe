#!/usr/bin/python
# coding: utf-8

import csv
import re
from colour import Color

templatefile = open('template.html', 'r')
output = templatefile.read()
templatefile.close()

# Read in raw data from csv
ereignisse = csv.reader(open('ereignisse.csv', 'rb'), delimiter=',')
aemterRaw =  csv.reader(open('aemter.csv', 'rb'), delimiter=',')
zeitenRaw = csv.reader(open('amtszeiten.csv', 'rb'), delimiter=',')

#convert to lists (2d)
zeiten = list(zeitenRaw)
aemter = list(aemterRaw)

#create set with all the names (without duplicates)
nameset = set([])
for name in zeiten:
	nameset.add(name[1])

# lets add some color!
cssoutput = ''
csstemplate = '''
	.%s {background-color:%s;}'''

importantpeople = ['Frank-Walter Steinmeier', 'Günter Heiß', 'August Hanning', 'Wolfgang Schäuble', 'Thomas de Maiziére', 'Ernst Uhrlau', 'Peter Altmaier', 'Ronald Pofalla', 'Klaus-Dieter Fritsche', 'Gerhard Schindler', 'Hans-Peter Friedrich']
i = 1
for val in importantpeople:
	col = Color(hue=float(i)/float(len(importantpeople)), saturation=0.8, luminance=0.8)
	i += 1
	cssoutput += csstemplate % (re.sub('\W+', '', val), col)

# hier werden jetzt die groups erstellt
groupoutput = ''
grouptemplate = '''{id:%s,content:'%s',title:'%s',order:%s},
'''

order = 0
for row in aemter[:9]:
	groupoutput += grouptemplate % (row[0], row[1], row[2], order)
	order += 1

for name in nameset:
	groupoutput += grouptemplate % ("'"+re.sub('\W+', '', name)+"'", name, name + "',className:'person", order)
	order += 1

# the template. where data from the csv will be formatted to the correct format
itemoutput = ''
itemtemplate = '''{id:%s,group:%s,content:'%s',title:'%s',className:'%s',start:'%s',end:'%s'},
'''

i = 0
for row in zeiten:
	itemoutput += itemtemplate % (i, row[0], row[1], row[1], re.sub('\W+', '', row[1]), row[2], row[3])
	i += 1

#dann die einzelnen Leute
for name in nameset:
	for row in zeiten:
		if row[1] == name:
			itemoutput += itemtemplate % (i, "'"+re.sub('\W+', '', name)+"'", aemter[int(row[0])][1], aemter[int(row[0])][2], 'person', row[2], row[3])
			i += 1

# und jetzt die sonstigen Ereignisse
ereignissetemplate = '''{id:%s,group:99,content:'%s<br />%s',title:'%s',start:'%s'},
'''

for row in ereignisse:
	itemoutput += ereignissetemplate % (i, row[0][8:10]+'.'+row[0][5:7]+'.'+row[0][:4], row[1], row[2], row[0])
	i += 1

output = output.replace("//COLORTEMPLATE", cssoutput)
output = output.replace("{'GROUPTEMPLATE':1}", groupoutput)
output = output.replace("{'ITEMTEMPLATE':1}", itemoutput)
output = output.replace("'today'", 'today')

# opens an file to write the output to
outFileHandle = open("index.html", "w")
outFileHandle.write(output)
outFileHandle.close()
