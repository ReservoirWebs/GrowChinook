#!\usr\bin\python


import cgi
import os
import time

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
        <li><a href="http://cas-web0.biossys.oregonstate.edu/instructions.html">Instructions</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/Test.py">Run Standard Model</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSens.py">Run Model With Sensitivity</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSens2.py">Run Advanced Sensitivity</a></li>
        <li><a class="current" href="http://cas-web0.biossys.oregonstate.edu/scene.py">Run Scenarios</a><li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSumm.py">Run Multiple Months</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/Curves.html">Temperature and Daphnia Curves</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/about.html">About</a></li>
        
    </ul>

<body>
    <h2>Enter Values to GrowChinook</h2>
    <div id="formwrap">
        <form action="RunModelScene.py" method="post" target="_blank">
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
''')
print ('</html>')
