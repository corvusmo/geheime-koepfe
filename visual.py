#!/usr/bin/python
# coding: utf-8

import csv
import re
from colour import Color


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

# the head of the file
output = '''\
<!DOCTYPE HTML>
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<title>Sichere und geheime Köpfe</title>
	<script src="vis.min.js"></script>
	<script src="jquery-2.1.4.min.js"></script>
	<link href="vis.min.css" rel="stylesheet" type="text/css" />
<style>
	.vis-item {border-width:2px;}
	.vis-range {background-color:#ccc;}
	.vis-range.selected, .person {border-color:#FF7500;background-color:#FFF785;}
	.vis-range.person {border-color:#FF7500;background-color:#FFCF00;}
	.menu {position:absolute;top:0;left:20px;margin:10px;z-index:9999;}
	.breg .vis-item-content{background-color:rgba(255,255,255,0.8);background-clip:content-box;}
	.rg {background-image:linear-gradient(#f00 50%, #0c0 50%);}
	.sg {background-image:linear-gradient(#000 50%, #ff0 50%);}
	.sr {background-image:linear-gradient(#000 50%, #f00 50%);}
'''

# lets add some color!

csstemplate = '''\
	.%s {background-color: %s;}
'''

importantpeople = ['Frank-Walter Steinmeier', 'Günter Heiß', 'August Hanning', 'Wolfgang Schäuble', 'Thomas de Maiziére', 'Ernst Uhrlau', 'Peter Altmaier', 'Ronald Pofalla', 'Klaus-Dieter Fritsche', 'Gerhard Schindler', 'Hans-Peter Friedrich']
i = 1
for val in importantpeople:
	col = Color(hue=float(i)/float(len(importantpeople)), saturation=0.8, luminance=0.9)
	i += 1
	output += csstemplate % (re.sub('\W+', '', val), col)

# and the rest of the content before the data
output += '''\
	.cdsu {background-color:#000; color:#ddd;}
	.spd {background-color:#f00;}
	.fdp {background-color:#ff0;}
	.gruene {background-color:#0c0;}
	.noparty {background-color:#eee;}
</style>
</head>
<body>
<div id="einleitung" style="font-size:13px;">
Den Anstoß für diese Visualisierung gab die <a href="http://logbuch-netzpolitik.de/lnp168-es-war-nicht-alles-schlecht-im-rechtsstaat#t=43:23.003" target="_blank">Folge 168 des Podcast Logbuch Netzpolitik</a>. Der <a href="https://nelaco.de/lnp/bndbkamtmibfv.png">erste Versuch</a> war schnell erstellt, sehr einfach und nicht fehlerfrei (Fritsche). Außerdem wurde sich etwas "interaktives" gewünscht, hier nun also ein zweiter Versuch. <b>Hinweis:</b> In einigen Fällen habe ich bisher nur Jahreszahlen/Monate gefunden. In diesen Fällen wird immer der erste Tag als Start/End-Datum angenommen.<br />
<b>Mouseover:</b> vollständige Namen/Bezeichnungen<br />
<b>Klick auf einen Namen:</b>  alle bisherigen Ämter der Person auf einen Blick (soweit die Daten schon eingetragen sind)<br />
<b>Parteizugehörigkeit:</b> schaltet zwischen einer Darstellung der Parteizugehörigkeit und der Standardansicht hin und her
</div>
<div id="visualization" style="margin-top:10px;position:relative;">
<noscript>Ohne Javascript geht hier leider nix :/</noscript>
    <div class="menu">
        <input type="button" id="partei" value="Parteizugehörigkeit"/>
    </div>
</div>
<div>
<a href="https://github.com/corvusmo/geheime-koepfe" target="_blank">auf Github</a>
</div>

<script type="text/javascript">
var today = new Date();
var dd = today.getDate();
var mm = today.getMonth()+1; //January is 0!
var yyyy = today.getFullYear();
if(dd<10) { dd='0'+dd }
if(mm<10) { mm='0'+mm } 
today = yyyy+'-'+mm+'-'+dd;

  var groups = new vis.DataSet([
'''

