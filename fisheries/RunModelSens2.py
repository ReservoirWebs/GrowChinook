#!/usr/bin/python

import os, time
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
from matplotlib.font_manager import FontProperties
from scipy.interpolate import griddata
import pandas
cgitb.enable()
Scruffy()

address = cgi.escape(os.environ["REMOTE_ADDR"])
script = "Advanced Sensitivity Run Page"
with open('userlog.csv', 'a') as log:
    log.write("IP: {}," .format(address))
    log.write("Page: {}," .format(script))
    log.write("Time: {}," .format(time.ctime(time.time())))
    log.write('\n')
log.closed

def RunSens(Site, Month1, Month2, Year, Light, DaphSize, Total_Daphnia, StartingMass, Dmax, Dmin,Tmax,Tmin,largestout,oldresults,oldresults1):
    SensOutPer = []
    SensOutPerD1 = []
    SensInputs = []
    numskips = 0
    month = Month1
    Growths1 = []
    Growths = []
    Light,Total_Daphnia,DaphSize = GetVals(Light,Total_Daphnia,DaphSize,Site,month,Year)

    if SensParam == 'Starting Mass':
        Sparam = StartingMass
        FreshBatch = Batch(Site, month, Year, Light, DaphSize, Total_Daphnia, StartingMass, Dmax,Dmin,Tmax,Tmin,TempCurve,DYear,DMonth,DSite)
        results = []
        BaseResults, DConsumed, condition, condition1 = FreshBatch.Run_Batch()
        batches = []
        for i in range(11):
            sensIn = float(Sparam * (SensFactors[i])/100 + Sparam)
            if (sensIn < 0.0):
                SensInputs.append(.0001)
            else:
                SensInputs.append(sensIn)
            csvheaders[i] = [Site, month, Year, ("%s: %f" % ("Starting Mass", SensInputs[i]))]
            batches.append(Batch(Site, month, Year, Light, DaphSize, Total_Daphnia, SensInputs[i],Dmax,Dmin,Tmax,Tmin,TempCurve,DYear,DMonth,DSite))
            res, taway, condition, condition1 = batches[i].Run_Batch()
            results.append(res)
            SensOutPer.append(results[i]['growth'][29])
            SensOutPerD1.append(results[i]['growth'][0])
            Growths.append(results[i]['growth'][29])
            Growths1.append(results[i]['growth'][0])

    elif SensParam == 'Total Daphnia':
        Sparam = Total_Daphnia
        FreshBatch = Batch(Site, month, Year, Light, DaphSize, Total_Daphnia, StartingMass, Dmax,Dmin,Tmax,Tmin,TempCurve,DYear,DMonth,DSite)
        results = []
        BaseResults, DConsumed, condition, condition1 = FreshBatch.Run_Batch()
        batches = []
        for z in range(11):
            sensIn = float(Sparam * (SensFactors[z]/100) + Sparam)
            if (sensIn < 0.0):
                SensInputs.append(.0001)
            else:    
                SensInputs.append(sensIn)
            newbatch = Batch(Site, month, Year, Light, DaphSize, SensInputs[z], StartingMass,Dmax,Dmin,Tmax,Tmin,TempCurve,DYear,DMonth,DSite)
            csvheaders[z] = [Site, month, Year, ("%s: %f" % ("Total Daphnia", SensInputs[z]))]
            batches.append(newbatch)
            res, taway, condition, condition1 = batches[z].Run_Batch()
            results.append(res)
            SensOutPer.append(100 * ((results[z]['growth'][29] - BaseResults['growth'][29]) / BaseResults['growth'][29]))
            SensOutPerD1.append(100 * ((results[z]['growth'][0] - BaseResults['growth'][0]) / BaseResults['growth'][0]))
            Growths.append(results[z]['growth'][29])
            Growths1.append(results[z]['growth'][0])
            
    elif SensParam == 'Daphnia Size':
        Sparam = DaphSize
        FreshBatch = Batch(Site, month, Year, Light, DaphSize, Total_Daphnia, StartingMass, Dmax,Dmin,Tmax,Tmin,TempCurve,DYear,DMonth,DSite)
        results = []
        BaseResults, DConsumed, condition, condition1 = FreshBatch.Run_Batch()
        batches = []
        for i in range(11):
            sensIn = float(Sparam * (SensFactors[i]/100) + Sparam)
            if (sensIn > 0.0):    
                SensInputs.append(sensIn)
                batches.append(Batch(Site, month, Year, Light, SensInputs[i], Total_Daphnia, StartingMass,Dmax,Dmin,Tmax,Tmin,TempCurve,DYear,DMonth,DSite))
                csvheaders[i] = [Site, month, Year, ("%s: %f" % ("Daphnia Size", SensInputs[i]))]
                res, taway, condition, condition1 = batches[i].Run_Batch()
                results.append(res)
                SensOutPer.append(100 * ((results[i]['growth'][29] - BaseResults['growth'][29]) / BaseResults['growth'][29]))
                SensOutPerD1.append(100 * ((results[i]['growth'][0] - BaseResults['growth'][0]) / BaseResults['growth'][0]))
                Growths.append(results[i]['growth'][29])
                Growths1.append(results[i]['growth'][0])
            else:
                numskips = numskips + 1
                SensInputs.append(None)
                batches.append(None)
                results.append(None)
                SensOutPer.append(None)
                SensOutPerD1.append(None)
                Growths.append(None)
                Growths1.append(None)

    elif SensParam == 'K':
        Sparam = Light
        FreshBatch = Batch(Site, month, Year, Light, DaphSize, Total_Daphnia, StartingMass, Dmax,Dmin,Tmax,Tmin,TempCurve,DYear,DMonth,DSite)
        results = []
        BaseResults, DConsumed, condition, condition1 = FreshBatch.Run_Batch()
        batches = []
        for i in range(11):
            sensIn = float(Sparam * (SensFactors[i]/100) + Sparam)
            if (sensIn > 0.0):    
                SensInputs.append(sensIn)
                batches.append(Batch(Site, month, Year, SensInputs[i], DaphSize, Total_Daphnia, StartingMass,Dmax,Dmin,Tmax,Tmin,TempCurve,DYear,DMonth,DSite))
                csvheaders[i] = [Site, month, Year, ("%s: %f" % ("LEC(k)", SensInputs[i]))]
                res, taway, condition, condition1 = batches[i].Run_Batch()
                results.append(res)
                SensOutPer.append(100 * ((results[i]['growth'][29] - BaseResults['growth'][29]) / BaseResults['growth'][29]))
                SensOutPerD1.append(100 * ((results[i]['growth'][0] - BaseResults['growth'][0]) / BaseResults['growth'][0]))
                Growths.append(results[i]['growth'][29])
                Growths1.append(results[i]['growth'][0])
            else:
                numskips = numskips + 1
                SensInputs.append(None)
                batches.append(None)
                results.append(None)
                SensOutPer.append(None)
                SensOutPerD1.append(None)
                Growths.append(None)
                Growths1.append(None)

