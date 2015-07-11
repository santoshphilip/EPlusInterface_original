# EPlusInterface (EPI) - An interface for EnergyPlus
# Copyright (C) 2004 Santosh Philip

# This file is part of EPlusInterface.
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
# VERSION: 0.2

#last update 21 Apr 2004


#this is a test version ... not for real use
#dammit i am using it

import sys
import getopt
import os
import string
import user
import copy



sys.path.append(user.home+'/Library/PythonFiles')
import mylib1,mylib2,mylib3



def removecomment(st,c):
	# the comment is similar to that in python.
	# any charachter after the # is treated as a comment 
	# until the end of the line
	# st is the string to be de-commented
	# c is the comment phrase
	linesep=mylib3.getlinesep(st)
	ls=st.split(linesep)
	for i in range(len(ls)):
		l=ls[i].split(c)
		ls[i]=l[0]
	
	return string.join(ls,linesep)
	

class idd:
	def __init__(self,dictfile,version=2):
		if version==2:
			# version==2. This is a just a flag I am using
			# it may wind up being the only type... then I can clean this up 
			# and not use the other option
			self.dt,self.dtls=self.initdict2(dictfile)
			return
		self.dt,self.dtls=self.initdict(dictfile)
		
	def initdict2(self,dictfile):			
		dt={}
		dtls=[]
		d=dictfile
		for el in d:
			dt[el[0].upper()]=[] #dict keys for objects always in caps
			dtls.append(el[0].upper())
		return dt,dtls

	def initdict(self,fname):
		st=mylib2.readfile(fname)
		nocom=removecomment(st,'!')
		idfst=nocom
		nocom=removecomment(idfst,'\\')
		idfst=nocom
		ls=string.split(idfst,';')
		lss=[]
		for el in ls:
			lst=string.split(el,',')
			lss.append(lst)
			
		for i in range(0,len(lss)):
			for j in range(0,len(lss[i])):
				lss[i][j]=lss[i][j].strip()
			
		dt={}
		dtls=[]
		for el in lss:
			if el[0]=='':continue
			dt[el[0].upper()]=[]
			dtls.append(el[0].upper())
			
		return dt,dtls



class eplusdata:

	def __init__(self,dictfile=None,fname=None):
		if fname==None and dictfile==None:
			self.dt,self.dtls={},[]
		if isinstance(fname,str) and isinstance(dictfile,str):
			self.makedict(dictfile,fname)
		if isinstance(dictfile,str) and fname==None:
			self.initdict(dictfile)
		if isinstance(dictfile,idd) and fname==None:
			self.initdict(dictfile)
		if isinstance(fname,str) and isinstance(dictfile,idd):
			self.makedict(dictfile,fname)

	def __repr__(self):
		#print dictionary
		dt=self.dt
		dtls=self.dtls
		dossep=mylib3.dossep
		st=''
		for node in dtls:
			nodedata=dt[node.upper()]
			for block in nodedata:
				for i in range(len(block)):
					format='     %s,'+dossep
					if i==0:format='%s,'+dossep
					if i==len(block)-1:format='     %s;'+dossep*2
					st=st+ format %block[i]
		
		return st

	#------------------------------------------
	def initdict(self,fname):
		#create a blank dictionary
		if isinstance(fname,idd):
			self.dt,self.dtls=fname.dt,fname.dtls
			return self.dt,self.dtls
		
		st=mylib2.readfile(fname)
		nocom=removecomment(st,'!')
		idfst=nocom
		nocom=removecomment(idfst,'\\')
		idfst=nocom
		ls=string.split(idfst,';')
		lss=[]
		for el in ls:
			lst=string.split(el,',')
			lss.append(lst)
		
		for i in range(0,len(lss)):
			for j in range(0,len(lss[i])):
				lss[i][j]=lss[i][j].strip()
		
		dt={}
		dtls=[]
		for el in lss:
			if el[0]=='':continue
			dt[el[0].upper()]=[]
			dtls.append(el[0].upper())
		
		self.dt,self.dtls=dt,dtls
		return dt,dtls
	
	#------------------------------------------
	def makedict(self,dictfile,fname):
		#stuff file data into the blank dictionary
		#fname='./exapmlefiles/5ZoneDD.idf'
		#fname='./1ZoneUncontrolled.idf'
		if isinstance(dictfile,idd):
			localidd=copy.deepcopy(dictfile)
			dt,dtls=localidd.dt,localidd.dtls
		else:
			dt,dtls=self.initdict(dictfile)
		st=mylib2.readfile(fname)
		nocom=removecomment(st,'!')
		idfst=nocom
		nocom=removecomment(idfst,'\\')
		idfst=nocom
		ls=string.split(idfst,';')
		lss=[]
		for el in ls:
			lst=string.split(el,',')
			lss.append(lst)
		
		for i in range(0,len(lss)):
			for j in range(0,len(lss[i])):
				lss[i][j]=lss[i][j].strip()
		
		for el in lss:
			node=el[0].upper()
			if dt.has_key(node):
				#stuff data in this key
				dt[node.upper()].append(el)
			else:
				#scream
				if node=='':continue
				print 'this node -%s-is not present in base dictionary'%(node)
			
		self.dt,self.dtls=dt,dtls
		return dt,dtls
	
	def replacenode(self,othereplus,node):
		#replace the node here with the node from othereplus
		node=node.upper()
		self.dt[node.upper()]=othereplus.dt[node.upper()]
	
	def add2node(self,othereplus,node):
		#add the node here with the node from othereplus
		#this will potentially have duplicates
		node=node.upper()
		self.dt[node.upper()]=self.dt[node.upper()] + othereplus.dt[node.upper()]
	
	def getrefs(self,reflist):
		"""
		reflist is got from getobjectref in parse_idd.py
		getobjectref returns a dictionary. 
		reflist is an item in the dictionary
		getrefs gathers all the fields refered by reflist
		"""
		ls=[]
		for el in reflist:
			if self.dt.has_key(el[0].upper()):
				for elm in self.dt[el[0].upper()]:
					ls.append(elm[el[1]])
		return ls

	
#------------------------------------------