# hier werden jetzt die groups erstellt
grouptemplate = '''{id:%s,content:'%s',title:'%s',order:%s},
'''

order = 0
for row in aemter[:9]:
	output += grouptemplate % (row[0], row[1], row[2], order)
	order += 1

for name in nameset:
	output += grouptemplate % ("'"+re.sub('\W+', '', name)+"'", name, name + "',className:'person", order)
	order += 1

#als erste Daten kommen die Bundesregierungen
output += \
	'''\
{id:99,content:'Ereignisse',title:'Was so alles passiert ist',order:99}
]);

  var items = new vis.DataSet([
{id:'A',group:0,content:'Schröder I',className:'breg rg',start:'1998-10-27',end:'2002-10-22'},
{id:'B',group:0,content:'Schröder II',className:'breg rg',start:'2002-10-22',end:'2005-11-22'},
{id:'C',group:0,content:'Merkel I',className:'breg sr',start:'2005-11-22',end:'2009-10-28'},
{id:'D',group:0,content:'Merkel II',className:'breg sg',start:'2009-10-28',end:'2013-12-17'},
{id:'E',group:0,content:'Merkel III',className:'breg sr',start:'2013-12-17',end:today},
'''

# the template. where data from the csv will be formatted to the correct format
datatemplate = '''{id:%s,group:%s,content:'%s',title:'%s',className:'%s',start:'%s',end:'%s'},
'''

i = 0
for row in zeiten:
	output += datatemplate % (i, row[0], row[1], row[1], re.sub('\W+', '', row[1]), row[2], row[3])
	i += 1

#dann die einzelnen Leute
for name in nameset:
	for row in zeiten:
		if row[1] == name:
			output += datatemplate % (i, "'"+re.sub('\W+', '', name)+"'", aemter[int(row[0])][1], aemter[int(row[0])][2], 'person', row[2], row[3])
			i += 1

# und jetzt die sonstigen Ereignisse
ereignissetemplate = '''{id:%s,group:99,content:'%s<br />%s',title:'%s',start:'%s'},
'''

for row in ereignisse:
	output += ereignissetemplate % (i, row[0][8:10]+'.'+row[0][5:7]+'.'+row[0][:4], row[1], row[2], row[0])
	i += 1

# the tail of the file
output += ''']);

  var name = '';

  var visiblegroups = new vis.DataView(groups, {
    filter: function (group) {
      return (group.id < 9) || (group.id == 99) || (group.id == name);
    }
  });

  var visibleitems = new vis.DataView(items, {
    filter: function (item) {
      return (item.group < 9) || (item.group == 99) || (item.group == name);
    }
  });

  var container = document.getElementById('visualization');

  var options = {
    orientation: 'both',
    selectable: false,
    stack: false,
    start: '2000-01-01',
  };

  var timeline = new vis.Timeline(container);
  timeline.setOptions(options);
  timeline.setGroups(visiblegroups);
  timeline.setItems(visibleitems);


document.getElementById('partei').onclick = function () { 
	$(".ThomasdeMaizire, .WolfgangSchuble, .PeterAltmaier, .RonaldPofalla, .KlausDieterFritsche, .GnterHei, .HansPeterFriedrich").toggleClass("cdsu");
	$(".FrankWalterSteinmeier, .ErnstUhrlau, .OttoSchily").toggleClass("spd");
	$(".GuidoWesterwelle, .GerhardSchindler").toggleClass("fdp");
	$(".JoschkaFischer").toggleClass("gruene");
	$(".AugustHanning").toggleClass("noparty");
};

$(".vis-item").click(function() {
	$(".vis-range").removeClass("selected");
	name = this.className.replace(/( |vis-item|vis-range|vis-readonly)/g,'');
	nameclass = '.' + name;
	$(nameclass).addClass("selected");

	//and now try to update the DataView
	visiblegroups.refresh();
	visibleitems.refresh();
});
</script>
</body>
</html>'''

output = output.replace("'today'", 'today')

# opens an file to write the output to
outFileHandle = open("index.html", "w")
outFileHandle.write(output)
outFileHandle.close()
