#!/usr/bin/python

import os, time
import sys
import csv
import matplotlib
matplotlib.use('Agg')
from Bioenergetics import *
import cgi, cgitb
import pylab
import io
from PIL import Image, ImageDraw
import base64
from scipy.interpolate import griddata
import pandas

address = cgi.escape(os.environ["REMOTE_ADDR"])
script = "Main Model Run Page"
with open('userlog.csv', 'a') as log:
    log.write("IP: {}," .format(address))
    log.write("Page: {}," .format(script))
    log.write("Time: {}," .format(time.ctime(time.time())))
    log.write('\n')
log.closed

Scruffy()
cgitb.enable()
form = cgi.FieldStorage()
title=form.getvalue('TabName')
if title == None:
    title="GrowChinook Results"
'''
fileitem = form["userfile"]
if fileitem.file:
    linecount = 0
    while 1:
        line = fileitem.file.readline()
        if not line: break
        linecount = linecount + 1
'''
TempCurve = form.getvalue('tempCurve')
StartingMass = form.getvalue('Starting_Mass_In')
if StartingMass != None:
    StartingMass=float(StartingMass)
else:
    StartingMass = 40

if (form.getvalue('DmaxIn') == None) and (form.getvalue('DminIn') == None):
    depr_flag = 'NO'
else:
    depr_flag = 'YES'

if (form.getvalue('TmaxIn') == None) and (form.getvalue('TminIn') == None):
    tempr_flag = 'NO'
else:
    tempr_flag = 'YES'


Total_Daphnia = form.getvalue('Total_Daphnia_Input_Name')
if Total_Daphnia == None:
    if form.getvalue('TotDDef') != None:
        Total_Daphnia = form.getvalue('TotDDef')
else:
    Total_Daphnia = float(Total_Daphnia)
DaphSize  = form.getvalue('Daphnia Size')
if DaphSize == None:
    if form.getvalue('DaphSDef') != None:
        DaphSize = form.getvalue('DaphSDef')
else:
    DaphSize = float(DaphSize)
Light = form.getvalue('Light')
if Light == None:
    if form.getvalue('LightDef') != None:
        Light = form.getvalue('LightDef')
else:
    Light = float(Light)
Year = form.getvalue('Year')
if Year == '2016':
    TYear = '2016'
    Year = '2016'
elif Year == None:
    Year = "2015"
Month = form.getvalue('Month1')
if Month == None:
    Month = "June"
Site = form.getvalue('Site')
if Site == None:
    Site = "Fall Creek"

if depr_flag == 'YES':
    if form.getvalue('DmaxIn') != None:
        Dmax = float(form.getvalue('DmaxIn'))
    else:
        Dmax = 10000
    if form.getvalue('DminIn') != None:
        Dmin = float(form.getvalue('DminIn'))
    else:
        Dmin = -1
else:
    Dmin,Dmax = -1,1000

if tempr_flag == 'YES':
    if form.getvalue('TmaxIn') != None:
        Tmax = float(form.getvalue('TmaxIn'))
    else:
        Tmax = 10000
    if form.getvalue('TminIn') != None:
        Tmin = float(form.getvalue('TminIn'))
    else:
        Tmin = -1
    if Tmin==Tmax:
        Tmax = Tmax+1
else:
    Tmin,Tmax = -1,1000

PSite = form.getvalue('ESite')
Elev = form.getvalue('Elev')
if Elev == None:
    Elev = 10000
DYear = form.getvalue('DYear')
if DYear == None:
    DYear = Year
DMonth = form.getvalue('DMonth')
if DMonth == None:
    DMonth = Month
DSite = form.getvalue('DSite')
if DSite == None:
    DSite = Site
TYear = form.getvalue('TYear')
if TYear == None:
    TYear = Year
TMonth = form.getvalue('TMonth')
if TMonth == None:
    TMonth = Month
TSite = form.getvalue('TSite')
if TSite == None:
    TSite = Site
TempCurve = '{0}_T_{1}_{2}.csv'.format(TSite, TMonth, TYear)