#    for i in range(len(SensFactors)):
#        if abs(SensFactors[i]) > abs(largestout):
#            largestout = abs(SensFactors[i])
#    for i in range(len(SensOutPer)):
#        if abs(SensOutPer[i]) > abs(largestout):
#            largestout = abs(SensOutPer[i])

    with open(fname, 'a') as outfile:
        writer = csv.writer(outfile)
        l = 0
        for batch in results:
            writer.writerow(csvheaders[l])
            if batch != None:
                writer.writerow(batch.keys())
                writer.writerows(zip(*batch.values()))
            l = l + 1
    outfile.close()

    #ax.plot(SensFactors, SensOutPerD1,label=("%s" % month))
    #ax1.plot(SensFactors,SensOutPer, label=("%s" % month))
    ax2.plot(SensInputs,Growths1,label=("%s" % month))
    ax3.plot(SensInputs, Growths, label=("%s" % month))
    oldresults = SensOutPer
    oldresults1 = SensOutPerD1
    return largestout,oldresults,oldresults1,SensInputs

matplotlib.rcParams.update({'font.size': 12})
form = cgi.FieldStorage()
# Get data from fields

StartingMass = form.getvalue('Starting_Mass_In')
if StartingMass != None:
    StartingMass=float(StartingMass)
else:
    StartingMass = 40
