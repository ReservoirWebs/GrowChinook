#!C:\Anaconda3\python.exe

import os
import sys
import csv
from Bioenergetics import *
import cgi, cgitb
import pylab
import io
from PIL import Image, ImageDraw
import base64
from scipy.interpolate import griddata
import pandas
import seaborn
cgitb.enable()
os.chdir(r'C:\xampp\cgi-bin')

def Sensitivity_Expand(Sparam_Range, Sparam_Exp):
    step_size = Sparam_Range/5
    Sparam_Range = Sparam_Range*-1
    for i in range(0,11):
        Sparam_Exp.append(Sparam_Range)
        Sparam_Range = Sparam_Range + step_size
    return Sparam_Exp


form = cgi.FieldStorage()
# Get data from fields

StartingMass = 60
if form.getvalue('sens') == 'yes':
    sens_flag = 'YES'
else:
    sens_flag = 'NO'

if form.getvalue('defa') == 'yes':
    def_flag = 'YES'
else:
    def_flag = 'NO'

if form.getvalue('depr') == 'yes':
    depr_flag = 'YES'
else:
    depr_flag = 'NO'

if def_flag == 'YES':
    Total_Daphnia = None
    DaphSize = None
    Month = form.getvalue('Month')
    Light = None
    Year = form.getvalue('Year')
    Site = form.getvalue('Site')
    if depr_flag == 'NO':
        Dmax = 50.0
        Dmin = -1.0
    else:
        Dmax = float(form.getvalue('DmaxIn'))
        Dmin = float(form.getvalue('DminIn'))
else:
    Total_Daphnia = float(form.getvalue('Total_Daphnia_Input_Name'))
    DaphSize  = float(form.getvalue('Daphnia Size'))
    Light = float(form.getvalue('Light'))
    Month = form.getvalue('Month')
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
print('<link type="text/css" rel="stylesheet" media="screen" href="/css/Style2.css" />')
print ('<head>')
print ('<title>Here are Your Results.</title>')
print ('</head>')

FreshBatch = Batch(Site, Month, Year, Light, DaphSize, Total_Daphnia, StartingMass, Dmax, Dmin)
BaseResults,DConsumed  = FreshBatch.Run_Batch()

if sens_flag == 'YES':
    largestout = 0.0
    batches = []
    results = []
    SensInputs = []
    SensFactors = []
    SensOutPer = []
    Sparam_Range = float(form.getvalue('Sparam_Range'))
    SensParam = form.getvalue('Sens_Param')
    SensFactors = Sensitivity_Expand(Sparam_Range, SensFactors)

    if SensParam == 'Starting Mass':
        figname = 'SMass.pdf'
        Sparam = StartingMass
        for i in range(11):
            SensInputs.append(Sparam * SensFactors[i] + Sparam)
            SensFactors[i] = SensFactors[i] * 100
            batches.append(Batch(Site, Month, Year, Light, DaphSize, Total_Daphnia, SensInputs[i],Dmax,Dmin))
            results.append(batches[i].Run_Batch())
            print(results[i][0]['growth'][29])
            SensOutPer.append(100 * ((results[i][0]['growth'][29] - BaseResults['growth'][29]) / BaseResults['growth'][29]))

    elif SensParam == 'Total Daphnia':
        figname = 'TDaph.pdf'
        Sparam = Total_Daphnia
        for i in range(11):
            SensInputs.append(Sparam * SensFactors[i] + Sparam)
            SensFactors[i] = SensFactors[i] * 100
            batches.append(Batch(Site, Month, Year, Light, DaphSize, SensInputs[i], StartingMass,Dmax,Dmin))
            results.append(batches[i].Run_Batch())
            SensOutPer.append(100 * ((results[i][0]['growth'][29] - BaseResults['growth'][29]) / BaseResults['growth'][29]))

    elif SensParam == 'Daphnia Size':
        figname = 'DaphS.pdf'
        Sparam = DaphSize
        for i in range(11):
            SensInputs.append(Sparam * SensFactors[i] + Sparam)
            SensFactors[i] = SensFactors[i] * 100
            batches.append(Batch(Site, Month, Year, Light, SensInputs[i], Total_Daphnia, StartingMass,Dmax,Dmin))
            results.append(batches[i].Run_Batch())
            SensOutPer.append(100 * ((results[i][0]['growth'][29] - BaseResults['growth'][29]) / BaseResults['growth'][29]))

    elif SensParam == 'K':
        figname = 'kout.pdf'
        Sparam = k
        for i in range(11):
            SensInputs.append(Sparam * SensFactors[i] + Sparam)
            SensFactors[i] = SensFactors[i] * 100
            batches.append(Batch(Site, Month, Year, SensInputs[i], DaphSize, Total_Daphnia, StartingMass,Dmax,Dmin))
            results.append(batches[i].Run_Batch())
            SensOutPer.append(100 * ((results[i][0]['growth'][29] - BaseResults['growth'][29]) / BaseResults['growth'][29]))

        # "Daphnia eaten",results[0]['dailyconsume'][x])
    for i in range(len(SensFactors)):
        if abs(SensFactors[i]) > abs(largestout):
            largestout = abs(SensFactors[i])
    for i in range(len(SensOutPer)):
        if abs(SensOutPer[i]) > abs(largestout):
            largestout = abs(SensOutPer[i])
    if abs(largestout) > 200:
        largestout = 200
    largestoutrem = largestout % 50
    largestout = largestout + 50 - largestoutrem
    fig=pyplot.figure()
    fig=pyplot.figure(facecolor='#c8e9b1')
    ax = fig.add_subplot(111)
    ax.plot(SensFactors, SensOutPer, 'g^')
    ax.set_ylabel('Percent Change in Final Growth Rate')
    ax.set_xlabel('Percent Change in %s' % SensParam)
    ax.axis([-largestout, largestout, -largestout, largestout])
    ax.grid()
    fig.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
    pylab.savefig( "new.png",facecolor=fig.get_facecolor(), edgecolor='lightblue')
    data_uri = base64.b64encode(open('new.png', 'rb').read()).decode('utf-8').replace('\n', '')
    img_tag = '<img class="results" src="data:image/png;base64,{0}">'.format(data_uri)
    print(img_tag)
    print(SensOutPer)

