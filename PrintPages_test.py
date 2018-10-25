import time

def print_header(title, page):
    if title is None:
        title = 'GrowChinook'
    print('Content-type:text/html; charset=utf-8\r\n\r\n')
    print('<html>')
    print('<link type="text/css" rel="stylesheet" media="screen" href="/css/Style.css" />')
    print('<head>')
    print('<title>{}</title>'.format(title))
    print('''<meta name="description" content="Grow Chinook Linked Foraging and Bioenergetics Model for Spring Chinook"/>
             <meta name="keywords" content="Grow Chinook, Linked Foraging Bioenergetics, Spring Chinook, Model"/>''')
    print('</head>')
    print('''<link type="text/css" rel="stylesheet" media="screen" href="/css/Style.css" />
    <link type="text/css" rel="stylesheet" media="screen" href="/css/Style.css" />
    <script src="/js/JavaForFish.js"></script>
    <img class="head" src="/css/src/LPR.jpg">
    <body>''')

    if page == 'Std':
        print('''
        <ul>
            <li><a href="http://growchinook.fw.oregonstate.edu/">Home</a></li>
            <li><a href="http://growchinook.fw.oregonstate.edu/instructions.html">Instructions</a></li>
            <li><a class="current" href="http://growchinook.fw.oregonstate.edu/Test.py">Run Standard Model</a></li>
            <li><a href="http://growchinook.fw.oregonstate.edu/TestSens.py">Run Model With Sensitivity</a></li>
            <li><a href="http://growchinook.fw.oregonstate.edu/TestSumm.py">Run Multiple Months</a></li>
            <li><a href="http://growchinook.fw.oregonstate.edu/Curves.html">Temperature and Daphnia Curves</a></li>
            <li><a href="http://growchinook.fw.oregonstate.edu/about.html">About</a></li>
        </ul>''')
    elif page == 'Sens':
        print('''
        <ul>
            <li><a href="http://growchinook.fw.oregonstate.edu/">Home</a></li>
            <li><a href="http://growchinook.fw.oregonstate.edu/instructions.html">Instructions</a></li>
            <li><a href="http://growchinook.fw.oregonstate.edu/Test.py">Run Standard Model</a></li>
            <li><a class="current" href="http://growchinook.fw.oregonstate.edu/TestSens.py">Run Model With Sensitivity</a></li>
            <li><a href="http://growchinook.fw.oregonstate.edu/TestSumm.py">Run Multiple Months</a></li>
            <li><a href="http://growchinook.fw.oregonstate.edu/Curves.html">Temperature and Daphnia Curves</a></li>
            <li><a href="http://growchinook.fw.oregonstate.edu/about.html">About</a></li>
        </ul>''')
    elif page == 'AdvSens':
        print('''
                <ul>
                    <li><a href="http://growchinook.fw.oregonstate.edu/">Home</a></li>
                    <li><a href="http://growchinook.fw.oregonstate.edu/instructions.html">Instructions</a></li>
                    <li><a href="http://growchinook.fw.oregonstate.edu/Test.py">Run Standard Model</a></li>
                    <li><a href="http://growchinook.fw.oregonstate.edu/TestSens.py">Run Model With Sensitivity</a></li>
                    <li><a class="current" href="http://growchinook.fw.oregonstate.edu/TestSens2.py">Run Advanced Sensitivity</a></li>
                    <li><a href="http://growchinook.fw.oregonstate.edu/TestSumm.py">Run Multiple Months</a></li>
                    <li><a href="http://growchinook.fw.oregonstate.edu/Curves.html">Temperature and Daphnia Curves</a></li>
                    <li><a href="http://growchinook.fw.oregonstate.edu/about.html">About</a></li>
                </ul>''')
    elif page == 'Mult':
        print('''
                <ul>
                    <li><a href="http://growchinook.fw.oregonstate.edu/">Home</a></li>
                    <li><a href="http://growchinook.fw.oregonstate.edu/instructions.html">Instructions</a></li>
                    <li><a href="http://growchinook.fw.oregonstate.edu/Test.py">Run Standard Model</a></li>
                    <li><a href="http://growchinook.fw.oregonstate.edu/TestSens.py">Run Model With Sensitivity</a></li>
                    <li><a class="current" href="http://growchinook.fw.oregonstate.edu/TestSumm.py">Run Multiple Months</a></li>
                    <li><a href="http://growchinook.fw.oregonstate.edu/Curves.html">Temperature and Daphnia Curves</a></li>
                    <li><a href="http://growchinook.fw.oregonstate.edu/about.html">About</a></li>
                </ul>''')


