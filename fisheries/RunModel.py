#!/usr/bin/python

import csv
import cgi
import cgitb
import base64
import glob
import matplotlib
matplotlib.use('Agg')
import pylab
from Bioenergetics import *
import PrintPages as pt

FC_MIN_EL = 685.7
HC_MIN_EL = 1246.7
LP_MIN_EL = 702.1
PROCESS_ID = os.getpid()
ADDRESS = cgi.escape(os.environ["REMOTE_ADDR"])
SCRIPT = "Main Model Run Page"
pt.write_log_entry(SCRIPT, ADDRESS)

#CWD = os.getcwd()
#scruffy(CWD, CWD, 'output*')
#scruffy('../htdocs/uploads', CWD, '*')
cgitb.enable()
FORM = cgi.FieldStorage()
TITLE = is_none(FORM.getvalue('TabName'), 'GrowChinook Results')
TEMP_CURVE = FORM.getvalue('tempCurve')
STARTING_MASS = float(is_none(FORM.getvalue('Starting_Mass_In'), 20))
TOTAL_DAPHNIA = float(is_none(FORM.getvalue('Total_Daphnia_Input_Name'), float(is_none(FORM.getvalue('TotDDef'), 123456))))
DAPHNIA_SIZE = float(is_none(FORM.getvalue('Daphnia Size'), float(is_none(FORM.getvalue('DaphSDef'), 123456))))
LIGHT_EX_CO = float(is_none(FORM.getvalue('Light'), float(is_none(FORM.getvalue('LightDef'), 123456))))
YEAR = is_none(FORM.getvalue('Year'), '2015')
MONTH = is_none(FORM.getvalue('Month1'), 'June')
SITE = is_none(FORM.getvalue('Site'), 'Fall Creek')
MAX_DEPTH = float(is_none(FORM.getvalue('DmaxIn'), 10000))
MIN_DEPTH = float(is_none(FORM.getvalue('DminIn'), -1))
MAX_TEMP = float(is_none(FORM.getvalue('TmaxIn'), 10000))
MIN_TEMP = float(is_none(FORM.getvalue('TminIn'), -1))
if MIN_TEMP == MAX_TEMP:
    MAX_TEMP = MAX_TEMP + 1

POP_EST_SITE = is_none(FORM.getvalue('ESite'), SITE)
ELEVATION = float(is_none(FORM.getvalue('Elev'), 10000))
if POP_EST_SITE == 'Fall Creek':
    MAX_DEPTH = min(((ELEVATION-FC_MIN_EL)/3.281), MAX_DEPTH)
elif POP_EST_SITE == 'Lookout Point':
    MAX_DEPTH = min(((ELEVATION-LP_MIN_EL)/3.281), MAX_DEPTH)
elif POP_EST_SITE == 'Hills Creek':
    MAX_DEPTH = min(((ELEVATION-HC_MIN_EL)/3.281), MAX_DEPTH)

DAPHNIA_YEAR = is_none(FORM.getvalue('DYear'),YEAR)
DAPHNIA_MONTH = is_none(FORM.getvalue('DMonth'), MONTH)
DAPHNIA_SITE = is_none(FORM.getvalue('DSite'), SITE)
TEMP_YEAR = is_none(FORM.getvalue('TYear'), YEAR)
TEMP_MONTH = is_none(FORM.getvalue('TMonth'), MONTH)
TEMP_SITE = is_none(FORM.getvalue('TSite'), SITE)
if FORM.getvalue('CustTemp') is None:
    TEMP_YEAR = is_none(FORM.getvalue('TYear'), YEAR)
    TEMP_MONTH = is_none(FORM.getvalue('TMonth'), MONTH)
    TEMP_SITE = is_none(FORM.getvalue('TSite'), SITE)
    TEMP_CURVE = '{0}_T_{1}_{2}.csv'.format(TEMP_SITE, TEMP_MONTH, TEMP_YEAR)
