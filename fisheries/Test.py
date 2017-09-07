#!/usr/bin/python


import cgi
import os
import time
import glob

print ('Content-type:text/html\r\n\r\n')
print('<html>')

address = cgi.escape(os.environ["REMOTE_ADDR"])
script = "Main Model Form"
with open('userlog.csv', 'a') as log:
    log.write("IP: {}," .format(address))
    log.write("Page: {}," .format(script))
    log.write("Time: {}," .format(time.ctime(time.time())))
    log.write('\n')
log.closed

#<li><a href="http://cas-web0.biossys.oregonstate.edu/scene.py">Run Scenarios</a><li>

print('''<link type="text/css" rel="stylesheet" media="screen" href="/css/Style.css" />
<img class="head" src="/css/src/LPR.jpg">
<head>
<script src="/js/JavaForFish.js"></script>
<title>GrowChinook</title>
</head>
<body>
    <ul>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/">Home</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/instructions.html">Instructions</a></li>
        <li><a class="current" href="http://cas-web0.biossys.oregonstate.edu/Test.py">Run Standard Model</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSens.py">Run Model With Sensitivity</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSens2.py">Run Advanced Sensitivity</a></li>

        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSumm.py">Run Multiple Months</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/Curves.html">Temperature and Daphnia Curves</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/about.html">About</a></li>
        
    </ul>

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
                  <div style="float:left;">
                <label>Enter Name of Custom Daphnia File:</label>
                <input type="text" style="width:25%;" name="CustDaph" id="CustDaph">
            <br>
</div>
<div style="float:left;">
                <label>Enter Name of Custom Temp File:</label>
                <input type="text" style="width:25%;" name="CustTemp" id="CustTemp">
            </div><br>
                </div>
            </div>
            <div style="float:left;">
                <label>Enter Name to Display on Tab:</label>
                <input type="text" style="width:50%;" name="TabName" id="TabNameID">
            </div><br>
            <div style="display:inline-block;margin:auto;width:75%">
                <div id="subutt" style="float:right;">
                    <input style="width:120px;" type="submit" value="Run Model"/>
                </div>
            <div>Select Site for Density Dependence
            <select name="ESite" id="ddes">
                        <option value=""></option>
                        <option value="Fall Creek">Fall Creek</option>
                        <option value="Hills Creek">Hills Creek</option>
                        <option value="Lookout Point">Lookout Point</option>
                    </select>
            </div>
            <br>
            <div style="float:left;">
                <label>Optional: Enter Pool Elevation (ft) for Density Dependence:</label>
                <input type="text" style="width:25%;" name="Elev" id="ElevID">
            </div><br>
        </div>
    </form>
<div style="float:left; width:45%;">Download Temperature Template to Use Custom Temps
                        <a href="/TemperatureTemplate.csv" download>Temperature Template</a>
<form action = "/UploadTemp.php" method="POST" enctype="multipart/form-data">
    <input type="file" accept=".csv" name="tempfilename" id="tempfilename">
    <input type="submit" value="Upload">
    </form>
<br>
Here is a list of uploaded temperature files:''')
extension = 'csv'
os.chdir('uploads/temp')
temp_files = [i for i in glob.glob('*.csv')]

print('''
{}

</div>

'''.format(temp_files))

os.chdir('../..')

print('''
<div style="float:right; width:45%;">Download Daphnia Template to Use Custom Daphnia Profile
                        <a href="/DaphniaTemplate.csv" download>Daphnia Template</a>
<form action = "/UploadDaph.php" method="POST" enctype="multipart/form-data">
    <input type="file" accept=".csv" name="daphfilename" id="daphfilename">
    <input type="submit" value="Upload">
    </form>
    <br>
Here is a list of uploaded daphnia files:''')
extension = 'csv'
os.chdir('uploads/daph')
daph_files = [i for i in glob.glob('*.csv')]

print('''
{}

</body>
'''.format(daph_files))


print ('</html>')
