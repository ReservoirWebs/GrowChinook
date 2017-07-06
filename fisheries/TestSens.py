#!\usr\bin\python


import cgi, cgitb, time, os
cgitb.enable()

address = cgi.escape(os.environ["REMOTE_ADDR"])
script = "Sensitivity Form"

with open('userlog.csv', 'a') as log:
    log.write("IP: {}," .format(address))
    log.write("Page: {}," .format(script))
    log.write("Time: {}," .format(time.ctime(time.time())))
    log.write('\n')
log.closed

print ('Content-type:text/html\r\n\r\n')
print('<html>')
print('''<link type="text/css" rel="stylesheet" media="screen" href="/css/Style.css" />
<script src="/js/JavaForFish.js"></script>
<link type="text/css" rel="stylesheet" media="screen" href="/css/Style.css" />
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
    </ul>
<body>
    <h2>Enter Values to GrowChinook</h2>
    <div id="formwrap">
        <form action="RunModelSens.py" method="post" target="_blank">
           <div style="display:inline-block;width:90%;">
                    <div style="font-size:20px;width:45%;float:left;margin:auto;">First Select Sensitivity Parameter:<select name="Sens_Param"><br>
                        <option value="Starting Mass" selected>Starting Mass</option>
                        <option value="Total Daphnia">Total Daphnia</option>
                        <option value="Daphnia Size">Daphnia Size</option>
                        <option value="Light">Light</option>
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
                    <br>
                    <div style="float:left;">
                <label>Enter Name to Display on Tab:</label>
                <input type="text" style="width:50%;" name="TabName" id="TabNameID">
                </div><br>
                    <div id="subutt" style="margin:auto;">
                        <input type="submit" value="Submit"/>
                    </div>
                </div>
        </form>
    </div>
</body>
''')

print ('</html>')