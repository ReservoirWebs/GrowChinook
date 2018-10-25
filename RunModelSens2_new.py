#!/usr/bin/python

import os
import matplotlib
matplotlib.use('Agg')
import sys
import csv
import Bioenergetics_advsens_new as bio
import cgi, cgitb
import pylab
import io
from PIL import Image, ImageDraw
import base64
from matplotlib.ticker import FormatStrFormatter
from matplotlib.font_manager import FontProperties
from scipy.interpolate import griddata
import pandas
import PrintPages as pt

PROCESS_ID = os.getpid()
ADDRESS = cgi.escape(os.environ["REMOTE_ADDR"])
SCRIPT = "Adv Sensitivity Run Page"
pt.write_log_entry(SCRIPT, ADDRESS)

CWD = os.getcwd()
bio.scruffy(CWD, CWD, 'output*')
bio.scruffy('uploads/daph/', CWD, '*')
bio.scruffy('uploads/temp/', CWD, '*')

cgitb.enable()

form = cgi.FieldStorage()
vals = bio.Adv_Sens_Form_Data_Packager(form)
pid = os.getpid()
fname=("output_%s.csv" % pid)
SHORT_OUT_FILENAME = ("output_short_%s.csv" % pid)
pt.print_header(vals.title, 'Sens')
Months2014 = ['June', 'July', 'August']
Months2015 = ['March', 'April', 'May', 'June', 'July', 'August']
Months2016 = ['April', 'May', 'June', 'July', 'August','September']


year = form.getvalue('Year')
if year == '2014':
    months = Months2014
elif year == '2015':
    months = Months2015
else:
    months = Months2016

SensParam = form.getvalue('Sens_Param')
fig = bio.pyplot.figure(facecolor='#c8e9b1')
fontP = FontProperties()
fontP.set_size('small')
fig.suptitle('Spring Chinook', fontsize=20)
ax2 = fig.add_subplot(211)
ax2.set_ylabel('Day 1 Growth Rate')
#ax.set_aspect('equal', adjustable='box')
if SensParam == 'Total Daphnia':
    ax2.set_xlabel('Total Daphnia (Thousands)')
else:
    ax2.set_xlabel('%s' % SensParam)
ax2.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
ax2.grid()
ax3 = fig.add_subplot(212)
ax3.set_ylabel('Final Growth Rate')
#ax.set_aspect('equal', adjustable='box')
if SensParam == 'Total Daphnia':
    ax3.set_xlabel('Total Daphnia (Thousands)')
else:
    ax3.set_xlabel('%s' % SensParam)
ax3.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
ax3.grid()

base_set_flag = 0
base_val = 0

for month in months:
    vals.site_data.month = month
    vals.daph_data.d_month = month
    all_results = []
    all_growths = []
    all_growths1 = []
    all_csv_headers = []
    all_sens_inputs = []
    try:

        vals.site_data.light, vals.daph_data.total_daph, vals.daph_data.daph_size = bio.get_vals(vals.site_data.light, vals.daph_data.total_daph, vals.daph_data.daph_size, vals.site_data.site, vals.site_data.month, vals.site_data.year)
        FRESH_BATCH = bio.Batch(vals.site_data, vals.starting_mass, vals.daph_data, vals.max_temp, vals.min_temp, "None_T_None_None.csv", None, None)
        BASE_RESULTS, DAPHNIA_CONSUMED, CONDITION, CONDITION1, DAY_TEMP, NIGHT_TEMP, \
        POPULATION_ESTIMATE = FRESH_BATCH.Run_Batch()
        sens_factors = bio.sensitivity_expand(form)
        results, growths, growths1, csv_headers, sens_inputs, SHORT_RESULTS, base_val, base_set_flag = bio.run_sensitivity(sens_factors, form.getvalue('Sens_Param'), vals.site_data, vals.starting_mass, vals.daph_data, vals.max_temp, vals.min_temp, "None_T_None_None.csv", None, None, base_val, base_set_flag)
        #all_results.append(results), all_csv_headers.append(csv_headers)
        for i in range(len(growths)):
            all_growths.append(growths[i])
            all_growths1.append(growths1[i])
            all_sens_inputs.append(sens_inputs[i])
        ax2.plot(all_sens_inputs, all_growths1, label=("%s" % month))
        ax3.plot(all_sens_inputs,all_growths, label=("%s" % month))
        with open(fname, 'a') as outfile:
            writer = csv.writer(outfile)
            for i in range(len(all_results)):
                for j in range(len(all_results[i])):
                    writer.writerow(all_csv_headers[i][j])
                    writer.writerow(all_results[i][j].keys())
                    writer.writerows(zip(*all_results[i][j].values()))
        outfile.close()
        with open(SHORT_OUT_FILENAME, 'a') as outfile:
            writer = csv.writer(outfile)
            for results in all_results:
                for set in results:
                    writer.writerow(set.keys())
                    writer.writerows(zip(*set.values()))
        outfile.close()

    except:
        # print('Content-Type: text/html')
        # print('Location: http://growchinook.fw.oregonstate.edu/error.html')
        # print('<html>')
        # print('<head>')
        # print('<meta http-equiv="refresh" '
        #      'content="0;url=http://growchinook.fw.oregonstate.edu/error.html" />')
        # print('<title>You are going to be redirected</title>')
        # print('</head>')
        # print('<body>')
        # print('Wait <a href="http://growchinook.fw.oregonstate.edu/error.html">'
        #      'Click here if you are not redirected</a>')
        # print('</body>')
        # print('</html>')
        cgitb.handler()

art = []
lgd = pylab.legend(prop = fontP,loc=9, bbox_to_anchor=(0.5, -0.1), ncol=3)
bio.pyplot.gcf().subplots_adjust(bottom=0.35)
art.append(lgd)
fig.tight_layout(pad=2, h_pad=None, w_pad=None, rect=None)
pylab.savefig( "new_{}.png".format(pid),facecolor=fig.get_facecolor(), edgecolor='lightblue')
data_uri = base64.b64encode(open('new_{}.png'.format(pid), 'rb').read()).decode('utf-8').replace('\n', '')
img_tag = '<img class="results" src="data:image/png;base64,{0}">'.format(data_uri)
print(img_tag)

pt.print_in_data(FRESH_BATCH.site, FRESH_BATCH.year, vals.starting_mass, FRESH_BATCH.total_daphnia,
                  FRESH_BATCH.daphnia_size, FRESH_BATCH.light)

print('''
            </div>
            
            
            </div>

            


       <br>
       ''')


if vals.site_data.max_depth < 40 or vals.site_data.min_depth != -1:
    print('''<div style="width:600px;display:inline-block;font: normal normal 18px
          'Times New Roman', Times, FreeSerif, sans-serif;"><div style="float:left;">
          Depth restricted to between %.2fm and %.2fm.</div><br>''' % (vals.site_data.min_dep, vals.site_data.max_depth))
if vals.max_temp != 10000 or vals.min_temp != -1:
    print('''<div style="float:left;">
          Temperature restricted to between %.2f degrees and %.2f degrees.</div><br>
          ''' % (vals.max_temp, vals.min_temp))
print('</div>')
pt.print_adv_sens_form(fname, SHORT_OUT_FILENAME, 'out', 'RunModelSens2_test.py')

print('''
</body>
</html>
''')
os.remove('new_{}.png'.format(pid))
quit()