else:
    TEMP_CURVE = 'uploads/{}'.format(FORM.getvalue('CustTemp'))

pt.print_header(TITLE)
LIGHT_EX_CO, TOTAL_DAPHNIA, DAPHNIA_SIZE = get_vals(LIGHT_EX_CO, TOTAL_DAPHNIA, DAPHNIA_SIZE,
                                                        SITE, MONTH, YEAR)
SITE_DATA = Site_Data(YEAR, SITE, MONTH, LIGHT_EX_CO, MAX_DEPTH, MIN_DEPTH)
DAPH_DATA = Daph_Data(TOTAL_DAPHNIA, DAPHNIA_SIZE, DAPHNIA_YEAR, DAPHNIA_SITE, DAPHNIA_MONTH)

try:
    FRESH_BATCH = Batch(SITE_DATA, STARTING_MASS, DAPH_DATA, MAX_TEMP, MIN_TEMP, TEMP_CURVE, ELEVATION, POP_EST_SITE)
    BASE_RESULTS, DAPHNIA_CONSUMED, CONDITION, CONDITION1, DAY_TEMP, NIGHT_TEMP,\
    POPULATION_ESTIMATE = FRESH_BATCH.Run_Batch()
except:
    #print('Content-Type: text/html')
    #print('Location: http://cas-web0.biossys.oregonstate.edu/error.html')
    #print('<html>')
    #print('<head>')
    #print('<meta http-equiv="refresh" '
    #      'content="0;url=http://cas-web0.biossys.oregonstate.edu/error.html" />')
    #print('<title>You are going to be redirected</title>')
    #print('</head>')
    #print('<body>')
    #print('Wait <a href="http://cas-web0.biossys.oregonstate.edu/error.html">'
    #      'Click here if you are not redirected</a>')
    #print('</body>')
    #print('</html>')
    cgitb.handler()

SHORT_RESULTS = {'Tab Name':[], 'Elevation':[], 'Reservoir(used for elevation)':[],
                 'Daphnia Density':[], 'Light':[], 'Daphnia Size':[],
                 'Min Depth':[], 'Max Depth':[], 'Min Temp':[], 'Max Temp':[],
                 'Daphnia Year':[], 'Daphnia Month':[], 'Daphnia Site':[],
                 'Temperature File':[], 'Starting Mass':[], 'Ending Mass':[],
                 'Day Depth':[], 'Day Temperature':[], 'Night Depth':[],
                 'Night Temperature':[], 'Day 1 Growth':[], 'Day 30 Growth':[],
                 'Daphnia Consumed':[], 'Sustainable Estimate':[],
                 'Estimated Condition Change':[]}
SHORT_RESULTS['Tab Name'].append(TITLE)
SHORT_RESULTS['Elevation'].append(ELEVATION)
SHORT_RESULTS['Reservoir(used for elevation)'].append(POP_EST_SITE)
SHORT_RESULTS['Daphnia Density'].append(TOTAL_DAPHNIA)
SHORT_RESULTS['Light'].append(LIGHT_EX_CO)
SHORT_RESULTS['Daphnia Size'].append(DAPHNIA_SIZE)
SHORT_RESULTS['Min Depth'].append(MIN_DEPTH)
SHORT_RESULTS['Max Depth'].append(MAX_DEPTH)
SHORT_RESULTS['Min Temp'].append(MIN_TEMP)
SHORT_RESULTS['Max Temp'].append(MAX_TEMP)
SHORT_RESULTS['Daphnia Year'].append(DAPHNIA_YEAR)
SHORT_RESULTS['Daphnia Month'].append(DAPHNIA_MONTH)
SHORT_RESULTS['Daphnia Site'].append(DAPHNIA_SITE)
SHORT_RESULTS['Temperature File'].append(TEMP_CURVE)
SHORT_RESULTS['Starting Mass'].append(STARTING_MASS)
SHORT_RESULTS['Ending Mass'].append(BASE_RESULTS['StartingMass'][29])
SHORT_RESULTS['Day Depth'].append(BASE_RESULTS['day_depth'][29])
SHORT_RESULTS['Day Temperature'].append(DAY_TEMP)
SHORT_RESULTS['Night Depth'].append(BASE_RESULTS['night_depth'][29])
SHORT_RESULTS['Night Temperature'].append(NIGHT_TEMP)
SHORT_RESULTS['Day 1 Growth'].append(BASE_RESULTS['growth'][0])
SHORT_RESULTS['Day 30 Growth'].append(BASE_RESULTS['growth'][29])
SHORT_RESULTS['Daphnia Consumed'].append(DAPHNIA_CONSUMED)
SHORT_RESULTS['Sustainable Estimate'].append(POPULATION_ESTIMATE)
SHORT_RESULTS['Estimated Condition Change'].append(CONDITION)

