#!/usr/bin/python

import cgi
form = cgi.FieldStorage()


print ('Content-type:text/html\r\n\r\n')
print('<html>')

item = form["filename"]
if item.file:
    data = item.file.read()
    print("Content-Type: text/html")
    print(cgi.escape(data))


print('</html>')