else:
    fig = pyplot.figure()
    fig=pyplot.figure(facecolor='#c8e9b1')
    massax = fig.add_subplot(221)
    massax.plot(BaseResults['StartingMass'])
    massax.set_ylabel('Mass')
    grax = fig.add_subplot(222)
    grax.plot(BaseResults['growth'])
    grax.set_ylabel('Growth')
    dax = fig.add_subplot(223)
    '''
    if def_flag == 'NO':
    df = pandas.read_csv('%s_%s_%s_temps.csv' % (Site,Month,Year))
    OldTemps = df.Temperature
    OldDays = df.Day
    OldDepths = df.Depth
    NewTemps = []
    NewDepths = []
    NewDays = []
    for i in range(30):
        for j in range(len(OldDepths)):
            if ((OldDepths[j] < Dmax) and (OldDepths[j] > Dmin)):
                NewDays.append(i)
                NewDepths.append(OldDepths[j])
                NewTemps.append(OldTemps[j])

    columns = ["Days", "Depths", "Temperatures"]
    index = NewDays
    df_ = pandas.DataFrame(index=index, columns=columns)
    df_ = df_.fillna(0)
    df_.Days = NewDays
    df_.Depths = NewDepths
    df_.Temperatures = NewTemps
    df_.to_csv('heatmapdata.csv')



    temps = pandas.read_csv('heatmapdata.csv')
    temps = temps.pivot_table("Temperatures","Depths", "Days")
    x = arange(0.0, 30, 0.01)
    dax =seaborn.heatmap(temps, xticklabels=5, yticklabels=5, vmin = 0, vmax=25, cmap = pyplot.cm.rainbow)
    '''
    dax.plot(BaseResults['day_depth'], 'black')
    dax.set_ylabel('Day Depth')
    #dax.set_autoscaley_on(False)
    dax.set_ylim(35,0)
    dax.set_ylabel('Day Depth')
    dax.yticklabels=(arange(0,35,5))
    #dax.fill_between(x, 0, Dmin, color="gray")
    #dax.fill_between(x, 35, Dmax, color="gray")
    nax = fig.add_subplot(224)
    #nax = seaborn.heatmap(temps, xticklabels=10, yticklabels=10, vmin=0, vmax=25, cmap=pyplot.cm.ocean)
    nax.set_ylabel('Night Depth')
    #nax.fill_between(x, Dmin, 0.0, color="gray")
    #nax.fill_between(x, Dmax, 35, color="gray")
    nax.plot(BaseResults['night_depth'],'black')
    nax.yticklabels=(arange(0,35,5))
    nax.set_ylim(35,0)
    fig.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
    pylab.savefig( "new.png",facecolor=fig.get_facecolor(), edgecolor='lightblue')
    data_uri = base64.b64encode(open('new.png', 'rb').read()).decode('utf-8').replace('\n', '')
    img_tag = '<img class="results" src="data:image/png;base64,{0}">'.format(data_uri)
    print(img_tag)
print ('''
    <br>
    <div id="valuewrap">
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
       ''' % (FreshBatch.Site,FreshBatch.Year,Month,StartingMass,Month,FreshBatch.TotalDaphnia,Month,FreshBatch.DaphSize,Month,FreshBatch.Light))

if depr_flag == "YES":
    print('''Depth restricted to between %.2fm and %.2fm.<br>''' % (Dmin,Dmax))

