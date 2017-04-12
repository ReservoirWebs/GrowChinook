#!/usr/bin/python


import cgi, cgitb
cgitb.enable()

print ('Content-type:text/html\r\n\r\n')
print('<html>')
print('''<link type="text/css" rel="stylesheet" media="screen" href="/css/Style.css" />
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
        <li><a href="/">Home</a></li>
        <li><a href="/Test.py">Run Standard Model</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSens.py">Run Model With Sensitivity</a></li>
        <li><a class="current" href="TestSens2.py">Run Advanced Sensitivity</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/about.html">About</a></li>
    </ul>
<body>
    <h2>Enter Values to GrowChinook</h2>
    <div id="formwrap">
        <form action="RunModelSens2.py" method="post" target="_blank">
        <div style="display:inline-block;width:1100px;">
                    <div style="width:300px;"></div>
                    <div style="font-size:20px;width:500px;margin:auto;">Select Sensitivity Parameter:<select name="Sens_Param"><br>
                        <option value="Starting Mass" selected>Starting Mass</option>
                        <option value="Total Daphnia">Total Daphnia</option>
                        <option value="Daphnia Size">Daphnia </option>
                        <option value="K">Light</option>
                    </select>
                    </div>
                    <div style="width:300px;"></div>
                    <br>
</div>    
	<div id="sec1">
                <label>Please Select Year:</label> <select name="Year" id="ddy" onchange="configureDropDownLists(this,document.getElementById('ddm'),document.getElementById('dds'))">
                    <option value=""></option>
                    <option value="2015">2015</option>
                    <option value="2014">2014</option>
                    <option value="2013">2013</option>
                </select>
                <br>
                <br>
                    <div style="text-align:center;font-size:20px;">Use Default Values? </div><br>
                <label>Yes</label><input type="radio" name="defa" value="yes" /><br>
                <label>No</label><input type="radio" name="defa" value='no' /><br><br>

                <label>Fish Starting Mass (g):</label><input type="range" name="SMassSlide" id="SMassInID" value="60" min="0" max="200" step="0.1" onchange="updateSMassInput(this.value);" oninput="SMassOut.value = SMassSlide.value"><output name="SMassOut" id="SMassOutID">60</output>
                <label>Or Enter Value:</label> <input type="text" name="Starting_Mass_In" id="SMass_TextInID"  oninput="SMassOutID.value = SMass_TextInID.value"> <br><br>

                <label>Daphnia Size (mm):</label><input type="range" name="DaphSSlide" id="DaphSInID" value=".75" min=".5" max="1.5" step=".01" onchange="updateDaphSText(this.value);" oninput="DaphSOut.value = DaphSSlide.value"><output name="DaphSOut" id="DaphSOutID">.75</output><br><br>
                <label>Or Enter Value:</label> <input type="text" name="Daphnia Size" id="DaphSTextInID" oninput="DaphSOutID.value = DaphSTextInID.value"> <br>

            </div>
            <div id="sec2">
                <label>Total Daphnia:</label><input type="range" name="TotDSlide" id="TotDInID" value="500" min="0" max="1000" onchange="updateTotDTextInput(this.value);" oninput="TotDOut.value = TotDSlide.value"><output name="TotDOut" id="TotDOutID"> 500 </output><br><br>
                <label>Or Enter Value:</label> <input type="text" name="Total_Daphnia_Input_Name" id="TotDTextInID" oninput="TotDOutID.value = TotDTextInID.value" oninput="TotDOutID.value = TotDInID.value"> <br>

                <label>Light Extinction Coefficient:</label><input type="range" name="LightSlide" id="LightInID" value=".3" min="0" max="1" step=".01" oninput="LightOutID.value = LightInID.value" onchange="updateLightTextInput(this.value);"><output name="LightOut" id="LightOutID">.3</output><br><br>
                <label>Or Enter Value:</label> <input type="text" name="Light" id="LightTextInID" oninput="LightSlide.value = Light.value"><output name="Light_TextOut" id="Light_TextOutID"> </output> <br><br>


<div style="text-align:center;font-size:20px;">Restrict Depth?</div><br>
                <label>Yes</label><input type="radio" name="depr" value="yes" /><br>
                <label>No</label><input type="radio" name="depr" value="no" /><br>
		<label>Maximum Depth:</label><input type="range" name="DmaxIn" id="DmaxInID" value="20" min="0" max="35" oninput="DmaxOutID.value = DmaxInID.value" onchange="updateDepthTextInput(this.value);"><output name="DmaxOut" id="DmaxOutID"> 20 </output> <br>
                <label>Minimum Depth:</label><input type="range" name="DminIn" id="DminInID" value="10" min="0" max="35" oninput="DminOutID.value = DminInID.value" onchange="updateDepthTextInput(this.value);"><output name="DminOut" id="DminOutID"> 10 </output> <br>
                <label>Or Restrict to a Single Depth:</label> <input type="text" name="Depth_Text" id="Depth_TextInID" oninput="DminIn.value = Depth_Text.value; DmaxIn.value = Depth_Text.value"> <output name="Depth_TextOut" id="Depth_TextOutID"> </output> <br><br>
            <br>
            </div>
                
  		    <div id="subutt">
                        <input type="submit" value="Submit"/>
                    </div>
               
        </form>
    </div>
</body>
''')

print ('</html>')