FIG = pyplot.figure()
FIG = pyplot.figure(facecolor='#c8e9b1')
FIG.suptitle('Juvenile Spring Chinook', fontsize=20)
MASS_PLOT = FIG.add_subplot(221)
MASS_PLOT.plot(BASE_RESULTS['StartingMass'], label="Mass (g)")
MASS_PLOT.set_ylabel('Mass (g)')
MASS_PLOT.set_xlabel('Day of Month')
GROWTH_PLOT = FIG.add_subplot(222)
GROWTH_PLOT.plot(BASE_RESULTS['growth'])
GROWTH_PLOT.set_ylabel('Growth (g/g/d)')
GROWTH_PLOT.set_xlabel('Day of Month')
DAY_DEPTH_PLOT = FIG.add_subplot(223)
DAY_DEPTH_PLOT.plot(BASE_RESULTS['day_depth'], 'black', label="Day Depth (m)")
DAY_DEPTH_PLOT.set_ylabel('Day Depth (m)')
DAY_DEPTH_PLOT.set_xlabel('Day of Month')
DAY_DEPTH_PLOT.set_ylim(35, 0)
DAY_DEPTH_PLOT.yticklabels = (np.arange(0, 35, 5))
NIGHT_DEPTH_PLOT = FIG.add_subplot(224)
NIGHT_DEPTH_PLOT.set_ylabel('Night Depth (m)')
NIGHT_DEPTH_PLOT.set_xlabel('Day of Month')
NIGHT_DEPTH_PLOT.plot(BASE_RESULTS['night_depth'], 'black', label="Night Depth (m)")
NIGHT_DEPTH_PLOT.yticklabels = (np.arange(0, 35, 5))
NIGHT_DEPTH_PLOT.set_ylim(35, 0)
pyplot.subplots_adjust(top=0.3)
FIG.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
pylab.savefig(("new_%s.png" % PROCESS_ID), facecolor=FIG.get_facecolor(), edgecolor='lightblue')
data_uri = base64.b64encode(open(("new_%s.png" % PROCESS_ID), 'rb').read())\
                                  .decode('utf-8').replace('\n', '')
img_tag = '<img class="results" src="data:image/png;base64,{0}">'.format(data_uri)
print(img_tag)


