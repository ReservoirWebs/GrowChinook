#!/usr/bin/python

import os
import glob
import cgi
import PrintPages as pt

address = cgi.escape(os.environ["REMOTE_ADDR"])
script = "Main Model Form"
pt.write_log_entry(script, address)
pt.print_header('GrowChinook')
pt.print_full_form(None, None, 'in')
extension = 'csv'
os.chdir('uploads')
result = [i for i in glob.glob('*.csv')]

print('''
{}
</body>
'''.format(result))
print ('</html>')