print ('Content-type:text/html; charset=utf-8\r\n\r\n')
print ('<html>')
print('<link type="text/css" rel="stylesheet" media="screen" href="/css/Style.css" />')
print ('<head>')
print ('<title>{}</title>'.format(title))
print ('</head>')
print('''<link type="text/css" rel="stylesheet" media="screen" href="/css/Style.css" />
<link type="text/css" rel="stylesheet" media="screen" href="/css/Style.css" />
<script src="/js/JavaForFish.js"></script>

<img class="head" src="/css/src/LPR.jpg">
<head>
    <title>GrowChinook</title>
</head>
<body>
    <ul>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/">Home</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/">Instructions</li>
        <li><a class="current" href="http://cas-web0.biossys.oregonstate.edu/Test.py">Run Standard Model</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSens.py">Run Model With Sensitivity</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSens2.py">Run Advanced Sensitivity</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSumm.py">Run Multiple Months</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/scene.py">Run Scenarios</a><li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/Curves.html">Temperature and Daphnia Curves</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/about.html">About</a></li>
    </ul>''')

Light,Total_Daphnia,DaphSize = GetVals(Light,Total_Daphnia,DaphSize,Site,Month,Year)
try:
    FreshBatch = Batch(Site, Month, Year, Light, DaphSize, Total_Daphnia, StartingMass, Dmax, Dmin,Tmax,Tmin,TempCurve,DYear,DMonth,DSite,Elev,PSite)
    BaseResults,DConsumed,condition,condition1,daytemp,nighttemp,PopEst  = FreshBatch.Run_Batch()
except:    
    #print ('Content-Type: text/html')
    #print ('Location: http://cas-web0.biossys.oregonstate.edu/error.html')
    #print ('<html>')
    #print ('<head>')
    #print ('<meta http-equiv="refresh" content="0;url=http://cas-web0.biossys.oregonstate.edu/error.html" />')
    #print ('<title>You are going to be redirected</title>')
    #print ('</head>') 
    #print ('<body>')
    #print ('Redirecting... <a href="http://cas-web0.biossys.oregonstate.edu/error.html">Click here if you are not redirected</a>')
    #print ('</body>')
    #print ('</html>')
    cgitb.handler()

fig = pyplot.figure()
fig=pyplot.figure(facecolor='#c8e9b1')
fig.suptitle('Juvenile Spring Chinook', fontsize=20)
massax = fig.add_subplot(221)
massax.plot(BaseResults['StartingMass'], label="Mass (g)")
massax.set_ylabel('Mass (g)')
massax.set_xlabel('Day of Month')
grax = fig.add_subplot(222)
grax.plot(BaseResults['growth'])
grax.set_ylabel('Growth (g/g/d)')
grax.set_xlabel('Day of Month')
dax = fig.add_subplot(223)
dax.plot(BaseResults['day_depth'], 'black', label="Day Depth (m)")
dax.set_ylabel('Day Depth (m)')
dax.set_xlabel('Day of Month')
dax.set_ylim(35,0)
dax.yticklabels=(arange(0,35,5))
nax = fig.add_subplot(224)
nax.set_ylabel('Night Depth (m)')
nax.set_xlabel('Day of Month')
nax.plot(BaseResults['night_depth'],'black', label="Night Depth (m)")
nax.yticklabels=(arange(0,35,5))
nax.set_ylim(35,0)
pyplot.subplots_adjust(top=0.3)
fig.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
pid = os.getpid()
fname=("output_%s.csv" % pid)
with open(fname,'w') as outfile:
   writer = csv.writer(outfile)
   writer.writerow(BaseResults.keys())
   writer.writerows(zip(*BaseResults.values()))
outfile.close()
pylab.savefig(("new_%s.png" % pid),facecolor=fig.get_facecolor(), edgecolor='lightblue')
data_uri = base64.b64encode(open(("new_%s.png" % pid), 'rb').read()).decode('utf-8').replace('\n', '')
img_tag = '<img class="results" src="data:image/png;base64,{0}">'.format(data_uri)
print(img_tag)

print ('''
    <br>
    <div id="valuewrap">
        <div id="datahead">
            %s, %s
        </div>
        <div id="ftwo">
        <div id="indata">
            <div class="dataleft">Input Values:</div>

            <div class="dataleft">Chinook Starting Mass:
                <div class="dataright">%.1f g</div>
            </div>

            <div class="dataleft">Daphnia Density (m2 surface):
                <div class="dataright">%.0f</div>
            </div>

            <div class="dataleft">Daphnia Size (mm):
                <div class="dataright">%.2f mm</div>
            </div>

            <div class="dataleft">Light Extinction Coefficient:
                <div class="dataright">%.2f</div>
            </div>




       ''' % (FreshBatch.Site,FreshBatch.Year,StartingMass,FreshBatch.TotalDaphnia,FreshBatch.DaphSize,FreshBatch.Light))