DYear = form.getvalue('DYear')
DMonth = form.getvalue('DMonth')
DSite = form.getvalue('DSite')

DYear = '2015'
DMonth = 'June'
DSite = 'Fall Creek'

TempCurve = '{0}_smoothed_{1}_{2}.csv'.format(form.getvalue('TSite'), form.getvalue('TMonth'), form.getvalue('TYear'))

if form.getvalue('defa') == 'yes':
    def_flag = 'YES'
else:
    def_flag = 'NO'

if form.getvalue('depr') == 'yes':
    depr_flag = 'YES'
else:
    depr_flag = 'NO'
if form.getvalue('tempr') == 'yes':
    tempr_flag = 'YES'
else:
    tempr_flag = 'NO'
if tempr_flag == 'YES':
    Tmax = float(form.getvalue('TmaxIn'))
    Tmin = float(form.getvalue('TminIn'))
else:
    Tmax = 10000
    Tmin = -1

Total_Daphnia = form.getvalue('Total_Daphnia_Input_Name')
if Total_Daphnia != None:
    Total_Daphnia = float(Total_Daphnia)
DaphSize  = form.getvalue('Daphnia Size')
if DaphSize != None:
    DaphSize = float(DaphSize)
Light = form.getvalue('Light')
if Light != None:
    Light = float(Light)
Year = form.getvalue('Year')
Site = form.getvalue('Site')

if depr_flag == 'YES':
    Dmax = float(form.getvalue('DmaxIn'))
    Dmin = float(form.getvalue('DminIn'))
else:
    Dmax = 10000
    Dmin = -1



print ('Content-type:text/html; charset=utf-8\r\n\r\n')
print ('<html>')
print('''<link type="text/css" rel="stylesheet" media="screen" href="/css/Style.css" />
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
        <li><a class="current" href="http://cas-web0.biossys.oregonstate.edu/TestSens2.py">Run Advanced Sensitivity</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSumm.py">Run Multiple Months</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/Curves.html">Temperature and Daphnia Curves</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/about.html">About</a></li>
    </ul>''')
print ('<head>')
print ('<title>Here are Your Results.</title>')
print ('</head>')

largestout = 0.0
batches = []
Years = ['2013','2014','2015']
Sites2013 = ['Lookout Point', 'Fall Creek', 'Hills Creek']
Sites2014 = ['Lookout Point', 'Fall Creek', 'Hills Creek']
Sites2015 = ['Lookout Point', 'Fall Creek', 'Hills Creek']
Months2013 = ['June','July']
Months2014 = ['June', 'July', 'August']
Months2015 = ['March', 'April', 'May', 'June', 'July', 'August']
AllMonths = [Months2013,Months2014,Months2015]
pid = os.getpid()
fname=("output_%s.csv" % pid)
Growths = []
Growths1=[]

SensFactors = []
Sparam_Range = 3
SensParam = form.getvalue('Sens_Param')
if form.getvalue('Sparam_Range') != None:
    Sparam_Range = float(form.getvalue('Sparam_Range'))
else:
   Sparam_Range = 1
SensFactors = Sensitivity_Expand(Sparam_Range, SensFactors)
for i in range(len(SensFactors)):
    SensFactors[i] = SensFactors[i] * 100

