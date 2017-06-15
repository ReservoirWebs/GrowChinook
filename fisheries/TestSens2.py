#!/usr/bin/python


import cgi, cgitb,time, os
cgitb.enable()

address = cgi.escape(os.environ["REMOTE_ADDR"])
script = "Advanced Sensitivity Form"
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
<script type="text/javascript">
function configureDropDownLists2(ddy,dds) {
var years = ['2013', '2014', '2015'];
var sites = ['Blue River', 'Fall Creek', 'Hills Creek', 'Lookout Point'];

switch (ddy.value) {
    case '2013':
        dds.options.length = 0;
        for (i=0; i<3; i++) {
            createOption(dds,sites[i],sites[i]);
        }
        break;
    case '2014':
    dds.options.length = 0;
    for (i=1; i<sites.length; i++) {
            createOption(dds,sites[i],sites[i]);
        }
        break;
    case '2015':
        dds.options.length = 0;
        for (i=1; i<sites.length; i++) {
            createOption(dds,sites[i],sites[i]);
        }
        break;
    default:
        dds.options.length = 0;
    break;
    }

}


function createOption(dd, text, value) {
    var opt = document.createElement('option');
    opt.value = value;
    opt.text = text;
    dd.options.add(opt);
}</script>
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
function updateSensTextInput(val) {
          document.getElementById('SensTextInID').value=val;
        }
</script>
<script>
function updateLightTextInput(val) {
          document.getElementById('LightTextInID').value=val;
        }
</script>
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
        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSens.py">Run Model With Sensitivity</a></li>
        <li><a class="current" href="http://cas-web0.biossys.oregonstate.edu/TestSens2.py">Run Advanced Sensitivity</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSumm.py">Run Multiple Months</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/Curves.html">Temperature and Daphnia Curves</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/about.html">About</a></li>
    </ul>
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

print ('</html>')