print ('''
            </div>

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
                <div class="dataright">%+.2f</div>
                </div>
                <div class="dataleft">Population at which Density Dependent Interactions Expected:
                <div class="dataright">%i</div>
                </div>
            </div>


       <br>
       ''' % (BaseResults['StartingMass'][0],BaseResults['growth'][0],BaseResults['day_depth'][0],BaseResults['night_depth'][0],BaseResults['StartingMass'][29],
              BaseResults['growth'][29],BaseResults['day_depth'][29],daytemp,BaseResults['night_depth'][29],nighttemp,DConsumed,condition,PopEst))

print('''   <div style="margin-top:2px;"><div style="width:600px;display:inline-block;font: normal normal 18px 'Times New Roman', Times, FreeSerif, sans-serif;">
            <div style="float:left;">Daphnia Distribution Year: %s,  Site: %s,  and Month: %s
            </div>

            <div style="float:left;">Temperature Distribution Year: %s,  Site: %s,  and Month: %s
            </div>
            </div>
            ''' %(DYear,DSite,DMonth,TYear,TSite,TMonth))
if depr_flag == "YES":
    print('''<div style="width:600px;display:inline-block;font: normal normal 18px 'Times New Roman', Times, FreeSerif, sans-serif;"><div style="float:left;">Depth restricted to between %.2fm and %.2fm.</div></div>''' % (Dmin,Dmax))
if tempr_flag == "YES":
    print('''<div style="float:left;">Temperature restricted to between %.2f degrees and %.2f degrees.</div>
    ''' % (Tmin, Tmax))

