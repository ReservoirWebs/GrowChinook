#!/usr/bin/python

import os,time
import matplotlib
matplotlib.use('Agg')
import sys
import csv
from Bioenergetics import *
import cgi, cgitb
import pylab
import io
from PIL import Image, ImageDraw
import base64
from matplotlib.ticker import FormatStrFormatter
import numpy

from scipy.interpolate import griddata
import pandas
cgitb.enable()
Scruffy()
form = cgi.FieldStorage()

address = cgi.escape(os.environ["REMOTE_ADDR"])
script = "Sensitivity Run Page"
with open('userlog.csv', 'a') as log:
    log.write("IP: {}," .format(address))
    log.write("Page: {}," .format(script))
    log.write("Time: {}," .format(time.ctime(time.time())))
    log.write('\n')
log.closed

# Get data from fields

StartingMass = form.getvalue('Starting_Mass_In')
DYear = form.getvalue('DYear')
DMonth = form.getvalue('DMonth')
DSite = form.getvalue('DSite')
TempCurve = '{0}_smoothed_{1}_{2}.csv'.format(form.getvalue('TSite'), form.getvalue('TMonth'), form.getvalue('TYear'))

if StartingMass != None:
    StartingMass=float(StartingMass)
else:
    StartingMass = 40

if form.getvalue('depr') == 'yes':
    depr_flag = 'YES'
else:
    depr_flag = 'NO'
if form.getvalue('tempr') == 'yes':
    tempr_flag = 'YES'
else:
    tempr_flag = 'NO'
Elev = form.getvalue('Elev')
Total_Daphnia = form.getvalue('Total_Daphnia_Input_Name')
if Total_Daphnia != None:
    Total_Daphnia = float(Total_Daphnia)
DaphSize  = form.getvalue('Daphnia Size')
if DaphSize != None:
    DaphSize = float(DaphSize)
else:
    DaphSize = 1
Light = form.getvalue('Light')
if Light != None:
    Light = float(Light)
Year = form.getvalue('Year')
if Year == None:
    Year = '2015'
Site = form.getvalue('Site')
if Site == None:
    Site = 'Fall Creek'
Month = form.getvalue('Month1')
if Month == None:
    Month = 'June'

if depr_flag == 'YES':
    Dmax = float(form.getvalue('DmaxIn'))
    Dmin = float(form.getvalue('DminIn'))
else:
    Dmax = 10000
    Dmin = -1
if tempr_flag == 'YES':
    Tmax = float(form.getvalue('TmaxIn'))
    Tmin = float(form.getvalue('TminIn'))
else:
    Tmax = 10000
    Tmin = -1

print ('Content-type:text/html; charset=utf-8\r\n\r\n')
print ('<html>')
print('''<link type="text/css" rel="stylesheet" media="screen" href="/css/Style.css" />
<script src="/js/JavaForFish.js"></script>
<img class="head" src="/css/src/LPR.jpg">
<head>
    <title>GrowChinook</title>
</head>
<body>
    <ul>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/">Home</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/">Instructions</li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/Test.py">Run Standard Model</a></li>
        <li><a class="current" href="http://cas-web0.biossys.oregonstate.edu/TestSens.py">Run Model With Sensitivity</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSens2.py">Run Advanced Sensitivity</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/scene.py">Run Scenarios</a><li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSumm.py">Run Multiple Months</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/Curves.html">Temperature and Daphnia Curves</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/about.html">About</a></li>
    </ul>''')
print ('<head>')
print ('<title>Here are Your Results.</title>')
print ('</head>')

Light,Total_Daphnia,DaphSize = GetVals(Light,Total_Daphnia,DaphSize,Site,Month,Year)
FreshBatch = Batch(Site, Month, Year, Light, DaphSize, Total_Daphnia, StartingMass, Dmax, Dmin,Tmax,Tmin,TempCurve,DYear,DMonth,DSite,Elev)
BaseResults,DConsumed,condition,condition1,dt,nt,PopEst  = FreshBatch.Run_Batch()

largestout = 0.0
numskips = 0
batches = []
results = []
SensInputs = []
SensFactors = []
SensOutPer = []
SensOutPerD1 = []
Growths = []
Growths1 = []
csvheaders=[[] for i in range(11)]
if form.getvalue('Sparam_Range') != None:
    Sparam_Range = float(form.getvalue('Sparam_Range'))
else:
   Sparam_Range = 0.75
