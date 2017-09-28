#!/usr/bin/python

import os
import glob
import cgi
import PrintPages as pt

address = cgi.escape(os.environ["REMOTE_ADDR"])
script = "Advanced Sens Form"
pt.write_log_entry(script, address)
pt.print_header('GrowChinook', 'AdvSens')
pt.print_adv_sens_form(None, None, 'Sens_in', 'RunModelSens2.py')
print ('</html>')