LONG_OUT_FILENAME = ("output_%s.csv" % PROCESS_ID)
with open(LONG_OUT_FILENAME, 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(BASE_RESULTS.keys())
    writer.writerows(zip(*BASE_RESULTS.values()))
outfile.close()
SHORT_OUT_FILENAME = ("output_short_%s.csv" % PROCESS_ID)
with open(SHORT_OUT_FILENAME, 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(SHORT_RESULTS.keys())
    writer.writerows(zip(*SHORT_RESULTS.values()))
outfile.close()

pt.print_in_data(FRESH_BATCH.site, FRESH_BATCH.year, STARTING_MASS, FRESH_BATCH.total_daphnia,
                  FRESH_BATCH.daphnia_size, FRESH_BATCH.light, 'in')



print('''
            </div>
            <div id="outdata">
                <div class="dataleft">Day 1 Output Values:</div>
                <div class="dataleft">Chinook Mass:
                    <div class="dataright">%.1f g</div>
                </div>
                <div class="dataleft">Growth:
                    <div class="dataright">%.2f g/g/day</div>
                </div>
                <div class="dataleft">Day Depth Occupied:
                    <div class="dataright">%.0f m</div>
                </div>
                <div class="dataleft">Night Depth Occupied:
                    <div class="dataright">%.0f m</div>
                </div>
            </div>
            </div>

            <div id="outdata">
                <div class="dataleft">Day 30 Output Values:</div>
                <div class="dataleft">Chinook Mass:
                    <div class="dataright">%.1f g</div>
                </div>
                <div class="dataleft">Growth (day 30):
                    <div class="dataright">%.2f g/g/day</div>
                </div>
                <div class="dataleft">Day Depth Occupied:
                    <div class="dataright">%.0f m</div>
                </div>
                <div class="dataleft">Temp at Day Depth Occupied:
                    <div class="dataright">%.0f &#176;C</div>
                </div>
                <div class="dataleft">Night Depth Occupied:
                    <div class="dataright">%.0f m</div>
                </div>
                <div class="dataleft">Temp at Night Depth Occupied:
                    <div class="dataright">%.0f &#176;C</div>
                </div>
                <div class="dataleft">Total Daphnia Consumed:
                    <div class="dataright">%.0f</div>
                </div>
                <div class="dataleft">Estimated Condition Change:
                <div class="dataright">%+.2f</div>
                </div>
                <div class="dataleft">Population at which Density Dependent Interactions Expected:
                <div class="dataright">%.0f</div>
                </div>
            </div>


       <br>
       ''' % (BASE_RESULTS['StartingMass'][0], BASE_RESULTS['growth'][0],
              BASE_RESULTS['day_depth'][0], BASE_RESULTS['night_depth'][0],
              BASE_RESULTS['StartingMass'][29], BASE_RESULTS['growth'][29],
              BASE_RESULTS['day_depth'][29], DAY_TEMP, BASE_RESULTS['night_depth'][29],
              NIGHT_TEMP, DAPHNIA_CONSUMED, CONDITION, POPULATION_ESTIMATE))

print('''   <div style="margin-top:2px;"><div style="width:600px;display:inline-block;
            font: normal normal 18px 'Times New Roman', Times, FreeSerif, sans-serif;">
            <div style="float:left;">Daphnia Distribution Year: %s,  Site: %s,  and Month: %s
            </div>

            <div style="float:left;">Temperature Distribution Year: %s,  Site: %s,  and Month: %s
            </div>
            </div>
            ''' %(DAPHNIA_YEAR, DAPHNIA_SITE, DAPHNIA_MONTH, TEMP_YEAR, TEMP_SITE, TEMP_MONTH))
if MAX_DEPTH < 40 or MIN_DEPTH != -1:
    print('''<div style="width:600px;display:inline-block;font: normal normal 18px
          'Times New Roman', Times, FreeSerif, sans-serif;"><div style="float:left;">
          Depth restricted to between %.2fm and %.2fm.</div><br>''' % (MIN_DEPTH, MAX_DEPTH))
if MAX_TEMP != 10000 or MIN_TEMP != -1:
    print('''<div style="float:left;">
          Temperature restricted to between %.2f degrees and %.2f degrees.</div><br>
          ''' % (MIN_TEMP, MAX_TEMP))
print('</div>')
pt.print_full_form(LONG_OUT_FILENAME, SHORT_OUT_FILENAME, 'out')
extension = 'csv'
os.chdir('uploads')
result = [i for i in glob.glob('*.csv')]

print('''
{}
</body>
'''.format(result))
print('</html>')

os.chdir('..')
os.remove(("new_%s.png" % PROCESS_ID))

quit()