SensParam = form.getvalue('Sens_Param')
SensFactors = Sensitivity_Expand(Sparam_Range, SensFactors)

if SensParam == 'Starting Mass':
    Sparam = StartingMass
    for i in range(11):
        if (Sparam * SensFactors[i] + Sparam) < .2:
            SensInputs.append(.00001)
        else:
            SensInputs.append(Sparam * SensFactors[i] + Sparam)
        SensFactors[i] = SensFactors[i] * 100
        csvheaders[i] = [Site,Month,Year,("%s: %f" % ("Starting Mass",SensInputs[i]))]
        batches.append(Batch(Site, Month, Year, Light, DaphSize, Total_Daphnia, SensInputs[i],Dmax,Dmin,Tmax,Tmin,TempCurve,DYear,DMonth,DSite))
        results.append(batches[i].Run_Batch())
        SensOutPer.append(results[i][0]['growth'][29])
        SensOutPerD1.append(results[i][0]['growth'][0])
        Growths.append(results[i][0]['growth'][29])
        Growths1.append(results[i][0]['growth'][0])


elif SensParam == 'Total Daphnia':
    Sparam = Total_Daphnia
    for i in range(11):
        if (Sparam * SensFactors[i] + Sparam) > 0:
            SensInputs.append(Sparam * SensFactors[i] + Sparam)
        else:
            SensInputs.append(.00001)
        SensFactors[i] = SensFactors[i] * 100
        csvheaders[i] = [Site,Month,Year,("%s: %f" % ("Total Daphnia",SensInputs[i]))]
        batches.append(Batch(Site, Month, Year, Light, DaphSize, SensInputs[i], StartingMass,Dmax,Dmin,Tmax,Tmin,TempCurve,DYear,DMonth,DSite))
        results.append(batches[i].Run_Batch())
        SensOutPer.append(100 * ((results[i][0]['growth'][29] - BaseResults['growth'][29]) / BaseResults['growth'][29]))
        SensOutPerD1.append(100 * ((results[i][0]['growth'][0] - BaseResults['growth'][0]) / BaseResults['growth'][0]))
        Growths.append(results[i][0]['growth'][29])
        Growths1.append(results[i][0]['growth'][0])


elif SensParam == 'Daphnia Size':
    Sparam = DaphSize
    for i in range(11):
        if (Sparam * SensFactors[i] + Sparam) > 0:
            SensInputs.append(Sparam * SensFactors[i] + Sparam)
        else:
            SensInputs.append(.00001)
        SensFactors[i] = SensFactors[i] * 100
        csvheaders[i] = [Site,Month,Year,("%s: %f" % ("Daphnia Size",SensInputs[i]))]
        batches.append(Batch(Site, Month, Year, Light, SensInputs[i], Total_Daphnia, StartingMass,Dmax,Dmin,Tmax,Tmin,TempCurve,DYear,DMonth,DSite))
        results.append(batches[i].Run_Batch())
        SensOutPer.append(100 * ((results[i][0]['growth'][29] - BaseResults['growth'][29]) / BaseResults['growth'][29]))
        SensOutPerD1.append(100 * ((results[i][0]['growth'][0] - BaseResults['growth'][0]) / BaseResults['growth'][0]))
        Growths.append(results[i][0]['growth'][29])
        Growths1.append(results[i][0]['growth'][0])

elif SensParam == 'Light':
    Sparam = Light
    for i in range(11):
        if (Sparam * SensFactors[i] + Sparam) > 0:
            SensInputs.append(Sparam * SensFactors[i] + Sparam)
        else:
            SensInputs.append(.00001)
        SensFactors[i] = SensFactors[i] * 100
        csvheaders[i] = [Site,Month,Year,("%s: %f" % ("LEC(K)",SensInputs[i]))]
        batches.append(Batch(Site, Month, Year, SensInputs[i], DaphSize, Total_Daphnia, StartingMass,Dmax,Dmin,Tmax,Tmin,TempCurve,DYear,DMonth,DSite))
        results.append(batches[i].Run_Batch())
        SensOutPer.append(100 * ((results[i][0]['growth'][29] - BaseResults['growth'][29]) / BaseResults['growth'][29]))
        SensOutPerD1.append(100 * ((results[i][0]['growth'][0] - BaseResults['growth'][0]) / BaseResults['growth'][0]))
        Growths.append(results[i][0]['growth'][29])
        Growths1.append(results[i][0]['growth'][0])


