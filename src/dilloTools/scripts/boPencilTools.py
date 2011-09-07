'''
	Pencil Tools
	1.1.3

	created by Bohdon Sayre
	bsayre@c.ringling.edu

	Description:
		Includes tools for exporting to Pencil, an animation program
		for quickly sketching in bitmap and vector modes.

	Version 1.1.3:
	    > Updated to be a part of dilloTools exclusively
		> Layers named nicely and rearranged properly for Pencil (Thanks Keith!)
		> Updated camera layer to use correct resolution
		> GUI() - a GUI for exporting pencil files with custom names, and for changing the default resolution
			The GUI also provides an option for easily adding shelf buttons.
		> export() - a wrapper for creating a PencilExporter instance
			Also allows 'useSelected' option for exporting stepped animation
		> runPencil() - runs the Pencil application
		> PencilApp class for running Pencil.exe
		> PencilExporter class for playblasting and writing Pencil xml files
		
	Feel free to email me with any bugs, comments, or requests!
'''

#TODO:
#I'd like to add a functionality where if the app isn't found, the user can browse for it,
#and the location is stored as an optionVar
#I'd like to store the defaultRes as an optionVar too...


import maya.cmds as cmds
import maya.mel as mel
import os
import dilloTools

#path to the pencil exe
__PENCIL_PATH__ = os.path.join(dilloTools.getDilloDir(), 'programs/Pencil/Pencil.exe')
defaultRes = [853, 480]
__version__ = '1.1.3'

def GUI():
	'''The GUI for Pencil Tools'''
	import maya.mel as mel
	
	#yay!, writing mel GUIs in python :D, don't forget the r (raw) before every triplequote
	melCmd = r'''
	global proc bpentWin() {
	python("import boPencilTools as pencil");
	
	//window name
	$win = "bpentWin";
	
	//check for pre-existing window
	if (`window -ex $win`) deleteUI -wnd $win;
	
	//create window
	window -w 260 -rtf 1 -mb 1 -mxb 0 -t "Pencil Tools '''+__version__+r'''" -mnc ("window -e -t \"Pencil Tools '''+__version__+r'''\" "+$win+";") $win;
	window -e -h 10 $win;
    
	//menus
	menu -l "Add buttons to shelf..." bpentWinMenu;
		menuItem -l "Pencil Tools Window" -c "bpentButtonsToShelf 0 0 1";
		menuItem -l "Export Button" -c "bpentButtonsToShelf 1 0 0";
		menuItem -l "Run Pencil Button" -c "bpentButtonsToShelf 0 1 0";
		menuItem -d 1;
		menuItem -l "All Buttons" -c "bpentButtonsToShelf 1 1 1";
	
	//main layout
	formLayout -nd 100 bpentMainForm;
		string $nameTxt = `text -l "Filename:"`;
		string $resTxt = `text -l "Resolution:"`;
		string $nameHintTxt = `text -en 0 -l "leave blank to use scene name"`;
		textField bpentNameField;
		intField -w 50 -v '''+str(defaultRes[0])+r''' -cc "python(\"pencil.defaultRes[0] = \"+#1)" bpentResWField;
		intField -w 50 -v '''+str(defaultRes[1])+r''' -cc "python(\"pencil.defaultRes[1] = \"+#1)" bpentResHField;
		checkBox -l "Stepped Mode (uses selected objects)" bpentUseSelectedCheck;
		button -l "Export to Pencil" -c "bpentExportBtn;" bpentExportBtn;
		button -l "Run Pencil" -c "python(\"pencil.runPencil()\")" bpentRunBtn;
		string $sep2 = `separator -h 2 -st "in"`;
	
	formLayout -e
		-ap $nameTxt "top" 5 0
		-ap $nameTxt "left" 5 0
		-ap bpentNameField "top" 5 0
		-ac bpentNameField "left" 5 $nameTxt
		-ap bpentNameField "right" 5 100
		
		-ac $nameHintTxt "top" 5 $nameTxt
		-ap $nameHintTxt "left" 38 10
		-ap $nameHintTxt "right" 5 100
		
		-ac $resTxt "top" 8 $nameHintTxt
		-ap $resTxt "left" -80 50
		
		-ac bpentResWField "top" 5 $nameHintTxt
		-ac bpentResWField "left" 3 $resTxt
		
		-ac bpentResHField "top" 5 $nameHintTxt
		-ac bpentResHField "left" 3 bpentResWField
		
	
		-ac bpentUseSelectedCheck "top" 5 bpentResHField
		-ap bpentUseSelectedCheck "left" -100 50
		
		-ac bpentExportBtn "top" 5 bpentUseSelectedCheck
		-ap bpentExportBtn "left" 5 0
		-ap bpentExportBtn "right" 5 100
		
		-ac $sep2 "top" 8 bpentExportBtn
		-ap $sep2 "left" 2 0
		-ap $sep2 "right" 2 100
		
		-ac bpentRunBtn "top" 8 $sep2
		-ap bpentRunBtn "left" 5 0
		-ap bpentRunBtn "right" 5 100
		bpentMainForm;
	
	window -e -w 228 -h 210 $win;
	showWindow $win;
	}
	global proc bpentExportBtn() {
		//gets name and runs the python code
		string $name = `textField -q -tx bpentNameField`;
		int $useSel = `checkBox -q -v bpentUseSelectedCheck`;
		//resolution is built into the pencil.defaultRes
		
		if (size($name)) {
			python("pencil.export(name='"+$name+"', useSelected="+$useSel+")");
		} else {
			python("pencil.export(useSelected="+$useSel+")");
		}
	}
	global proc bpentButtonsToShelf(int $export, int $run, int $gui) {
		if (!$export && !$run)
			return;
		
		global string $gShelfTopLevel;

		if (`tabLayout -exists $gShelfTopLevel`) {
			string $currentShelf = `tabLayout -query -selectTab $gShelfTopLevel`;
			setParent $currentShelf;

			if ($export) {
				shelfButton
					-command "import boPencilTools as pencil\npencil.export(useSelected=True)"
					-label "Export to Pencil"
					-sourceType "python"
					-annotation "Export to Pencil"
					-image1 "dilloPencilExport.bmp"
					-style `shelfLayout -q -style $currentShelf`
					-width `shelfLayout -q -cellWidth $currentShelf`
					-height `shelfLayout -q -cellHeight $currentShelf`;
			}
			if ($run) {
				shelfButton
					-command "import boPencilTools as pencil\npencil.runPencil()"
					-label "Run Pencil"
					-sourceType "python"
					-annotation "Run Pencil"
					-image1 "dilloPencilRun.bmp"
					-style `shelfLayout -q -style $currentShelf`
					-width `shelfLayout -q -cellWidth $currentShelf`
					-height `shelfLayout -q -cellHeight $currentShelf`;
			}
			if ($gui) {
				shelfButton
					-command "import boPencilTools as pencil\npencil.GUI()"
					-label "Run Pencil"
					-sourceType "python"
					-annotation "Pencil Tools Window"
					-image1 "dilloPencilGUI.bmp"
					-style `shelfLayout -q -style $currentShelf`
					-width `shelfLayout -q -cellWidth $currentShelf`
					-height `shelfLayout -q -cellHeight $currentShelf`;
			}
		}
	}
	bpentWin;'''
	print melCmd
	mel.eval(melCmd)

	
