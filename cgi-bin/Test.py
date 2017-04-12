#!/usr/bin/python


import cgi

print ('Content-type:text/html\r\n\r\n')
print('<html>')
print('''<link type="text/css" rel="stylesheet" media="screen" href="/css/Style.css" />
<link type="text/css" rel="stylesheet" media="screen" href="/css/Style.css" />
<img class="head" src="/css/src/LPR.jpg">
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js" type="text/javascript"></script>
    <title>GrowChinook</title>
</head>
<body>
    <ul>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/">Home</a></li>
        <li><a class="current" href="http://cas-web0.biossys.oregonstate.edu/Test.py">Run Standard Model</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSens.py">Run Model With Sensitivity</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/TestSens2.py">Run Advanced Sensitivity</a></li>
        <li><a href="http://cas-web0.biossys.oregonstate.edu/about.html">About</a></li>
    </ul>

<script>
jQuery().ready(function() {
/* Custom select design */
jQuery('.drop-down').append('<div class="button"></div>');
jQuery('.drop-down').append('<ul class="select-list"></ul>');jQuery('.drop-down select option').each(function() {var bg = jQuery(this).css('background-image');jQuery('.select-list').append('<li class="clsAnchor"><span value="' + jQuery(this).val() + '" class="' + jQuery(this).attr('class') + '" style=background-image:' + bg + '>' + jQuery(this).text() + '</span></li>');

});

jQuery('.drop-down .button').html('<span style=background-image:' + jQuery('.drop-down select').find(':selected').css('background-image') + '>' + jQuery('.drop-down select').find(':selected').text() + '</span>' + '<a href="javascript:void(0);" class="select-list-link">Arrow</a>');

jQuery('.drop-down ul li').each(function() {

if (jQuery(this).find('span').text() == jQuery('.drop-down select').find(':selected').text()) {

jQuery(this).addClass('active');

}

});

jQuery('.drop-down .select-list span').on('click', function()

{

var dd_text = jQuery(this).text();
var dd_img = jQuery(this).css('background-image');
var dd_val = jQuery(this).attr('value');

jQuery('.drop-down .button').html('<span style=background-image:' + dd_img + '>' + dd_text + '</span>' + '<a href="javascript:void(0);" class="select-list-link">Arrow</a>');

jQuery('.drop-down .select-list span').parent().removeClass('active');

jQuery(this).parent().addClass('active');

$('.drop-down select[name=tempCurve]').val( dd_val );

$('.drop-down .select-list li').slideUp();

});

jQuery('.drop-down .button').on('click','a.select-list-link', function()

{

jQuery('.drop-down ul li').slideToggle();

});
});
</script>

<script type="text/javascript">
    function configureDropDownLists(ddy,ddm,dds) {
    var years = ['2013', '2014', '2015'];
    var months = ['March', 'April', 'May', 'June', 'July', 'August'];
    var sites = ['Blue River', 'Fall Creek', 'Hills Creek', 'Lookout Point'];

    switch (ddy.value) {
        case '2013':
            ddm.options.length = 0;
            createOption(ddm, "", "");
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

<script type="text/javascript">
    function configureMonthDropDowns(ddm1,ddm2) {
    var months = ['March', 'April', 'May', 'June', 'July', 'August'];
    if(document.getElementById('ddy').value == '2013'){
        ddm2.options.length = 0;
        createOption(ddm2,ddm1.value,ddm1.value);
    }

    else{
    switch (ddm1.value) {
        case 'March':
            ddm2.options.length = 0;
            for (i=0; i<6; i++) {
                createOption(ddm2,months[i],months[i]);
            }
            break;
        case 'April':
            ddm2.options.length = 0;
            for (i=1; i<6; i++) {
                createOption(ddm2,months[i],months[i]);
            }
            break;
        case 'May':
            ddm2.options.length = 0;
            for (i=2; i<6; i++) {
                createOption(ddm2,months[i],months[i]);
            }
            break;
        case 'June':
            ddm2.options.length = 0;
            for (i=3; i<6; i++) {
                createOption(ddm2,months[i],months[i]);
            }
            break;
        case 'July':
            ddm2.options.length = 0;
            for (i=4; i<6; i++) {
                createOption(ddm2,months[i],months[i]);
            }
            break;
        case 'August':
            ddm2.options.length = 0;
            for (i=5; i<6; i++) {
                createOption(ddm2,months[i],months[i]);
            }
            break;
        default:
            ddm.options.length = 0;
        break;
    }
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
          document.getElementByID('LightInID').value=val;
          document.getElementByID('LightOutID').value=val;
        }
</script>

<body>
    <h2>Enter Values to GrowChinook</h2>
    <div id="formwrap">
        <form action="RunModel.py" method="post" target="_blank">   
	   <div class="drop-down">    
	   <select name="tempCurve">     
	   <option value="Lookout Point_smoothed_May_2015.csv" style="background-image:url('images/LP5_15_Temp.png');">Lookout Point, May 2015</option>
           <option value="Fall Creek_smoothed_June_2015.csv" style="background-image:url('images/FC6_15_Temp.png');">Fall Creek, June 2015</option>	       
	   <option value="Hills Creek_smoothed_August_15.csv" style="background-image:url('images/HC8_15_Temp.png');">Hills Creek, August 2015</option>    
	   </select><br><br>
	   </div>

           <div id="sec1">
                <label>Please Select Year:</label> <select name="Year" id="ddy" onchange="configureDropDownLists(this,document.getElementById('ddm1'),document.getElementById('dds'))">
                    <option value=""></option>
                    <option value="2015">2015</option>
                    <option value="2014">2014</option>
                    <option value="2013">2013</option>
               </select>
                <br>
                <br>

                <label>Please Select Site:</label> <select name="Site" id="dds">
                </select>
                <br>
                <br>

                <label>Please Select Starting Month:</label> <select name="Month1" id="ddm1" onchange="configureMonthDropDowns(this,document.getElementById('ddm2'))">
                </select>
                <br>
                <label>Please Select Ending Month:</label> <select name="Month2" id="ddm2">
                </select>
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

                <div id="subutt">
                    <input type="submit" value="Submit"/>
                </div>
            </div><br>
        </form>
    </div>

</body>
''')
print ('</html>')
