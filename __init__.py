import os
import inspect
def test():
	return None
from os.path import basename

dir = os.path.abspath(inspect.getsourcefile(test))
dir =  os.path.dirname(dir)
import sys	

filename = dir + '/database.py'
import database
execfile(filename)
filename = dir + '/web_interface.py'
execfile(filename)