print('''
<br><div style="float:left;">Download Full Results?
                <a href="/{}" download>Download</a>
            </div>

</div>
</div>
<body>
    <h2>Enter Values to GrowChinook</h2>
    <div id="formwrap">
        <form action="RunModel.py" method="post" target="_blank">
           <b>First, enter a Starting Mass for the fish. Then select a default Year, Month, and Site, which will be used to fill in any fields you may choose to leave blank.
           Now you may adjust any values you like, and can at any time reassert the default values for your selected Year, Month, and Site by clicking the "Apply Observed Values" button.</b><br><br>
           <div id="sec1">
                <label>Enter Fish Starting Mass (g):</label><input type="text" name="Starting_Mass_In" id="SMass_TextInID"  oninput="SMassSlide.value = SMass_TextInID.value"> <br><br>
                <p style="text-align:center;width:80%;"><b>Select a Year, Month, and Site to fill Daphnia Density, Daphnia Size, and Light Extinction Coefficient with Observed Values</b>
                <div style="margin:auto;">
                    <label class="dd">Year:</label>
                    <select name="Year" value="2015" id="ddy" onchange="configureDropDownLists(this,document.getElementById('ddm1'),document.getElementById('dds'))">
                        <option value=""></option>
                        <option value="2016">2016</option>
                        <option value="2015">2015</option>
                        <option value="2014">2014</option>
                    </select>
                    <label class="dd">Site:</label>
                    <select name="Site" value="Fall Creek" id="dds">
                    </select>
                    <label class="dd">Month:</label>
                    <select name="Month1" value="June" id="ddm1" onchange="configureMonthDropDowns(this,document.getElementById('ddm2'))">
                    </select><br>
                </div>
                <div style="text-align:center;">
                    <button type="button" onclick="getDefaultValues(document.getElementById('ddy'),document.getElementById('ddm1'),document.getElementById('dds'),document.getElementById('SMass_TextInID'),document.getElementById('TotDDef'),document.getElementById('DaphSDef'),document.getElementById('LightDef'));
                    getDefaultValues(document.getElementById('ddy'),document.getElementById('ddm1'),document.getElementById('dds'),document.getElementById('SMass_TextInID'),document.getElementById('TotDTextInID'),document.getElementById('DaphSTextInID'),document.getElementById('LightTextInID'));">
                    Apply Observed Values
                    </button>
                </div><br>
                Observed:<input class="defdisp" type="text" name="TotDDef" id="TotDDef" value="" readonly><label>Daphnia Density (per m<sup>2</sup> surface)</label>Using:<input type="text" name="Total_Daphnia_Input_Name" id="TotDTextInID" oninput="TotDSlide.value = TotDTextInID.value" oninput="TotDOutID.value = TotDInID.value"> <br><br>
                Observed:<input class="defdisp" type="text" name="LightDef" id="LightDef" value="" readonly><label>Light Extinction Coefficient (Higher is Darker)</label>Using:<input type="text" name="Light" id="LightTextInID" oninput="LightSlide.value = Light.value"><output name="Light_TextOut" id="Light_TextOutID"> </output> <br><br>
                Observed:<input class="defdisp" type="text" name="DaphSDef" id="DaphSDef" value="" readonly><label>Daphnia Size (mm):</label>Using:<input type="text" name="Daphnia Size" id="DaphSTextInID" oninput="DaphSSlide.value = DaphSTextInID.value"> <br><br>
                <div class="deptem" style="float:left;"><p style="margin-top:auto;">
                    <b>Optional: Set to restrict depth</b>
                </div>
                <div style="float:right;width:70%;">
                    <label class="deptem">Maximum Depth (m):</label>
                    <input class="deptem" type="text" name="DmaxIn" id="DmaxInID"><br>
                    <label class="deptem">Minimum Depth (m):</label>
                    <input class="deptem" type="text" name="DminIn" id="DminInID">
                </div>
            </div>
            <div id="sec2">
                <div style="display:inline-block;">
                    <div class="deptem" style="float:left;"><p style="margin-top:auto;">
                        <b>Optional: Set to restrict temperature</b>
                    </div>
                    <div style="float:right;width:70%;">
                        <label class="deptem">Maximum Temperature (Celsius):</label>
                        <input class="deptem" type="text" name="TmaxIn" id="TmaxInID"><br>
                        <label class="deptem">Minimum Temperature (Celsius):</label>
                        <input class="deptem" type="text" name="TminIn" id="TminInID">
                    </div>
                </div>
                <div><br></div>
                <div style="width:80%;">
                    <b>Optional: Select a Year, Month, and Site to apply the corresponding Daphnia distribution curve. 
                       Otherwise, the curve corresponding to the Default Year, Month, and Site will be used.</b>
                    <label class="dd">Daphnia Year:</label>
                    <select name="DYear" id="dddy" onchange="configureDropDownLists(this,document.getElementById('dddm'),document.getElementById('ddds'))">
                        <option value=""></option>
                        <option value="2016">2016</option>
                        <option value="2015">2015</option>
                        <option value="2014">2014</option>
                    </select>
                    <label class="dd">Daphnia Site:</label>
                    <select name="DSite" id="ddds">
                    </select><br>
                    <label class="dd">Daphnia Month:</label>
                    <select name="DMonth" id="dddm">
                    </select>
                    <div><br></div>
                    <div style="margin-top:auto;width:100%;">
                        <b>Optional: Select a Year, Month, and Site to apply the corresponding Daphnia distribution curve.
                           Otherwise, the curve corresponding to the Default Year, Month, and Site will be used.</b>
                        <label class="dd">Temperature Year:</label>
                        <select name="TYear" id="ddty"  onchange="configureDropDownLists(this,document.getElementById('ddtm'),document.getElementById('ddts'))">
                            <option value=""></option>
                            <option value="2016">2016</option>
                            <option value="2015">2015</option>
                            <option value="2014">2014</option>
                        </select>
                        <label class="dd">Temperature Site:</label>
                        <select name="TSite" id="ddts">
                        </select><br>
                        <label class="dd">Temperature Month:</label>
                        <select name="TMonth" id="ddtm">
                        </select><br><br><br>
                    </div>
                    
                    
                </div>
            </div>
            <div style="float:left;">
                <label>Enter Name to Display on Tab:</label>
                <input type="text" style="width:50%;" name="TabName" id="TabNameID">
            </div><br>
            <div style="display:inline-block;margin:auto;width:75%">
                <div id="subutt" style="float:right;">
                    <input type="submit" value="Submit"/>
                </div>
            <div>Select Site for Population Estimate
            <select name="ESite" id="ddes">
                        <option value=""></option>
                        <option value="Fall Creek">Fall Creek</option>
                        <option value="Hills Creek">Hills Creek</option>
                        <option value="Lookout Point">Lookout Point</option>
                    </select>
            </div>
            <br>
            <div style="float:left;">
                <label>Enter Elevation for Population Estimate (ft):</label>
                <input type="text" style="width:25%;" name="Elev" id="ElevID">
            </div><br>
        </div>
    </form>
<div style="float:left;">Download Temperature Template to Use Custom Temps
                        <a href="/TemperatureTemplate.csv" download>Temperature Template</a>
    <form action = "/upload.py" method="POST" enctype="multipart/form-data">
    <input type="file" name="filename">
    <input type="submit" value="Upload">
    </form>
                    </div>
    <br>

</body>
''' .format(fname,Year,Site,Month))
print ('</html>')


os.remove(("new_%s.png" % pid))

quit()