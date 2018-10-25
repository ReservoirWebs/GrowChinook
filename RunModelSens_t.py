#!/usr/bin/python

import csv
import matplotlib
matplotlib.use('Agg')
from Bioenergetics import *
import cgi
import time
import cgitb
import pylab
import base64
import PrintPages_test as pt

PROCESS_ID = os.getpid()
ADDRESS = cgi.escape(os.environ["REMOTE_ADDR"])
SCRIPT = "Adv Sensitivity Run Page"

log_start = time.time()
pt.write_log_entry(SCRIPT, ADDRESS)
log_end = time.time()


CWD = os.getcwd()
scruffy(CWD, CWD, 'output*')
scruffy('uploads/daph/', CWD, '*')
scruffy('uploads/temp/', CWD, '*')

cgitb.enable()
form = cgi.FieldStorage()
vals = Form_Data_Packager(form)
pt.print_header(vals.title, 'Sens')
print("<br>Log write time: ")
print(log_end-log_start)
print('<br>')
try:
    FRESH_BATCH = Batch(vals.site_data, vals.starting_mass, vals.daph_data, vals.max_temp, vals.min_temp, vals.cust_temp, vals.elev, vals.pop_site, None, None, None, None, None)
    BASE_RESULTS, DAPHNIA_CONSUMED, CONDITION, CONDITION1, DAY_TEMP, NIGHT_TEMP,\
    POPULATION_ESTIMATE = FRESH_BATCH.Run_Batch()
    sens_factors = sensitivity_expand(form)
    results, growths, growths1, csv_headers, sens_inputs, SHORT_RESULTS, tx, tx1 = run_sensitivity(sens_factors, form.getvalue('Sens_Param'), vals.site_data, vals.starting_mass, vals.daph_data, vals.max_temp, vals.min_temp, vals.cust_temp, vals.elev, vals.pop_site, None, None)
except:
    cgitb.handler()


plot_start = time.time()
fig=pyplot.figure(facecolor='#c8e9b1')
fig.suptitle('Spring Chinook', fontsize=20)
ax2 = fig.add_subplot(211)
ax2.plot(sens_inputs, growths1)
ax2.set_ylabel('Day 1 Growth Rate')
ax2.set_xlabel('%s Input Value' % form.getvalue('Sens_Param'))
ax2.grid()
ax3 = fig.add_subplot(212)
ax3.plot(sens_inputs,growths)
ax3.set_ylabel('Final Growth Rate')
ax3.set_xlabel('%s Input Value' % form.getvalue('Sens_Param'))
ax3.grid()
pyplot.subplots_adjust(top=0.3)
fig.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
pid = os.getpid()
pylab.savefig(("new_%s.png" % pid),facecolor=fig.get_facecolor(), edgecolor='lightblue')
data_uri = base64.b64encode(open(('new_%s.png' % pid), 'rb').read()).decode('utf-8').replace('\n', '')
img_tag = '<img class="results" src="data:image/png;base64,{0}">'.format(data_uri)
print(img_tag)
plot_end = time.time()
print("<br>Plot time: ")
print(plot_end-plot_start)
print('<br>')

start_write_time = time.time()
LONG_OUT_FILENAME = ("output_%s.csv" % pid)
with open(LONG_OUT_FILENAME, 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(BASE_RESULTS.keys())
    writer.writerows(zip(*BASE_RESULTS.values()))
outfile.close()
SHORT_OUT_FILENAME = ("output_short_%s.csv" % pid)
with open(SHORT_OUT_FILENAME, 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(SHORT_RESULTS.keys())
    writer.writerows(zip(*SHORT_RESULTS.values()))
outfile.close()
end_write_time = time.time()
print("<br>Write Time:")
print((end_write_time - start_write_time))

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
form_start = time.time()
pt.print_full_form(LONG_OUT_FILENAME, SHORT_OUT_FILENAME, 'out', 'RunModelSens_test.py')
extension = 'csv'
os.chdir('uploads')
result = [i for i in glob.glob('*.csv')]

print('''
{}
</div>
</body>
'''.format(result))
form_end = time.time()
print('</html>')

os.chdir('..')
os.remove(("new_%s.png" % PROCESS_ID))

quit()