def runPencil():
	'''Runs Pencil.exe'''
	pencil = PencilApp()
	pencil.run()
	del pencil

def export(name=None, frames=None, res=defaultRes, objects=None, useSelected=False):
	'''Automatically creates an instance of PencilExporter
	and runs it with the specified settings.
	If objects are specified, only the frames on which
	the objects are keyed are exported.'''
	
	#store selection, to restore it later
	selList = cmds.ls(r=True, sl=True)
	
	if useSelected and selList:
		objects = selList
	
	cmds.select(cl=True)
		
	if objects != None and objects != []:
		frames = getObjectKeys(objects)
	
	exporter = PencilExporter(name, frames, res)
	exporter.run()
	del exporter
	
	if selList:
		cmds.select(selList)

#some helper definitions
def getObjectKeys(objects):
	'''Returns a list of frames on which the objects are keyed.
	Always includes the first and last frame of the playback range.'''
	prange = getPlaybackRange()
	keys = list(prange)
	for object in objects:
		objKeys = cmds.keyframe(object, time=prange, q=True, tc=True)
		if objKeys:
			keys.extend(objKeys)
	
	if keys != []:
		keys = list(set(keys))
		keys.sort()
		return keys
	else:
		return None
def getPlaybackRange():
	'''Returns the current playback range as (min, max).'''
	min = cmds.playbackOptions(q=True, min=True)
	max = cmds.playbackOptions(q=True, max=True)
	return (min, max)
def melPrint(msg):
	msg = msg.replace('\\', '\\\\')
	mel.eval(r' print ("%s\n")' % msg)