for i in range(len(SensFactors)):
    if SensFactors[i] != None:
        if abs(SensFactors[i]) > abs(largestout):
            largestout = abs(SensFactors[i])
for i in range(len(SensOutPer)):
    if SensOutPer[i] != None:
        if abs(SensOutPer[i]) > abs(largestout):
            largestout = abs(SensOutPer[i])
if abs(largestout) > 30000:
    largestout = 30000
largestoutrem = largestout % 50
largestout = largestout + 50 - largestoutrem
fig=pyplot.figure()
fig=pyplot.figure(facecolor='#c8e9b1')
fig.suptitle('Juvenile Spring Chinook', fontsize=20)

#ax = fig.add_subplot(222)
#ax.plot(SensFactors, SensOutPer, 'g^')
#ax.set_xticks(SensFactors)
#ax.xaxis.set_major_formatter(FormatStrFormatter('%i'))

#if SensParam == 'Starting Mass':
#    ax.set_ylabel('Final Growth Rate')
#else:
#    ax.set_ylabel('Day 30 % Change Growth Rate')
#ax.axis([-largestout, largestout, -largestout, largestout])
#ax.set_aspect('equal', adjustable='box')
#ax.set_xlabel('Percent Change in %s' % SensParam)
#ax.grid()
#ax1 = fig.add_subplot(221)
#ax1.plot(SensFactors, SensOutPerD1, 'o')
#if SensParam == 'Starting Mass':
#    ax1.set_ylabel('Day 1 Growth Rate')
#else:
#    ax1.set_ylabel('Day 1 % Change Growth Rate')
#ax1.axis([-largestout, largestout, -largestout, largestout])
#ax1.set_aspect('equal', adjustable='box')
#ax1.set_xlabel('Percent Change in %s' % SensParam)
#ax1.grid()
ax2 = fig.add_subplot(211)
ax2.plot(SensInputs,Growths1)
ax2.set_ylabel('Day 1 Growth Rate')
#ax2.axis([-largestout, largestout, -largestout, largestout])
#ax2.set_aspect('equal', adjustable='box')
ax2.set_xlabel('%s Input Value' % SensParam)
ax2.grid()
ax3 = fig.add_subplot(212)
ax3.plot(SensInputs,Growths)
ax3.set_ylabel('Final Growth Rate')
#ax3.axis([-largestout, largestout, -largestout, largestout])
#ax3.set_aspect('equal', adjustable='box')
ax3.set_xlabel('%s Input Value' % SensParam)
ax3.grid()
pyplot.subplots_adjust(top=0.3)
fig.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
pid = os.getpid()
fname=("output_%s.csv" % pid)
with open(fname,'w') as outfile:
   writer = csv.writer(outfile)
   l=0
   for batch in results:
       writer.writerow(csvheaders[l])
       if batch != None:
           writer.writerow(batch[0].keys())       
           writer.writerows(zip(*batch[0].values()))
       l=l+1
outfile.close()
pylab.savefig(("new_%s.png" % pid),facecolor=fig.get_facecolor(), edgecolor='lightblue')
data_uri = base64.b64encode(open(('new_%s.png' % pid), 'rb').read()).decode('utf-8').replace('\n', '')
img_tag = '<img class="results" src="data:image/png;base64,{0}">'.format(data_uri)
print(img_tag)

print ('''
    <br>
    <div id="valuewraps">
        <div id="datahead">
            %s, %s
        </div>
        <div id="indata">
            <div class="dataleft">Input Values:</div>
            <div class="dataleft">%s Starting Mass:
                <div class="dataright">%.1f g</div>
            </div>
            <div class="dataleft">%s Total Daphnia:
                <div class="dataright">%.0f</div>
            </div>
            <div class="dataleft">%s Daphnia Size:
                <div class="dataright">%.2f mm</div>
            </div>
            <div class="dataleft">%s Light Extinction Coefficient:
                <div class="dataright">%.2f</div>
            </div>
            <div class="dataleft">Download Full Results?
                <a class="dataright" href="/%s" download>Download</a>
            </div>
       ''' % (FreshBatch.Site,FreshBatch.Year,Month,StartingMass,Month,FreshBatch.TotalDaphnia,Month,FreshBatch.DaphSize,Month,FreshBatch.Light,fname))

if depr_flag == "YES":
    print('''Depth restricted to between %.2fm and %.2fm.<br>''' % (Dmin,Dmax))