print ('''  </div>
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
       ''' % (Month,SensFactors[10],results[10][0]['StartingMass'][29],Month,SensFactors[10],results[0][0]['StartingMass'][29],Month,BaseResults['growth'][29],Month,BaseResults['day_depth'][29],Month,BaseResults['night_depth'][29],Month,DConsumed))

print('''
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
        <form action="RunModel.py" method="post" target="_blank">
            <div id="sec1">
                <label>Please Select Year:</label> <select name="Year" id="YearID">
                    <option value="2013" selected>2013</option>
                    <option value="2014">2014</option>
                    <option value="2015">2015</option>
                </select>
                <br>
                <br>

                <label>Please Select Site:</label> <select name="Site">
                    <option value="Fall Creek" selected>Fall Creek</option>
                    <option value="Hills Creek">Hills Creek</option>
                    <option value="Lookout Point">Lookout Point</option>
                </select>
                <br>
                <br>

                <label>Please Select Month:</label> <select name="Month">
                    <option value="March" selected>March</option>
                    <option value="April">April</option>
                    <option value="May">May</option>
                    <option value="June">June</option>
                    <option value="July">July</option>
                    <option value="August">August</option>
                </select>
                <br>
                <br>
                    <div style="text-align:center;font-size:20px;">Use Default Values? </div><br>
                <label>Yes</label><input type="radio" name="defa" value="yes" /><br>
                <label>No</label><input type="radio" name="defa" value='no' /><br><br>

                <label>Fish Starting Mass (g):</label><input type="range" name="SMassSlide" id="SMassInID" value="60" min="0" max="200" step="0.1" onchange="updateSMassInput(this.value);" oninput="SMassOut.value = SMassSlide.value"><output name="SMassOut" id="SMassOutID">.75</output>
                <label>Or Enter Value:</label> <input type="text" name="Starting_Mass_In" id="SMass_TextInID"  oninput="SMassOutID.value = SMass_TextInID.value"> <br><br>

                <label>Daphnia Size (mm):</label><input type="range" name="DaphSSlide" id="DaphSInID" value=".75" min=".5" max="1.5" step=".01" onchange="updateDaphSText(this.value);" oninput="DaphSOut.value = DaphSSlide.value"><output name="DaphSOut" id="DaphSOutID">.75</output><br><br>
                <label>Or Enter Value:</label> <input type="text" name="Daphnia Size" id="DaphSTextInID" oninput="DaphSOutID.value = DaphSTextInID.value"> <br>
            </div>
            <div id="sec2">
                <label>Total Daphnia:</label><input type="range" name="TotDSlide" id="TotDInID" value="500" min="0" max="1000" onchange="updateTotDTextInput(this.value);" oninput="TotDOut.value = TotDSlide.value"><output name="TotDOut" id="TotDOutID"> 500 </output><br><br>
                <label>Or Enter Value:</label> <input type="text" name="Total_Daphnia_Input_Name" id="TotDTextInID" oninput="TotDOutID.value = TotDTextInID.value" oninput="TotDOutID.value = TotDInID.value"> <br>

                <label>Light Extinction Coefficient:</label><input type="range" name="LightSlide" id="LightInID" value=".3" min="0" max="1" step=".01" onchange="updateLightTextInput(this.value);" oninput="LightOut.value = LightSlide.value"><output name="LightOut" id="LightOutID">.3</output><br><br>
                <label>Or Enter Value:</label> <input type="text" name="Light" id="LightTextInID" oninput="LightOutID.value = LightTextInID.value" oninput="LightOutID.value = LightInID.value"> <br><br>

                    <div style="text-align:center;font-size:20px;">Restrict Depth?</div><br>
                <label>Yes</label><input type="radio" name="depr" value="yes" /><br>
                <label>No</label><input type="radio" name="depr" value="no" /><br>
                <label>Maximum Depth:</label><input type="range" name="DmaxIn" id="DmaxInID" value="60" min="0" max="200" oninput="DmaxOutID.value = DmaxInID.value" onchange="updateDepthTextInput(this.value);"><output name="DmaxOut" id="DmaxOutID"> 60 </output> <br>
                <label>Minimum Depth:</label><input type="range" name="DminIn" id="DminInID" value="60" min="0" max="200" oninput="DminOutID.value = DminInID.value" onchange="updateDepthTextInput(this.value);"><output name="DminOut" id="DminOutID"> 60 </output> <br>
                <label>Or Restrict to a Single Depth:</label> <input type="text" name="Depth_Text" id="Depth_TextInID" oninput="DminIn.value = Depth_Text.value; DmaxIn.value = Depth_Text.value"> <output name="Depth_TextOut" id="Depth_TextOutID"> </output> <br><br>
                <div id="subutt">
                    <input type="submit" value="Submit"/>
                </div>
            </div><br>
        </form>
    </div>
</body>
''')

os.remove('new.png')
quit()