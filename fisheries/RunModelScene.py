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
Elev = form.getvalue('Elev')
Year = form.getvalue('Year')
if Year == None:
    Year = "2015"
Month = form.getvalue('Month1')
if Month == None:
    Month = "June"
Site = form.getvalue('Site')
if Site == None:
    Site = "Fall Creek"

Light = form.getvalue('Light')
if Light != None:
    Light = float(Light)
Total_Daphnia = form.getvalue('Total_Daphnia_Input_Name')
if Total_Daphnia != None:
    Total_Daphnia = float(Total_Daphnia)
DaphSize = form.getvalue('Daphnia Size')
if DaphSize != None:
    DaphSize = float(form.getvalue('Daphnia Size'))

TempCurve = None
DYear = Year
DMonth = Month
DSite = Site
TYear = Year
TMonth = Month
TSite = Site
Dmax = 1000
Dmin = -1
Tmax = 1000
Tmin = -1

StartingMass = form.getvalue('Starting_Mass_In')
if StartingMass != None:
    StartingMass=float(StartingMass)
else:
    StartingMass = 40

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
        <li><a href="http://cas-web0.biossys.oregonstate.edu/Test.py">Run Standard Model</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSens.py">Run Model With Sensitivity</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSens2.py">Run Advanced Sensitivity</a></li>
        <li><a class="current" href="http://cas-web0.biossys.oregonstate.edu/scene.py">Run Scenarios</a><li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSumm.py">Run Multiple Months</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/Curves.html">Temperature and Daphnia Curves</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/about.html">About</a></li>
    </ul>''')

Scenario=form.getvalue('Scene')
if Scenario == 'CM':
    Year = '2014'
    DYear = '2014'
    TYear = '2014'
    TempCurve = '{0}_T_{1}_{2}.csv'.format(Site, Month, Year)
    if Site == 'Fall Creek':
        TempCurve = '{0}_T_{1}_{2}.csv'.format('Hills Creek', form.getvalue('Month1'), Year)
        TYear = '2014'
        Light,Total_Daphnia2,DaphSize2 = GetVals(Light,Total_Daphnia,DaphSize,'Hills Creek',Month,'2014')
        print(Light)
        TMonth = Month
        TSite = 'Hills Creek'
        Light2,Total_Daphnia,DaphSize = GetVals(Light,Total_Daphnia,DaphSize,Site,Month,Year)
        
elif Scenario == 'WSBDD': #Uses user selection for Daphnia data, Fall Creek 2016 for light and temp
    TYear = '2016'
    TempCurve = '{0}_T_{1}_{2}.csv'.format('Fall Creek', form.getvalue('Month1'), '2016')
    TYear = '2016'
    TMonth = Month
    TSite = 'Fall Creek'
    Light = None
    Total_Daphnia = None
    DaphSize = None
    Light,Total_Daphnia2,DaphSize2 = GetVals(Light,Total_Daphnia,DaphSize,'Fall Creek',Month,'2016')
    Light2,Total_Daphnia, DaphSize = GetVals(Light,Total_Daphnia,DaphSize,Site,Month,Year)
    
elif Scenario == 'STD':
    if Site == 'Hills Creek':
        Year = '2015' #Change to 2016 once 2016 data in
        Dmax = 10
    elif Site == 'Fall Creek' or 'Lookout Point':
        Year = '2015'
        Dmax = 10

elif Scenario == 'MYD':
    Year = '2015'
    Dmax = 15

elif Scenario == 'WWP2015':
    Year = '2015'
    Tmax = 20

elif Scenario == 'IP22015':
    Year = '2015'
    Light,Total_Daphnia,DaphSize = GetVals(Light,Total_Daphnia,DaphSize,Site,Month,Year)
    Total_Daphnia = 2*(Total_Daphnia)
elif Scenario == 'IP102015':
    Year = '2015'
    Light,Total_Daphnia,DaphSize = GetVals(Light,Total_Daphnia,DaphSize,Site,Month,Year)
    Total_Daphnia = 10*(Total_Daphnia)

elif Scenario == 'DR':
    Light,Total_Daphnia,DaphSize = GetVals(Light,Total_Daphnia,DaphSize,Site,Month,Year)
else:
    Light,Total_Daphnia,DaphSize = GetVals(Light,Total_Daphnia,DaphSize,Site,Month,Year)

if TempCurve == None:
    TempCurve = '{0}_T_{1}_{2}.csv'.format(Site, Month, Year)
DYear = '2015' #remove once 2014 plankton data added
Light,Total_Daphnia,DaphSize = GetVals(Light,Total_Daphnia,DaphSize,Site,Month,Year)
print(Light,Total_Daphnia,DaphSize)
FreshBatch = Batch(Site, Month, Year, Light, DaphSize, Total_Daphnia, StartingMass, Dmax, Dmin,Tmax,Tmin,TempCurve,DYear,DMonth,DSite,None,None)
BaseResults,DConsumed,condition,condition1,dt,nt,PopEst  = FreshBatch.Run_Batch()
'''
except:    
    print 'Content-Type: text/html'
    print 'Location: http://cas-web0.biossys.oregonstate.edu/error.html'
    print 
    print '<html>'
    print '  <head>'
    print '    <meta http-equiv="refresh" content="0;url=http://cas-web0.biossys.oregonstate.edu/error.html" />'
    print '    <title>You are going to be redirected</title>'
    print '  </head>' 
    print '  <body>'
    print '    Redirecting... <a href="http://cas-web0.biossys.oregonstate.edu/error.html">Click here if you are not redirected</a>'
    print '  </body>'
    print '</html>'
    cgitb.handler()
