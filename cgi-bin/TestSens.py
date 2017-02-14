#!C:\Anaconda3\python.exe


import cgi, cgitb
cgitb.enable()

print ('Content-type:text/html\r\n\r\n')
print('<html>')
print('''<link type="text/css" rel="stylesheet" media="screen" href="/css/Style.css" />
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
<img class="head" src="http://localhost:81/css/src/LPR.jpg">
<body>
    <h2>Enter Values to GrowChinook</h2>
    <div id="formwrap">
        <form action="RunModelSens.py" method="post" target="_blank">
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

                <label>Fish Starting Mass (g):</label><input type="range" name="SMassSlide" id="SMassInID" value="60" min="0" max="200" step="0.1" onchange="updateSMassInput(this.value);" oninput="SMassOut.value = SMassSlide.value"><output name="SMassOut" id="SMassOutID">60</output>
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
                <br>
            </div><br>
            <div
                <div style="text-align:center;font-size:20px;margin:auto;">Run Sensitivity Analysis?</div><br>
                <label>Yes</label><input type="radio" name="sens" value="yes" /><br>
                <label>No</label><input type="radio" name="sens" value='no' /><br>
                <label>Select Sensitivity Parameter:</label><select name="Sens_Param">
                    <option value="Starting Mass" selected>Starting Mass</option>
                    <option value="Total Daphnia">Total Daphnia</option>
                    <option value="Daphnia Size">Daphnia </option>
                    <option value="K">Light</option>
                </select>
                <label>Select Sensitivity Range(percent)</label><input type="range" name="SensSlide" id="SensInID" value=".50" min=".01" max="1.50" step=".01" onchange="updateSensText(this.value);" oninput="SensOut.value = SensSlide.value"><output name="SensOut" id="SensOutID">.50</output><br><br>
                <label>Or Enter Value:</label> <input type="text" name="Sparam_Range" id="SensTextInID" oninput="SensOutID.value = SensTextInID.value"> <br>
            <div id="subutt">
                    <input type="submit" value="Submit"/>
            </div>
        </form>
    </div>
</body>
''')

print ('</html>')