fig=pyplot.figure(facecolor='#c8e9b1')
#ax1 = fig.add_subplot(222)
fontP = FontProperties()
fontP.set_size('small')
#if SensParam == 'Starting Mass':
#    ax1.set_ylabel('Final Growth Rate')
#else:
#    ax1.set_ylabel('Final % Change Growth Rate')
#ax.set_aspect('equal', adjustable='box')
#ax1.set_xlabel('Percent Change in %s' % SensParam)
#ax1.xaxis.set_major_formatter(FormatStrFormatter('%i'))
#ax1.grid()
#ax = fig.add_subplot(221)
#if SensParam == 'Starting Mass':
#    ax.set_ylabel('Day 1 Growth Rate')
#else:
#    ax.set_ylabel('Day 1 % Change Growth Rate')
#ax.set_aspect('equal', adjustable='box')
#ax.set_xlabel('Percent Change in %s' % SensParam)
#ax.xaxis.set_major_formatter(FormatStrFormatter('%i'))
#ax.grid()
fig.suptitle('Spring Chinook', fontsize=20)
ax2 = fig.add_subplot(211)
if SensParam == 'Starting Mass':
    ax2.set_ylabel('Day 1 Growth Rate')
else:
    ax2.set_ylabel('Day 1 Growth Rate')
#ax.set_aspect('equal', adjustable='box')
if SensParam == 'Starting Mass':
    ax2.set_xlabel('Starting Mass')
elif SensParam == 'Total Daphnia':
    ax2.set_xlabel('Total Daphnia (Thousands)')
else:
    ax2.set_xlabel('%s' % SensParam)
if SensParam != 'Starting Mass':
    ax2.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
else:
    ax2.xaxis.set_major_formatter(FormatStrFormatter('%i'))
ax2.grid()
ax3 = fig.add_subplot(212)
if SensParam == 'Starting Mass':
    ax3.set_ylabel('Final Growth Rate')
else:
    ax3.set_ylabel('Final Growth Rate')
#ax.set_aspect('equal', adjustable='box')
if SensParam == 'Starting Mass':
    ax3.set_xlabel('Starting Mass')
elif SensParam == 'Total Daphnia':
    ax3.set_xlabel('Total Daphnia (Thousands)')
else:
    ax3.set_xlabel('%s' % SensParam)
if SensParam != 'Starting Mass':
    ax3.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
else:
    ax3.xaxis.set_major_formatter(FormatStrFormatter('%i'))
ax3.grid()
#if SensParam == 'Starting Mass':
#    ax1.set_ylabel('Day 1 Growth Rate')
#else:
#    ax1.set_ylabel('% Change Final Growth Rate')
#ax1.set_aspect('equal', adjustable='box')
#ax1.set_xlabel('Percent Change in %s' % SensParam)
#ax1.xaxis.set_major_formatter(FormatStrFormatter('%i'))

oldresults = []
oldresults1 = []
Sites = []
Months = []
csvheaders=[[] for i in range(11)]
try:
    if Year == '2015':
        for m in (Months2015):
            largestout,oldresults,oldresults1,SensInputs = RunSens(Site, m, m,Year, Light, DaphSize, Total_Daphnia, StartingMass, Dmax, Dmin,Tmax,Tmin,largestout,oldresults,oldresults1)
    elif Year == '2014':
        for m in (Months2014):
            largestout,oldresults,oldresults1,SensInputs = RunSens(Site, m, m,Year, Light, DaphSize, Total_Daphnia, StartingMass, 1000, -1,largestout,oldresults,oldresults1)
    elif Year == '2013':
        for m in (Months2013):
            largestout,oldresults,oldresults1,SensInputs = RunSens(Site, m, m,Year, Light, DaphSize, Total_Daphnia, StartingMass, 1000, -1,largestout,oldresults,oldresults1)
except:
    print 'Content-Type: text/html'
    print 'Location: http://cas-web0.biossys.oregonstate.edu/error.html'
    print # HTTP says you have to have a blank line between headers and content
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

#if SensParam == 'Total Daphnia':
#    for m in (Months2015):        
#        largestout,oldresults,oldresults1,SensInputs = RunSens(Site, m, m,Year, None, None, Total_Daphnia, StartingMass, 1000, -1,largestout,oldresults,oldresults1)
#if SensParam == 'Daphnia Size':
#    for m in (Months2015):        
#        largestout,oldresults,oldresults1,SensInputs = RunSens(Site, m, m,Year, None, DaphSize, None, StartingMass, 1000, -1,largestout,oldresults,oldresults1)
#if SensParam == 'K':
#    for m in (Months2015):        
#        largestout,oldresults,oldresults1,SensInputs = RunSens(Site, m, m,Year, Light, None, None, StartingMass, 1000, -1,largestout,oldresults,oldresults1)