class PencilApp():
	'''Used to run Pencil. Retrieves the maya path and locates the exe.
	Pencil.exe should by default be in /MAYA/<version>/programs/Pencil/'''
	def __init__(self):
		self.appPath = __PENCIL_PATH__
	
	def run(self):
		'''Run Pencil.exe.'''
		import subprocess
		
		if self.appPath == None: return
		if os.path.exists(self.appPath):
			subprocess.Popen([self.appPath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		else:
			melPrint('// could not find Pencil application at: %s' % self.appPath)
			
	def getMayaPath(self):
		'''Returns the Maya scripts path, if one exists in sys.path'''
		import sys, re
		for path in sys.path:
			pattern = 'maya(/|\\\\)2009-x64(/|\\\\)scripts(/|\\\\)?$'
			if re.search(pattern, path.lower()):
				#we've found maya/<version>/scripts, but we want only want maya/<version>
				return os.path.split(path)[0]
		return None
	
class PencilExporter():
	'''A class for exporting a playblasted sequence of images and an xml file ready for use in Pencil.'''
	def __init__(self, name=None, frames=None, res=defaultRes, ):
		self.data = {}
		#evaluate the name, this will be the name of the file and it's data directory
		if name == None:
			name = os.path.splitext(os.path.basename(cmds.file(q=True, sn=True)))[0]
			if name == '':
				name = 'untitled'
		self.name = name
		self.data['frames'] = frames
		self.data['res'] = res
		self.getAllPaths()
	
	def getAllPaths(self):
		'''Retrieves all paths involved in exporting for Pencil.'''
		self.data['projectPath'] = cmds.workspace(q=True, fn=True)
		self.data['pencilPath'] = os.path.join(self.data['projectPath'], 'pencil')
		self.data['pencilDataPath'] = os.path.join(self.data['pencilPath'], '%s.data' % self.name)
		#normalize all paths
		for item in ['projectPath', 'pencilPath', 'pencilDataPath']:
			if item in self.data:
				self.data[item] = os.path.normpath(self.data[item])
		
	def run(self):
		'''Playblasts the frame range, creates the pencil xml file and runs Pencil.exe'''
		frames = self.getFrames()
		self.playblast(frames)
		data = self.buildXML(frames)
		filename = os.path.join(self.data['pencilPath'], self.name)
		self.writeFile(filename, data)
		melPrint('saved file: %s' % filename)
		runPencil()
	
	def initPaths(self):
		'''Creates (if necessary) the project's 'pencil' path
		as well as the data folder for the current name.'''
		
		if not os.path.exists(self.data['pencilPath']):
			os.mkdir(self.data['pencilPath'])
		
		if not os.path.exists(self.data['pencilDataPath']):
			os.mkdir(self.data['pencilDataPath'])

	def playblast(self, frames):
		'''Playblasts the current range to the project's 'pencil' folder'''
		
		#make sure the projects pencil path and name.data path exists
		self.initPaths()
		
		filename = os.path.join(self.data['pencilDataPath'], self.name)
		
		#temporarily set image format to png
		curTime = cmds.currentTime(q=True)#remember current time
		oldFormat = cmds.getAttr('defaultRenderGlobals.imageFormat')#remember image format
		cmds.setAttr('defaultRenderGlobals.imageFormat', 32)
		cmds.playblast(filename=filename, frame=frames, format='image', forceOverwrite=True, framePadding=4, w=self.data['res'][0], h=self.data['res'][1], percent=100, viewer=False)
		cmds.setAttr('defaultRenderGlobals.imageFormat', oldFormat)#restore last image format
		cmds.currentTime(curTime)#restore current time
	
	def getFrames(self):
		'''Returns the custom list of frames.
		If no list exists, returns the current playback range.'''
		if self.data['frames'] == None:
			prange = getPlaybackRange()
			frames = range(int(prange[0]), int(prange[1])+1)
		else:
			frames = self.data['frames']
		
		return frames
	
	
	def buildXML(self, frames):
		'''Generates an xml string representing the playblasted images.
		Offsets the frame numbering in Pencil so that the animation always starts at frame 1.'''
		if frames == None: return
		frames.sort()
		pos = [str(int(-self.data['res'][0]/2)), str(int(-self.data['res'][1]/2))]
		offset = 1 - frames[0]
		
		data = '<!DOCTYPE PencilDocument>\n<document>'
		data += '\n\t<editor>\n\t\t<currentLayer value="1" />\n\t\t<currentFrame value="1" />\n\t\t<currentView dx="0" dy="0" m21="0" m11="1" m22="1" m12="0" />\n\t</editor>\n\t<object>'
		data += '\n\t\t<layer visibility="1" type="1" id="2" name="Maya Layer" >'
		i=0
		for num in frames:
			data += '\n\t\t\t<image topLeftX="'+pos[0]+'" topLeftY="'+pos[1]+'" frame="%d" src="%s.%04d.png" />' % (num+offset, self.name, i)
			i += 1
		data += '\n\t\t</layer>'
		data += '\n\t\t<layer visibility="1" type="1" id="1" name="Drawing Layer" >\n\t\t</layer>'
		data += '\n\t\t<layer width="%d" visibility="0" height="%d" type="5" name="Camera Layer" >\n\t\t<camera dx="0" dy="0" m21="0" m11="1" m22="1" m12="0" frame="1" />\n\t\t</layer>\n\t</object>\n</document>' % (self.data['res'][0], self.data['res'][1])
		
		return data
	
	def writeFile(self, filename, data):
		'''Writes a string(data) to filename.'''
		try:
			fsock = open(filename, 'w')
			try:
				fsock.write(data+'\n')
			finally:
				fsock.close()
		except IOError:
			melPrint(r'// could not open file %s' % filename)