def print_in_data(site, year, mass, total_daphnia, daphnia_size, light):
    print('''
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
                    <div class="dataleft">Daphnia Density (thousand per m2 surface):
                        <div class="dataright">%.0f</div>
                    </div>
                    <div class="dataleft">Daphnia Size (mm):
                        <div class="dataright">%.2f mm</div>
                    </div>
                    <div class="dataleft">Light Extinction Coefficient:
                        <div class="dataright">%.2f</div>
                    </div>
                    </div>
                </div>
                ''' % (site, year, mass, total_daphnia, daphnia_size, light))


def print_full_form(long_file_name, short_file_name, in_out, target):
    if in_out == 'out':
        print('''
              <br>
              </div>
              <br>
              <br>
              <div>
              <div style="float:left;">Download Full Results?
                  <a href="/{}" download>Download Full</a>
              </div>
              <br>
              <div style="float:left;">Download Short Results?
                  <a href="/{}" download>Download Short</a>
              </div>
              </div>
          </div>
      </div>
      '''.format(long_file_name, short_file_name))

    print('''
    <body>
        <h2>Enter Values to GrowChinook</h2>
        <div id="formwrap">
            <form action='{}' method="post" target="_blank">'''.format(target))

    if target == 'RunModelSens_test.py':
        print('''<div style="display:inline-block;width:90%;">
                     <div style="font-size:20px;width:45%;float:left;margin:auto;">First Select Sensitivity Parameter:
                         <select name="Sens_Param"><br>
                             <option value="Starting Mass" selected>Starting Mass</option>
                             <option value="Total Daphnia">Total Daphnia</option>
                             <option value="Daphnia Size">Daphnia Size</option>
                             <option value="K">Light</option>
                         </select>
                     </div>
                     <div style="width:45%;float:right;">
                         <label>Enter Value for Sensitivity Range (Percent):</label>
                         <input type="text" name="Sparam_Range" id="SensTextInID" oninput="SensOutID.value = SensTextInID.value">
                     </div><br>
                 </div>
                 <br><br><br>''')

    print('''  <b>Enter a Starting Mass for the fish. Then select a default Year, Month, and Site, which will be used to fill in any fields you may choose to leave blank.
               Now you may adjust any values you like, and can at any time reassert the default values for your selected Year, Month, and Site by clicking the "Apply Observed Values" button.</b><br><br>
               <div id="sec1">
                   <label>Enter Fish Starting Mass (g):</label>
                       <input type="text" name="Starting_Mass_In" id="SMass_TextInID"  oninput="SMassSlide.value = SMass_TextInID.value" />
                   <br><br>
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
                        </select>
                        <br>
                    </div>
                    <div style="text-align:center;">
                        <button type="button" onclick="getDefaultValues(document.getElementById('ddy'),document.getElementById('ddm1'),document.getElementById('dds'),document.getElementById('SMass_TextInID'),document.getElementById('TotDDef'),document.getElementById('DaphSDef'),document.getElementById('LightDef'));
                        getDefaultValues(document.getElementById('ddy'),document.getElementById('ddm1'),document.getElementById('dds'),document.getElementById('SMass_TextInID'),document.getElementById('TotDTextInID'),document.getElementById('DaphSTextInID'),document.getElementById('LightTextInID'));">
                        Apply Observed Values
                        </button>
                    </div><br>
                    Observed:<input class="defdisp" type="text" name="TotDDef" id="TotDDef" value="" readonly><label>Daphnia Density (depth to surface per m<sup>2</sup>)</label>Using:<input type="text" name="Total_Daphnia_Input_Name" id="TotDTextInID" oninput="TotDSlide.value = TotDTextInID.value" oninput="TotDOutID.value = TotDInID.value"> <br><br>
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
                        <br>
                        <div class="deptem" style="float:left;"><p style="margin-top:auto;">
                            <b>Optional: Set to restrict temperature</b>
                        </div>
                        <div style="float:right;width:70%;">
                            <label class="deptem">Maximum Temperature (Celsius):</label>
                            <input class="deptem" type="text" name="TmaxIn" id="TmaxInID"><br>
                            <label class="deptem">Minimum Temperature (Celsius):</label>
                            <input class="deptem" type="text" name="TminIn" id="TminInID">
                        </div>
                        <br>
                    </div>
                    <div><br></div>
                    <div style="width:95%; display:inline-block;">
                        <b>Optional: Select a Year, Month, and Site to apply the corresponding Daphnia distribution curve.
                           Otherwise, the curve corresponding to the Default Year, Month, and Site will be used.</b><br><br>
                        <label class="dd">Daphnia Year:</label>
                        <select name="DYear" id="dddy" onchange="configureDropDownLists(this,document.getElementById('dddm'),document.getElementById('ddds'))">
                            <option value=""></option>
                            <option value="2016">2016</option>
                            <option value="2015">2015</option>
                            <option value="2014">2014</option>
                        </select>
                        <label class="dd">Daphnia Site:</label>
                        <select name="DSite" id="ddds">
                        </select>
                        <label class="dd">Daphnia Month:</label>
                        <select name="DMonth" id="dddm">
                        </select>
                        <div><br><br></div>
                        <div style="margin-top:auto;width:100%;">
                            <b>Optional: Select a Year, Month, and Site to apply the corresponding temperature curve.
                               Otherwise, the curve corresponding to the Default Year, Month, and Site will be used.</b><br><br>
                            <label class="dd">Temperature Year:</label>
                            <select name="TYear" id="ddty"  onchange="configureDropDownLists(this,document.getElementById('ddtm'),document.getElementById('ddts'))">
                                <option value=""></option>
                                <option value="2016">2016</option>
                                <option value="2015">2015</option>
                                <option value="2014">2014</option>
                            </select>
                            <label class="dd">Temperature Site:</label>
                            <select name="TSite" id="ddts">
                            </select>
                            <label class="dd">Temperature Month:</label>
                            <select name="TMonth" id="ddtm">
                            </select><br><br><br>
                        </div>
                        <div style="float:left;">
                    <label>Enter Name of Custom Temp File:</label>
                    <input type="text" style="width:25%;" name="CustTemp" id="CustTemp">
                </div>
                    </div>
                </div>
                <div style="float:left;">
                    <br>
                    <label>Enter Name to Display on Tab:</label>
                    <input type="text" style="width:50%;" name="TabName" id="TabNameID">
                </div><br>
                <div style="display:inline-block;margin:auto;width:75%">
                    <br><br>
                    <div id="subutt" style="float:right;">
                        <input type="submit" value="Run Model" style="width:140px"/>
                    </div>
                <div>
                    <b>Optional: Population Estimate</b><br>
                    Select Site for Population Estimate
                    <select name="ESite" id="ddes">
                        <option value=""></option>
                        <option value="Fall Creek">Fall Creek</option>
                        <option value="Hills Creek">Hills Creek</option>
                        <option value="Lookout Point">Lookout Point</option>
                    </select>
                </div>
                <br>
                <div style="float:left;">
                    <label style="text-align:left;">Enter Elevation for Population Estimate (ft):</label>
                    <input type="text" style="width:25%;" name="Elev" id="ElevID">
                </div><br>
            </div>
            <br><br>
        </form>

        <div style="width:48%; float:left;">Download Temperature Template to Use Custom Temps:<br>
                            <a href="/TemperatureTemplate.csv" download>Temperature Template</a><br>
        <form action = "/UploadTemp.php" method="POST" enctype="multipart/form-data">
            <input type="file" accept=".csv" name="filename" id="filename" style="width:130px;">
            <input type="submit" value="Upload" style="width:100px;">
            </form>
                        </div>
        <br>
        <div style="width:48%; float:right;">
        Here is a list of uploaded temperature files:''')