'''

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
                <div class="dataright">%.2f</div>
                </div>
            </div>


       <br>
       ''' % (BaseResults['StartingMass'][0],BaseResults['growth'][0],BaseResults['day_depth'][0],BaseResults['night_depth'][0],BaseResults['StartingMass'][29],
              BaseResults['growth'][29],BaseResults['day_depth'][29],dt,BaseResults['night_depth'][29],nt,DConsumed,condition))

print('''   <div style="margin-top:2px;"><div style="width:600px;display:inline-block;font: normal normal 18px 'Times New Roman', Times, FreeSerif, sans-serif;">
            <div style="float:left;">Daphnia Distribution Year: %s,  Site: %s,  and Month: %s
            </div>

            <div style="float:left;">Temperature Distribution Year: %s,  Site: %s,  and Month: %s
            </div>
            </div>
            ''' %(DYear,DSite,DMonth,TYear,TSite,TMonth))

print('''
<br><div style="float:left;">Download Full Results?
                <a href="/{}" download>Download</a>
            </div>

</div>
</div>
<body>
    <h2>Enter Values to GrowChinook</h2>
    <div id="formwrap">
        <b>First, enter a Starting Mass for the fish. Then select a default Year, Month, and Site, which will be used to fill in any fields you may choose to leave blank.
           Now you may adjust any values you like, and can at any time reassert the default values for your selected Year, Month, and Site by clicking the "Apply Observed Values" button.</b><br><br>
                <label>Enter Fish Starting Mass (g):</label><input type="text" name="Starting_Mass_In" id="SMass_TextInID"  oninput="SMassSlide.value = SMass_TextInID.value"> <br><br>
                
        <p style="text-align:center;width:80%;"><b>Select a Scenario</b>
        <select name="Scene" value="" id="ddscene" onclick="configureSceneMonths(this,document.getElementById('ddm1'))">
                        <option value=""></option>
                        <option value="CM">Conventional Management</option>
                        <option value="WSBDD">Winter Stream Bed Drawdown</option>
                        <option value="STD">Short-Term Drought or Drawdown for Repairs</option>
                        <option value="MYD">Multi-Year Drought</option>
                        <option value="WWP2015">Warm-water Predators 2015</option>
                        <option value="IP22015">Increased Productivity 2015 (2x)</option>
                        <option value="IP102015">Increased Productivity 2015 (10x)</option>
                        <option value="DR">Delayed Refill</option>
        </select>
        <p style="text-align:center;width:80%;"><b>Select a Year, Month, and Site to fill Daphnia Density, Daphnia Size, and Light Extinction Coefficient with Observed Values</b>
                <div style="margin:auto;">
                    <label class="dd">Site:</label>
                    <select name="Site" value="" id="dds">
                        <option value=""></option>
                        <option value="Fall Creek">Fall Creek</option>
                        <option value="Hills Creek">Hills Creek</option>
                        <option value="Lookout Point">Lookout Point</option>
                    </select>
                    <label class="dd">Month:</label>
                    <select name="Month1" value="" id="ddm1" onchange="getDefaultValuesScene(document.getElementById('ddscene'),document.getElementById('ddy'),document.getElementById('ddm1'),document.getElementById('dds'),document.getElementById('SMass_TextInID'),document.getElementById('TotDDef'),document.getElementById('DaphSDef'),document.getElementById('LightDef'));
                                                                       getDefaultValuesScene(document.getElementById('ddscene'),document.getElementById('ddy'),document.getElementById('ddm1'),document.getElementById('dds'),document.getElementById('SMass_TextInID'),document.getElementById('TotDTextInID'),document.getElementById('DaphSTextInID'),document.getElementById('LightTextInID'));">
                    <option value=""></option>
                        <option value="March">March</option>
                        <option value="April">April</option>
                        <option value="May">May</option>
                        <option value="June">June</option>
                        <option value="July">July</option>
                        <option value="August">August</option>
                    </select><br>
                
                Observed:<input class="defdisp" type="text" name="TotDDef" id="TotDDef" value="" readonly><label>Daphnia Density (per m<sup>2</sup> surface)</label>Using:<input type="text" name="Total_Daphnia_Input_Name" id="TotDTextInID" oninput="TotDSlide.value = TotDTextInID.value" oninput="TotDOutID.value = TotDInID.value"> <br><br>
                Observed:<input class="defdisp" type="text" name="LightDef" id="LightDef" value="" readonly><label>Light Extinction Coefficient (Higher is Darker)</label>Using:<input type="text" name="Light" id="LightTextInID" oninput="LightSlide.value = Light.value"><output name="Light_TextOut" id="Light_TextOutID"> </output> <br><br>
                Observed:<input class="defdisp" type="text" name="DaphSDef" id="DaphSDef" value="" readonly><label>Daphnia Size (mm):</label>Using:<input type="text" name="Daphnia Size" id="DaphSTextInID" oninput="DaphSSlide.value = DaphSTextInID.value"> <br><br>
                            </div>

            <div style="display:inline-block;margin:auto;width:75%">
                
            <div style="float:left;">
                <label>Enter Name to Display on Tab:</label>
                <input type="text" style="width:50%;" name="TabName" id="TabNameID">
            </div><br>
            <div id="subutt" style="float:right;">
                    <input type="submit" value="Submit"/>
                </div>
        </div>
    </form>
</body>
''' .format(fname))
print ('</html>')


os.remove(("new_%s.png" % pid))

quit()