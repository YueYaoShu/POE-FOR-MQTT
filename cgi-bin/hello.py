#!/usr/bin/python
import time

print "Content-type:text/html\n\n"

print '<html>'
print '<head>'
print '<title>Hello Word - First CGI Program</title>'
print '</head>'
print '<body>'
print '<h2>'+time.strftime('%Y-%m-%d %X', time.localtime(time.time()))+'</h2>'
print '</body>'
print '</html>'
