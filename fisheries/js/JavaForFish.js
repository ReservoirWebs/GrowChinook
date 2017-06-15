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
        dds.options.length = 0;
    break;
    }

}

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
}

function updateDepthTextInput(val) {
          document.getElementById('DMaxInID').value=val;
          document.getElementById('DmaxOutID').value=val;
          document.getElementById('DMinInID').value=val;
          document.getElementById('DminOutID').value=val;
        }

function updateTextInput(val,field) {
          document.getElementById(field).value=val;
        }

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

function getDefaultValues(ddy,ddm,dds,smt,tdt,dst,lt){
    var FallCreeklength = {March:31,April:30,May:31,June:30,July:31,August:31,September:30};
    var HillsCreeklength = {March:31,April:30,May:31,June:30,July:31,August:31,September:30};
    var LookoutPointlength = {March:31,April:30,May:31,June:30,July:31,August:31,September:30};

    var FCk = {March:0.834,April:0.596,May:0.58,June:0.72,July:0.521,August:0.509};
    var HCk = {March:0.583,April:0.503,May:0.467,June:0.441,July:0.32,August:0.368};
    var LPk = {March:0.532,April:0.565,May:0.373,June:0.374,July:0.396,August:0.39};
    var FCk14 = {June:0.404,July:0.274,August:0.295};
    var HCk14 = {June:0.298,July:0.274,August:0.274};
    var LPk14 = {June:0.315,July:0.271,August:0.282};
    var BRk14 = {July:0.254};
    var FCk13 = {August:0.487};
    var HCk13 = {August:0.291};
    var BRk13 = {August:0.263};

    var FCd = {March: 620.83,April: 7220.57,May: 10930.27,June: 5020.65,July: 2010.06,August: 1940.78};
    var HCd = {March: 120.57,April: 170.48,May: 5780.05,June: 59310.33,July: 4140.69,August: 3390.29};
    var LPd = {March: 30.14,April: 40.91,May: 5780.05,June: 21110.15,July: 7030.72,August: 13820.30};

    var FCd14 = {June: 4500.13,July: 0,August: 400.72};
    var HCd14 = {June: 2620.39,July: 0,August: 130.70};
    var LPd14 = {June: 5310.56,July: 0,August: 930.87};
    var FCd13 = {June: 8160.81,July: 0,August: 12690.20};
    var HCd13 = {June: 65840.78,July: 0,August: 8400.09};
    var BRd13 = {June: 127670.43,July: 0,August: 16710.33};

    var FCsize = {March:1.207,April:1.248,May:1.139,June:1.305,July:1.514,August:1.145};
    var HCsize = {March:1.455,April:1.077,May:1.053,June:1.045,July:1.769,August:1.516};
    var LPsize = {March:1.457,April:0.957,May:1.064,June:1.247,July:1.664,August:2.002};
    var BRsize = {March:0.628,June:1.497,August:1.252};

    var FCsize = {March:1.207,April:1.248,May:1.139,June:1.305,July:1.514,August:1.145};
    var HCsize = {March:1.455,April:1.077,May:1.053,June:1.045,July:1.769,August:1.516};
    var LPsize = {March:1.457,April:0.957,May:1.064,June:1.247,July:1.664,August:2.002};
    var BRsize = {March:0.628,June:1.497,August:1.252};

    if ((dds.value =='Fall Creek') && (ddy.value == '2015')){
        lt.value = FCk[ddm.value];
    }
    else if ((dds.value =='Hills Creek') && (ddy.value == '2015')){
        lt.value = HCk[ddm.value];
    }
    else if (dds.value  == 'Lookout Point' && ddy.value == '2015'){
        lt.value = LPk[ddm.value];
    }
    else if (dds.value  =='Fall Creek' && ddy.value == '2014'){
        lt.value = FCk14[ddm.value];
    }
    else if (dds.value =='Hills Creek' && ddy.value == '2014'){
        lt.value = HCk14[ddm.value];
    }
    else if (dds.value  == 'Lookout Point' && ddy.value == '2014'){
        lt.value = LPk14[ddm.value];
    }

    if (dds.value  == 'Fall Creek'){
        tdt.value = FCd[ddm.value];
    }
    else if (dds.value == 'Hills Creek'){
        tdt.value = HCd[ddm.value];
    }
    else if (dds.value  == 'Lookout Point'){
        tdt.value = LPd[ddm.value];
    }

    if (dds.value  == 'Fall Creek'){
        dst.value = FCsize[ddm.value];
    }
    else if (dds.value  == 'Hills Creek'){
        dst.value = HCsize[ddm.value];
    }
    else if (dds.value  == 'Lookout Point'){
        dst.value = LPsize[ddm.value];
    }
}

