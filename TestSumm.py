#!/usr/bin/python

import cgi, time, os

address = cgi.escape(os.environ["REMOTE_ADDR"])
script = "Multiple Month Form"
with open('userlog.csv', 'a') as log:
    log.write("IP: {}," .format(address))
    log.write("Page: {}," .format(script))
    log.write("Time: {}," .format(time.ctime(time.time())))
    log.write('\n')
log.closed

#        <li><a href="http://growchinook.fw.oregonstate.edu/scene.py">Run Scenarios</a><li>

print ('Content-type:text/html\r\n\r\n')
print('<html>')
print('''<link type="text/css" rel="stylesheet" media="screen" href="/css/Style.css" />
<link type="text/css" rel="stylesheet" media="screen" href="/css/Style.css" />
<img class="head" src="/css/src/LPR.jpg">
<head>
<script src="/js/JavaForFish.js"></script>
<title>GrowChinook</title>
</head>
<body>
    <ul>
        <li><a href="http://growchinook.fw.oregonstate.edu/">Home</a></li>
        <li><a href="http://growchinook.fw.oregonstate.edu/">Instructions</a></li>
        <li><a href="http://growchinook.fw.oregonstate.edu/Test.py">Run Standard Model</a></li>
        <li><a href="http://growchinook.fw.oregonstate.edu/TestSens.py">Run Model With Sensitivity</a></li>
        <li><a href="http://growchinook.fw.oregonstate.edu/TestSens2.py">Run Advanced Sensitivity</a></li>

        <li><a class="current" href="http://growchinook.fw.oregonstate.edu/TestSumm.py">Run Multiple Months</a></li>
        <li><a href="http://growchinook.fw.oregonstate.edu/Curves.html">Temperature and Daphnia Curves</a></li>
        <li><a href="http://growchinook.fw.oregonstate.edu/about.html">About</a></li>
        
    </ul>

<body>
    <h2>Enter Values to GrowChinook</h2>
    <div id="formwrap">
        <form action="RunModelMult.py" method="post" target="_blank">
           <div>
               <label class="dd">Select Year:</label> <select name="Year" id="ddy" onchange="configureDropDownLists(this,document.getElementById('ddm1'),document.getElementById('dds'))">
                    <option value=""></option>
                    <option value="2015">2015</option>

                    
               </select>

               <label class="dd">Select Site:</label> <select name="Site" id="dds">
               </select>

               <label class="dd">Select Starting Month:</label> <select name="Month1" id="ddm1" onchange="configureMonthDropDowns(this,document.getElementById('ddm2'))">
               </select>
               
               <label class="dd">Select Ending Month:</label> <select name="Month2" id="ddm2" onchange="configureMonthDropDowns(this,document.getElementById('ddm2'))">
               </select>
               <br>
               <div style="float:left;">
                <label>Enter Name to Display on Tab:</label>
                <input type="text" style="width:50%;" name="TabName" id="TabNameID">
                </div><br>
                                <div id="subutt">
                    <input type="submit" value="Submit"/>
                </div>
            </div><br>
        </form>
    </div>

</body>
''')
print ('</html>')