art = []
lgd = pylab.legend(prop = fontP,loc=9, bbox_to_anchor=(0.5, -0.1), ncol=3)
pyplot.gcf().subplots_adjust(bottom=0.35)
art.append(lgd)
fig.tight_layout(pad=2, h_pad=None, w_pad=None, rect=None)
pylab.savefig( "new.png",facecolor=fig.get_facecolor(), edgecolor='lightblue')
data_uri = base64.b64encode(open('new.png', 'rb').read()).decode('utf-8').replace('\n', '')    
img_tag = '<img class="results" src="data:image/png;base64,{0}">'.format(data_uri)
print(img_tag)
'''
print (
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
        % (FreshBatch.Site,FreshBatch.Year,Month,StartingMass,Month,FreshBatch.TotalDaphnia,Month,FreshBatch.DaphSize,Month,FreshBatch.Light))
'''
if depr_flag == "YES":
    print('''Depth restricted to between %.2fm and %.2fm.<br>''' % (Dmin,Dmax))

'''  </div>
            <div id="outdata">
                <div class="dataleft">Output Values:</div>
                <div class="dataleft">%s Final Mass at +%.0f percent:
                    <div class="dataright">%.1f g</div>
                </div>
                <div class="dataleft">%s Final Mass at -%.0f percent:
                    <div class="dataright">%.1f g</div>
                </div>
                <div class="dataleft">%s Final Daily Growth:
                    <div class="dataright">%.1f g/g/day</div>
                </div>
                <div class="dataleft">%s Final Day Depth:
                    <div class="dataright">%.0f m</div>
                </div>
                <div class="dataleft">%s Final Night Depth:
                    <div class="dataright">%.0f m</div>
                </div>
                <div class="dataleft">%s Total Daphnia Consumed:
                    <div class="dataright">%.0f</div>
                </div>
            </div>
       </div>
       </div><br>
        % (Month,SensFactors[10],results[10][0]['StartingMass'][29],Month,SensFactors[10],results[0][0]['StartingMass'][29],Month,BaseResults['growth'][29],Month,BaseResults['day_depth'][29],Month,BaseResults['night_depth'][29],Month,DConsumed))
'''

print('''<div style="display:block; margin-left:auto; margin-right:auto;">Download Full Results?
                <a href="/cgi-bin/{}" download>Download</a>
            </div>
'''.format(fname))