function DepthError(){
window.location = "http://http://cas-web0.biossys.oregonstate.edu/derror.html";
}

function getDefaultValuesScene(ddscene,ddy,ddm,dds,smt,tdt,dst,lt){
    var FallCreeklength = {March:31,April:30,May:31,June:30,July:31,August:31,September:30};
    var HillsCreeklength = {March:31,April:30,May:31,June:30,July:31,August:31,September:30};
    var LookoutPointlength = {March:31,April:30,May:31,June:30,July:31,August:31,September:30};

    var FCk = {March:0.834,April:0.596,May:0.58,June:0.72,July:0.521,August:0.509};
    var HCk = {March:0.583,April:0.503,May:0.467,June:0.441,July:0.32,August:0.368};
    var LPk = {March:0.532,April:0.565,May:0.373,June:0.374,July:0.396,August:0.39};
    var FCk14 = {June:0.404,July:0.274,August:0.295};
    var HCk14 = {June:0.298,July:0.274,August:0.274};
    var LPk14 = {June:0.315,July:0.271,August:0.282};
    var BRk14 = {July:0.254};
    var FCk13 = {August:0.487};
    var HCk13 = {August:0.291};
    var BRk13 = {August:0.263};

    var FCd = {March: 620.83,April: 7220.57,May: 10930.27,June: 5020.65,July: 2010.06,August: 1940.78};
    var HCd = {March: 120.57,April: 170.48,May: 5780.05,June: 59310.33,July: 4140.69,August: 3390.29};
    var LPd = {March: 30.14,April: 40.91,May: 5780.05,June: 21110.15,July: 7030.72,August: 13820.30};

    var FCd14 = {June: 4500.13,July: 0,August: 400.72};
    var HCd14 = {June: 2620.39,July: 0,August: 130.70};
    var LPd14 = {June: 5310.56,July: 0,August: 930.87};
    var FCd13 = {June: 8160.81,July: 0,August: 12690.20};
    var HCd13 = {June: 65840.78,July: 0,August: 8400.09};
    var BRd13 = {June: 127670.43,July: 0,August: 16710.33};

    var FCsize = {March:1.207,April:1.248,May:1.139,June:1.305,July:1.514,August:1.145};
    var HCsize = {March:1.455,April:1.077,May:1.053,June:1.045,July:1.769,August:1.516};
    var LPsize = {March:1.457,April:0.957,May:1.064,June:1.247,July:1.664,August:2.002};
    var BRsize = {March:0.628,June:1.497,August:1.252};

    var FCsize = {March:1.207,April:1.248,May:1.139,June:1.305,July:1.514,August:1.145};
    var HCsize = {March:1.455,April:1.077,May:1.053,June:1.045,July:1.769,August:1.516};
    var LPsize = {March:1.457,April:0.957,May:1.064,June:1.247,July:1.664,August:2.002};
    var BRsize = {March:0.628,June:1.497,August:1.252};

    

    if ((dds.value =='Fall Creek') && (ddy.value == '2015')){
        lt.value = FCk[ddm.value];
    }
    else if ((dds.value =='Hills Creek') && (ddy.value == '2015')){
        lt.value = HCk[ddm.value];
    }
    else if (dds.value  == 'Lookout Point' && ddy.value == '2015'){
        lt.value = LPk[ddm.value];
    }
    else if (dds.value  =='Fall Creek' && ddy.value == '2014'){
        lt.value = FCk14[ddm.value];
    }
    else if (dds.value =='Hills Creek' && ddy.value == '2014'){
        lt.value = HCk14[ddm.value];
    }
    else if (dds.value  == 'Lookout Point' && ddy.value == '2014'){
        lt.value = LPk14[ddm.value];
    }

    if (dds.value  == 'Fall Creek'){
        tdt.value = FCd[ddm.value];
    }
    else if (dds.value == 'Hills Creek'){
        tdt.value = HCd[ddm.value];
    }
    else if (dds.value  == 'Lookout Point'){
        tdt.value = LPd[ddm.value];
    }

    if (dds.value  == 'Fall Creek'){
        dst.value = FCsize[ddm.value];
    }
    else if (dds.value  == 'Hills Creek'){
        dst.value = HCsize[ddm.value];
    }
    else if (dds.value  == 'Lookout Point'){
        dst.value = LPsize[ddm.value];
    }
}
