#!/usr/bin/python

import csv
import matplotlib
matplotlib.use('Agg')
from Bioenergetics import *
import cgi
import cgitb
import pylab
import base64
import PrintPages as pt

PROCESS_ID = os.getpid()
ADDRESS = cgi.escape(os.environ["REMOTE_ADDR"])
SCRIPT = "Main Model Run Page"
pt.write_log_entry(SCRIPT, ADDRESS)
form = cgi.FieldStorage()
CWD = os.getcwd()
scruffy(CWD, CWD, 'output*')
scruffy('uploads/daph/', CWD, '*')
scruffy('uploads/temp/', CWD, '*')
pt.print_header(form.getvalue('TabName'), 'Std')
cgitb.enable()
vals = Form_Data_Packager(form)


try:
    FRESH_BATCH = Batch(vals.site_data, vals.starting_mass, vals.daph_data, vals.max_temp, vals.min_temp, vals.cust_temp, vals.elev, vals.pop_site)
    BASE_RESULTS, DAPHNIA_CONSUMED, CONDITION, CONDITION1, DAY_TEMP, NIGHT_TEMP,\
    POPULATION_ESTIMATE = FRESH_BATCH.Run_Batch()
except:
    #print('Content-Type: text/html')
    #print('Location: http://growchinook.fw.oregonstate.edu/error.html')
    #print('<html>')
    #print('<head>')
    #print('<meta http-equiv="refresh" '
    #      'content="0;url=http://growchinook.fw.oregonstate.edu/error.html" />')
    #print('<title>You are going to be redirected</title>')
    #print('</head>')
    #print('<body>')
    #print('Wait <a href="http://growchinook.fw.oregonstate.edu/error.html">'
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
SHORT_RESULTS['Tab Name'].append(vals.title)
SHORT_RESULTS['Elevation'].append(vals.elev)
SHORT_RESULTS['Reservoir(used for elevation)'].append(vals.pop_site)
SHORT_RESULTS['Daphnia Density'].append(vals.total_daphnnia)
SHORT_RESULTS['Light'].append(vals.light)
SHORT_RESULTS['Daphnia Size'].append(vals.daphnia_size)
SHORT_RESULTS['Min Depth'].append(vals.min_dep)
SHORT_RESULTS['Max Depth'].append(vals.max_dep)
SHORT_RESULTS['Min Temp'].append(vals.min_temp)
SHORT_RESULTS['Max Temp'].append(vals.max_temp)
SHORT_RESULTS['Daphnia Year'].append(vals.daph_year)
SHORT_RESULTS['Daphnia Month'].append(vals.daph_month)
SHORT_RESULTS['Daphnia Site'].append(vals.daph_site)
SHORT_RESULTS['Temperature File'].append(vals.cust_temp)
SHORT_RESULTS['Starting Mass'].append(vals.starting_mass)
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

pt.print_in_data(FRESH_BATCH.site, FRESH_BATCH.year, vals.starting_mass, FRESH_BATCH.total_daphnia,
                  FRESH_BATCH.daphnia_size, FRESH_BATCH.light)



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
            ''' %(vals.daph_year, vals.daph_site, vals.daph_month, vals.temp_year, vals.temp_site, vals.temp_month))
if vals.max_dep < 40 or vals.min_dep != -1:
    print('''<div style="width:600px;display:inline-block;font: normal normal 18px
          'Times New Roman', Times, FreeSerif, sans-serif;"><div style="float:left;">
          Depth restricted to between %.2fm and %.2fm.</div><br>''' % (vals.min_dep, vals.max_dep))
if vals.max_temp != 10000 or vals.min_temp != -1:
    print('''<div style="float:left;">
          Temperature restricted to between %.2f degrees and %.2f degrees.</div><br>
          ''' % (vals.max_temp, vals.min_temp))
print('</div>')
pt.print_full_form(LONG_OUT_FILENAME, SHORT_OUT_FILENAME, 'out', 'RunModel.py')
extension = 'csv'
os.chdir('uploads/temp')
result = [i for i in glob.glob('*.csv')]

print('''
{}
</div>
</body>
'''.format(result))
print('</html>')

os.chdir('../..')
os.remove(("new_%s.png" % PROCESS_ID))

quit()