if tempr_flag == "YES":
    print('''Temperature restricted to between %.2f degrees and %.2f degrees.<br>''' % (Tmin, Tmax))

print ('''  </div>
            <div id="outdata">
                <div class="dataleft">Day 1 Output Values:</div>
                <div class="dataleft">Chinook Mass:
                    <div class="dataright">%.1f g</div>
                </div>


                <div class="dataleft">Growth:
                    <div class="dataright">%.2f g/g/day</div>
                </div>

                <div class="dataleft">Day Depth Occupied:
                    <div class="dataright">%.0f m</div>
                </div>
                <div class="dataleft">Night Depth Occupied:
                    <div class="dataright">%.0f m</div>
                </div>
            </div>

            <div id="outdata">
                <div class="dataleft">Day 30 Output Values:</div>
                <div class="dataleft">Chinook Mass:
                    <div class="dataright">%.1f g</div>
                </div>
                <div class="dataleft">Growth (day 30):
                    <div class="dataright">%.2f g/g/day</div>
                </div>
                <div class="dataleft">Day Depth Occupied:
                    <div class="dataright">%.0f m</div>
                </div>
                <div class="dataleft">Temp at Day Depth Occupied:
                    <div class="dataright">%.0f &#176;C</div>
                </div>
                <div class="dataleft">Night Depth Occupied:
                    <div class="dataright">%.0f m</div>
                </div>
                <div class="dataleft">Temp at Night Depth Occupied:
                    <div class="dataright">%.0f &#176;C</div>
                </div>
                <div class="dataleft">Total Daphnia Consumed:
                    <div class="dataright">%.0f</div>
                </div>
                <div class="dataleft">Estimated Condition Change:
                <div class="dataright">%.2f</div>
                </div>
            </div>

       </div>
       </div><br>
       ''' % (BaseResults['StartingMass'][0],BaseResults['growth'][0],BaseResults['day_depth'][0],dt,BaseResults['night_depth'][0],nt,BaseResults['StartingMass'][29],
              BaseResults['growth'][29],BaseResults['day_depth'][29],BaseResults['night_depth'][29],DConsumed,condition))