print('''
<script type="text/javascript">
    function configureDropDownLists(ddy,ddm,dds) {
    var years = ['2013', '2014', '2015'];
    var months = ['March', 'April', 'May', 'June', 'July', 'August'];
    var sites = ['Blue River', 'Fall Creek', 'Hills Creek', 'Lookout Point'];
    switch (ddy.value) {
        case '2013':
            ddm.options.length = 0;
            createOption(ddm, months[3], months[3]);
            createOption(ddm, months[5], months[5]);
            dds.options.length = 0;
            for (i=0; i<3; i++) {
                createOption(dds,sites[i],sites[i]);
            }
            break;
        case '2014':
            ddm.options.length = 0;
        for (i = 3; i < months.length; i++) {
            createOption(ddm, months[i], months[i]);
            }
        dds.options.length = 0;
        for (i=1; i<sites.length; i++) {
                createOption(dds,sites[i],sites[i]);
            }
            break;
        case '2015':
            ddm.options.length = 0;
            for (i = 0; i < months.length; i++) {
                createOption(ddm, months[i], months[i]);
            }
            dds.options.length = 0;
            for (i=1; i<sites.length; i++) {
                createOption(dds,sites[i],sites[i]);
            }
            break;
        default:
            ddm.options.length = 0;
        break;
    }
}
    function createOption(dd, text, value) {
        var opt = document.createElement('option');
        opt.value = value;
        opt.text = text;
        dd.options.add(opt);
    }
</script>
<script>
function updateDepthTextInput(val) {
          document.getElementById('DMaxInID').value=val;
          document.getElementById('DmaxOutID').value=val;
          document.getElementById('DMinInID').value=val;
          document.getElementById('DminOutID').value=val;
        }
</script>
<script>
function updateSMassInput(val) {
          document.getElementById('SMass_TextInID').value=val;
        }
</script>
<script>
function updateDaphSText(val) {
          document.getElementById('DaphSTextInID').value=val;
        }
</script>
<script>
function updateTotDTextInput(val) {
          document.getElementById('TotDTextInID').value=val;
        }
</script>
<script>
function updateLightTextInput(val) {
          document.getElementById('LightTextInID').value=val;
        }
</script>
<body>
    
    <h2>Enter Values to GrowChinook</h2>
    <div id="formwrap">
        <form action="RunModelSens2.py" method="post" target="_blank">

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
                    <br><br><br>
</div>
 <br><b>Enter a Starting Mass for the fish. Then Select a Year and Site. The model will run sensitivity analysis of all months available for the selected Year and Month.</b>

           <div id="sec1" style="display:inline-block;">
                <div>
                    <label>Enter Fish Starting Mass (g):</label><input type="text" name="Starting_Mass_In" id="SMass_TextInID"  oninput="SMassSlide.value = SMass_TextInID.value">
                </div>
                <div style="text-align:center;width:80%;"><b>Select a Year and Site to run analysis for.</b></div>
                <div style="margin:auto;display:inline-block;float:left;width:100%;">
                    <div style="width:45%;float:left;">
                    <label>Select Year:</label> <select name="Year" id="ddy" onchange="configureDropDownLists2(this,document.getElementById('dds'))">
                        <option value=""></option>
                        
                        <option value="2014">2014</option>
                        <option value="2015">2015</option>
                        </select>
                    </div>
                    <div style="width:45%;float:right;">
                        <label>Select Site:</label> <select name="Site" id="dds">
                        </select>
                    </div>



                <div><br><br><label>Daphnia Density (per m<sup>2</sup> surface)</label>Using:<input type="text" name="Total_Daphnia_Input_Name" id="TotDTextInID" oninput="TotDSlide.value = TotDTextInID.value" oninput="TotDOutID.value = TotDInID.value"> <br><br>
                <label>Light Extinction Coefficient</label>Using:<input type="text" name="Light" id="LightTextInID" oninput="LightSlide.value = Light.value"><output name="Light_TextOut" id="Light_TextOutID"> </output> <br><br>
                <label>Daphnia Size (mm):</label>Using:<input type="text" name="Daphnia Size" id="DaphSTextInID" oninput="DaphSSlide.value = DaphSTextInID.value"> <br><br>
                </div>
                </div>


            </div>
            <div id="sec2">
                <br>
                <div style="display:inline-block;">
                <div class="deptem" style="float:left;width:30%;"><p style="margin-top:auto;"><b>Optional: Set to restrict temperature</b></div>
                <div style="float:right;width:70%;">
		        <label class="deptem">Maximum Temperature:</label><input class="deptem" type="text" name="TmaxIn" id="TmaxInID"><br>
                <label class="deptem">Minimum Temperature:</label><input class="deptem" type="text" name="TminIn" id="TminInID">
                </div>
                </div>
                <div><br></div>
                <div class="deptem" style="float:left;width:30%;"><p style="margin-top:auto;"><b>Optional: Set to restrict depth</b></div>
                <div style="float:right;width:70%;">
		        <label class="deptem">Maximum Depth:</label><input class="deptem" type="text" name="DmaxIn" id="DmaxInID"><br>
                <label class="deptem">Minimum Depth:</label><input class="deptem" type="text" name="DminIn" id="DminInID">
                </div>

              		    <div id="subutt">
                        <input type="submit" value="Submit"/>
                    </div>
        </form>
    </div>
</body>
''')

os.remove('new.png')
quit()