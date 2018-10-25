#!/usr/bin/python

import os
import glob
import cgi
import PrintPages_test as pt

address = cgi.escape(os.environ["REMOTE_ADDR"])
script = "Main Model Form"
pt.write_log_entry(script, address)
pt.print_header('GrowChinook', 'Std')
pt.print_full_form(None, None, 'in', 'RunModel.py')
extension = 'csv'
os.chdir('uploads')
result = [i for i in glob.glob('*.csv')]

print('''
{}
</div>
</body>
'''.format(result))
print ('</html>')
