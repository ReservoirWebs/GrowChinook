#!/usr/bin/python

import os, time
import matplotlib
matplotlib.use('Agg')
import sys
import csv
from Bioenergetics_Mult import *
import cgi, cgitb
import pylab
import io
from PIL import Image, ImageDraw
import base64
from matplotlib.ticker import FormatStrFormatter
import numpy
from collections import defaultdict

from scipy.interpolate import griddata
import pandas
cgitb.enable()
Scruffy()
form = cgi.FieldStorage()
StartingMass = 40
sys.stderr = sys.stdout

address = cgi.escape(os.environ["REMOTE_ADDR"])
script = "Multiple Month Run Page"
with open('userlog.csv', 'a') as log:
    log.write("IP: {}," .format(address))
    log.write("Page: {}," .format(script))
    log.write("Time: {}," .format(time.ctime(time.time())))
    log.write('\n')
log.closed

Elev = form.getvalue('Elev')
Total_Daphnia = None
DaphSize = None
TempCurve = None
Month = form.getvalue('Month1')
Month2 = form.getvalue('Month2')
Light = None
Year = form.getvalue('Year')
Site = form.getvalue('Site')
batches = []
results = {}
fullres = defaultdict(list)
growths = []
masses = []
dds = []
nds = []
newbatch = {}
z=0
MonthInts = {'March':1, 'April':2, 'May':3, 'June':4, 'July':5, 'August':6 }
Months = {1:'March',2:'April',3:'May',4:'June',5:'July',6:'August'}
Mon = MonthInts[Month]
Mon2 = MonthInts[Month2]
fig = pyplot.figure()
fig=pyplot.figure(facecolor='#c8e9b1')
fig.suptitle('Juvenile Spring Chinook', fontsize=20)
massax = fig.add_subplot(221)
Mass = StartingMass
for i in range(Mon, (Mon2+1)):
    Light,Total_Daphnia,DaphSize = GetVals(Light,Total_Daphnia,DaphSize,Site,Months[i],Year)
    batches.append(Batch(Site, Months[i], Year, Light, DaphSize, Total_Daphnia, Mass, 1000, -1, 1000,-1,"None_smoothed_None_None.csv",None,None,None))
    dd,nd,g,mass,length = (batches[z].Run_Batch())
    Mass = mass[29]
    for x in g:
        growths.append(x)
    for x in mass:
        masses.append(x)
    for x in dd:
        dds.append(x)
    for x in nd:
        nds.append(x)
    Light,Total_Daphnia,DaphSize = (None,None,None)
    z = z+1


	
print ('Content-type:text/html\r\n\r\n')
print('<html>')
print('''<link type="text/css" rel="stylesheet" media="screen" href="/css/Style.css" />
<link type="text/css" rel="stylesheet" media="screen" href="/css/Style.css" />
<img class="head" src="/css/src/LPR.jpg">
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js"></script>
<script src="/js/JavaForFish.js"></script>
<title>GrowChinook</title>
</head>
<body>
    <ul>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/">Home</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/">Instructions</li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/Test.py">Run Standard Model</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSens.py">Run Model With Sensitivity</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSens2.py">Run Advanced Sensitivity</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/scene.py">Run Scenarios</a><li>
        <li><a class="current" href="http://cas-web0.biossys.oregonstate.edu/TestSumm.py">Run Multiple Months</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/Curves.html">Temperature and Daphnia Curves</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/about.html">About</a></li>
        
    </ul>''')
massax.plot(masses, label="Mass (g)")
massax.set_ylabel('Mass (g)')
massax.set_xlabel('Day')
grax = fig.add_subplot(222)
grax.plot(growths)
grax.set_ylabel('Growth (g/g/d)')
grax.set_xlabel('Day')
dax = fig.add_subplot(223)
dax.plot(dds, 'black', label="Day Depth (m)")
dax.set_ylabel('Day Depth (m)')
dax.set_xlabel('Day')
dax.set_ylim(35,0)
dax.yticklabels=(arange(0,35,5))
nax = fig.add_subplot(224)
nax.set_ylabel('Night Depth (m)')
nax.set_xlabel('Day')
nax.plot(nds,'black', label="Night Depth (m)")
nax.yticklabels=(arange(0,35,5))
nax.set_ylim(35,0)
pyplot.subplots_adjust(top=0.3)
fig.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
pid = os.getpid()
fname=("output_%s.csv" % pid)
#with open(fname,'wb') as outfile:
#   writer = csv.writer(outfile)
#   writer.writerow(results.keys())
#   writer.writerows(zip(*results.values()))
#outfile.close()
pylab.savefig(("new_%s.png" % pid),facecolor=fig.get_facecolor(), edgecolor='lightblue')
data_uri = base64.b64encode(open(("new_%s.png" % pid), 'rb').read()).decode('utf-8').replace('\n', '')
img_tag = '<img class="results" src="data:image/png;base64,{0}">'.format(data_uri)
print(img_tag)
print('''
<body>
    <h2>Enter Values to GrowChinook</h2>
    <div id="formwrap">
        <form action="RunModelMult.py" method="post" target="_blank">
           <div>
               <label class="dd">Select Year:</label> <select name="Year" id="ddy" onchange="configureDropDownLists(this,document.getElementById('ddm1'),document.getElementById('dds'))">
                    <option value=""></option>
                    <option value="2015">2015</option>
                    <option value="2014">2014</option>
                    #<option value="2013">2013</option>
               </select>

               <label class="dd">Select Site:</label> <select name="Site" id="dds">
               </select>

               <label class="dd">Select Starting Month:</label> <select name="Month1" id="ddm1" onchange="configureMonthDropDowns(this,document.getElementById('ddm2'))">
               </select>
               
               <label class="dd">Select Ending Month:</label> <select name="Month2" id="ddm2" onchange="configureMonthDropDowns(this,document.getElementById('ddm2'))">
               </select>
               <br>
                                <div id="subutt">
                    <input type="submit" value="Submit"/>
                </div>
                <div style="float:left;">
                <label>Enter Name to Display on Tab:</label>
                <input type="text" style="width:50%;" name="TabName" id="TabNameID">
                </div><br>
            </div><br>
        </form>
    </div>

</body>
''')
print ('</html>')
