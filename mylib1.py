# EPlusInterface (EPI) - An interface for EnergyPlus
# Copyright (C) 2004 Santosh Philip


# This file is part of EPlusInterface.
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
# VERSION: 0.2




import string


def writeStr2File(pathname,s):
#	writes a string to file
	fname=pathname
	f=open(fname,'wb')
	f.write(s)
	f.close()
	
def readfile(pathname):
#	retrun the data in the file
	f=open(pathname,'rb')
	data=f.read()
	f.close()	
	return data

