#!/usr/bin/python

import os
import glob
import cgi
import PrintPages_db as pt

address = cgi.escape(os.environ["REMOTE_ADDR"])
script = "Main Model Form"
pt.write_log_entry(script, address)
pt.print_header('GrowChinook', 'Std')
pt.print_full_form(None, None, 'in', 'RunModel_db.py')
os.chdir('uploads/temp/')
temp_result = [i for i in glob.glob('*.csv')]
os.chdir('../..')
os.chdir('uploads/daph/')
daph_result = [i for i in glob.glob('*.csv')]

print('''
{}
</div>
<div style="width:100%; float:right;">
        Here is a list of uploaded daphnia files:{}
</div>
</body>
'''.format(temp_result, daph_result))
print('</html>')