def print_adv_sens_form(long_file_name, short_file_name, in_out, target):
    if in_out == 'out':
        print('''
              <br><div style="float:left;">Download Full Results?
                    <a href="/{}" download>Download Full</a>
                </div>
              <br><div style="float:left;">Download Short Results?
                    <a href="/{}" download>Download Short</a>
                </div>
                </div>
                </div>
              '''.format(long_file_name, short_file_name))
    print('''
        <body>
            <h2>Enter Values to GrowChinook</h2>
            <div id="formwrap">
                <form action='{}' method="post" target="_blank">'''.format(target))

    print('''<div style="display:inline-block;width:90%;">
                         <div style="font-size:20px;width:45%;float:left;margin:auto;">First Select Sensitivity Parameter:
                             <select name="Sens_Param"><br>
                                 <option value="Starting Mass" selected>Starting Mass</option>
                                 <option value="Total Daphnia">Total Daphnia</option>
                                 <option value="Daphnia Size">Daphnia Size</option>
                                 <option value="K">Light</option>
                             </select>
                         </div>

                        <div style="width:45%;float:right;">
                        <label>Enter Value for Sensitivity Range (Percent):</label> <input type="text" name="Sparam_Range" id="SensTextInID" oninput="SensOutID.value = SensTextInID.value"></div> <br>
                        </div><br><br><br>''')

    print('''  <b>Enter a Starting Mass for the fish. Then select a default Year, Month, and Site, which will be used to fill in any fields you may choose to leave blank.
                   Now you may adjust any values you like, and can at any time reassert the default values for your selected Year, Month, and Site by clicking the "Apply Observed Values" button.</b><br><br>
                   <label>Enter Fish Starting Mass (g):</label><input type="text" name="Starting_Mass_In" id="SMass_TextInID"  oninput="SMassSlide.value = SMass_TextInID.value"> 
                   <div id="sec1">
                        <br><br>
                        <p style="text-align:center;width:80%;"><b>Select a Year, Month, and Site to fill Daphnia Density, Daphnia Size, and Light Extinction Coefficient with Observed Values</b>
                        <div style="margin:auto;">
                            <label class="dd">Year:</label>
                            <select name="Year" value="2015" id="ddy" onchange="configureDropDownLists2(this,document.getElementById('dds'))">
                                <option value=""></option>
                                <option value="2016">2016</option>
                                <option value="2015">2015</option>
                                <option value="2014">2014</option>
                            </select>
                            <label class="dd">Site:</label>
                            <select name="Site" value="Fall Creek" id="dds">
                            </select>
                        </div>
                    <div style="float:left;">
                        <br>
                        <label>Daphnia Density (thousand per m<sup>2</sup> surface)</label>Use:<input type="text" name="Total_Daphnia_Input_Name" id="TotDTextInID" oninput="TotDSlide.value = TotDTextInID.value" oninput="TotDOutID.value = TotDInID.value"> <br><br>
                        <label>Light Extinction Coefficient (Higher is Darker)</label>Use:<input type="text" name="Light" id="LightTextInID" oninput="LightSlide.value = Light.value"><output name="Light_TextOut" id="Light_TextOutID"> </output> <br><br>
                        <label>Daphnia Size (mm):</label>Use:<input type="text" name="Daphnia Size" id="DaphSTextInID" oninput="DaphSSlide.value = DaphSTextInID.value"> <br><br>
                    </div></div>
                    <div id="sec2">
                    <br><br><br>
                        <div style="display:inline-block;">
                            <div class="deptem" style="float:left;"><p style="margin-top:auto;">
                                <b>Optional: Set to restrict depth</b>
                            </div>
                            <div style="float:right;width:70%;">
                                <label class="deptem">Maximum Depth (m):</label>
                                <input class="deptem" type="text" name="DmaxIn" id="DmaxInID"><br>
                                <label class="deptem">Minimum Depth (m):</label>
                                <input class="deptem" type="text" name="DminIn" id="DminInID">
                            </div>
                            <div class="deptem" style="float:left;">
                                <br>
                                <br>
                                <br>
                                <p style="margin-top:auto;">
                                    <b>Optional: Set to restrict temperature</b>
                                </p>
                            </div>
                            <div style="float:right;width:70%;">
                                <br>
                                <br>
                                <label class="deptem">Maximum Temperature (Celsius):</label>
                                <input class="deptem" type="text" name="TmaxIn" id="TmaxInID"><br>
                                <label class="deptem">Minimum Temperature (Celsius):</label>
                                <input class="deptem" type="text" name="TminIn" id="TminInID">
                            </div>
                            <div style="float:left;">
                            <br>
                    <label>Enter Name to Display on Tab:</label>
                    <input type="text" style="width:50%;" name="TabName" id="TabNameID">
                </div><br>
                <div style="display:inline-block;margin:auto;width:75%">
                    <br>
                    <div id="subutt" style="float:right;">
                        <input type="submit" value="Run Model" style="width:150px"/>
                    </div>
                        </div>
                        <div><br></div>''')


def write_log_entry(script, address):
    with open('userlog.csv', 'a') as log:
        log.write("IP: {},".format(address))
        log.write("Page: {},".format(script))
        log.write("Time: {},".format(time.ctime(time.time())))
        log.write('\n')