print('''

<body>
    <h2>Enter Values to GrowChinook</h2>
    <div id="formwrap">
        <form action="RunModelSens.py" method="post" target="_blank">
           <div style="display:inline-block;width:90%;">
                    <div style="font-size:20px;width:45%;float:left;margin:auto;">First Select Sensitivity Parameter:<select name="Sens_Param"><br>
                        <option value="Starting Mass" selected>Starting Mass</option>
                        <option value="Total Daphnia">Total Daphnia</option>
                        <option value="Daphnia Size">Daphnia Size</option>
                        <option value="K">Light</option>
                    </select>
                    </div>

                    <div style="width:45%;float:right;">
                    <label>Enter Value for Sensitivity Range (Percent):</label> <input type="text" name="Sparam_Range" id="SensTextInID" oninput="SensOutID.value = SensTextInID.value"></div> <br>
                    </div><br><br><br>
           <b>Enter a Starting Mass for the fish. Then select a default Year, Month, and Site, which will be used to fill in any fields you may choose to leave blank.
           Now you may adjust any values you like, and can at any time reassert the default values for your selected Year, Month, and Site by clicking the "Apply Observed Values" button.</b>

           <div id="sec1">
                <br>
                <label>Enter Fish Starting Mass (g):</label><input type="text" name="Starting_Mass_In" id="SMass_TextInID"  oninput="SMassSlide.value = SMass_TextInID.value"> <br><br>
                <p style="text-align:center;width:80%;"><b>Select a Year, Month, and Site to fill Daphnia Density, Daphnia Size, and Light Extinction Coefficient with Observed Values</b>
                <div style="margin:auto;">
                <label class="dd">Year:</label> <select name="Year" value="2015" id="ddy" onchange="configureDropDownLists(this,document.getElementById('ddm1'),document.getElementById('dds'))">
                    <option value=""></option>
                    <option value="2015">2015</option>
                    <option value="2014">2014</option>
                    
                </select>

                <label class="dd">Site:</label> <select name="Site" value="Fall Creek" id="dds">
                </select>

                <label class="dd">Month:</label> <select name="Month1" value="June" id="ddm1" onchange="configureMonthDropDowns(this,document.getElementById('ddm2'))">
                </select>
                <br>
                </div>
                <div style="text-align:center;"><button type="button" onclick="getDefaultValues(document.getElementById('ddy'),document.getElementById('ddm1'),document.getElementById('dds'),document.getElementById('SMass_TextInID'),document.getElementById('TotDDef'),document.getElementById('DaphSDef'),document.getElementById('LightDef'));
                getDefaultValues(document.getElementById('ddy'),document.getElementById('ddm1'),document.getElementById('dds'),document.getElementById('SMass_TextInID'),document.getElementById('TotDTextInID'),document.getElementById('DaphSTextInID'),document.getElementById('LightTextInID'));">Apply Observed Values</button>
                </div>
                <br>

                Observed:<input class="defdisp" type="text" name="TotDDef" id="TotDDef" value="" readonly><label>Daphnia Density (per m<sup>2</sup> surface)</label>Using:<input type="text" name="Total_Daphnia_Input_Name" id="TotDTextInID" oninput="TotDSlide.value = TotDTextInID.value" oninput="TotDOutID.value = TotDInID.value"> <br><br>

                Observed:<input class="defdisp" type="text" name="LightDef" id="LightDef" value="" readonly><label>Light Extinction Coefficient</label>Using:<input type="text" name="Light" id="LightTextInID" oninput="LightSlide.value = Light.value"><output name="Light_TextOut" id="Light_TextOutID"> </output> <br><br>


                Observed:<input class="defdisp" type="text" name="DaphSDef" id="DaphSDef" value="" readonly><label>Daphnia Size (mm):</label>Using:<input type="text" name="Daphnia Size" id="DaphSTextInID" oninput="DaphSSlide.value = DaphSTextInID.value"> <br><br>

                <div class="deptem" style="float:left;"><p style="margin-top:auto;"><b>Optional: Set to restrict depth</b></div>
                <div style="float:right;width:70%;">
		        <label class="deptem">Maximum Depth:</label><input class="deptem" type="text" name="DmaxIn" id="DmaxInID"><br>
                <label class="deptem">Minimum Depth:</label><input class="deptem" type="text" name="DminIn" id="DminInID">
                </div>

            </div>
            <div id="sec2">
                <br>
                <div style="display:inline-block;">
                <div class="deptem" style="float:left;"><p style="margin-top:auto;"><b>Optional: Set to restrict temperature</b></div>
                <div style="float:right;width:70%;">
		        <label class="deptem">Maximum Temperature:</label><input class="deptem" type="text" name="TmaxIn" id="TmaxInID"><br>
                <label class="deptem">Minimum Temperature:</label><input class="deptem" type="text" name="TminIn" id="TminInID">
                </div>
                </div>
                <div><br></div>


                <div style="width:80%;"><b>Optional: Select a Year, Month, and Site to apply the corresponding Daphnia distribution curve. Otherwise, the curve corresponding to the Default Year, Month, and Site will be used.</b>
                <label class="dd">Daphnia Year:</label> <select name="DYear" id="dddy" onchange="configureDropDownLists(this,document.getElementById('dddm'),document.getElementById('ddds'))">
                    <option value=""></option>
                    <option value="2015">2015</option>
                    <option value="2014">2014</option>
                    
                </select>

                <label class="dd">Daphnia Site:</label> <select name="DSite" id="ddds">
                </select>

                <label class="dd">Daphnia Month:</label> <select name="DMonth" id="dddm">
                </select>
<div><br></div>
                <div style="margin-top:auto;width:100%;"><b>Optional: Select a Year, Month, and Site to apply the corresponding Temperature distribution curve. Otherwise, the curve corresponding to the Default Year, Month, and Site will be used.</b>
                <div><br></div>
                <label class="dd">Temperature Year:</label> <select name="TYear" id="ddty"  onchange="configureDropDownLists(this,document.getElementById('ddtm'),document.getElementById('ddts'))">
                    <option value=""></option>
                    <option value="2015">2015</option>
                    <option value="2014">2014</option>
                    
                </select>

                <label class="dd">Temperature Site:</label> <select name="TSite" id="ddts">
                </select>

                <label class="dd">Temperature Month:</label> <select name="TMonth" id="ddtm">
                </select>
                </div>
                    <br>
                    <br><div style="float:left;">
                <label>Enter Name to Display on Tab:</label>
                <input type="text" style="width:50%;" name="TabName" id="TabNameID">
                </div><br>

                    <div id="subutt">
                        <input type="submit" value="Submit"/>
                    </div>
                
        </form>
    </div>
</body>
''')

os.remove('new_%s.png' %pid)
quit()
