"""
Dillo Tools - window
"""


import dilloTools
import logging
from pymel.core import *


LOG = logging.getLogger('dilloTools')


__WIN_NAME__ = 'dilloToolsWin'

def createWindow(tools):
    win = DilloToolsWindow()
    win.setTools(tools)
    win.create()
    del win


class DilloToolsWindow(object):
    """
    Class for displaying Dillo Tools in an organized window.
    
    The window consists of categorized frameLayouts that have
    a corresponding title and color. Tools are added as
    iconTextButtons to a gridLayout inside each category's
    frameLayout. Buttons are included for expanding/collapsing
    all layouts simultaneously.
    
    Currently, the grid layouts are hard coded to be
    6 icons wide, but this will later become dynamic.
    """
    
    def __init__(self):
        self.name = __WIN_NAME__
        self.title = 'Dillo Tools {0}'.format(dilloTools.getVersion())
        self.mainColumn = None
        self.heightBuffer = 0
        self.bgMult = .75
        self.gridColor = [0.26, 0.26, 0.26]
        self.cats = {}
        self._tools = None
    
    def setTools(self, tools):
        self._tools = tools
    
    def create(self):
        """Create the Dillo Tools Window and show it"""
        #create window
        if window(self.name, ex=True):
            deleteUI(self.name)
        if windowPref(self.name, ex=True):
            windowPref(self.name, e=True, w=2, h=2)
        
        with window(self.name, w=2, h=2, t=self.title):
            with columnLayout(adj=True) as self.mainColumn:
                self.createCollapseButtons()
                self.createAllTools()
        
        #calculate the height of OS specific GUI for resizing later
        self.heightBuffer = window(self.name, q=True, h=True) - layout(self.mainColumn, q=True, h=True)
    
    def createCollapseButtons(self):
        """Create the collapse and expand buttons"""
        with formLayout(nd=100) as form:
            expBtn = button(l='Expand All', h=20, bgc=[0.26, 0.26, 0.26], c=Callback(self.collapseAll, False))
            cllBtn = button(l='Collapse All', h=20, bgc=[0.26, 0.26, 0.26], c=Callback(self.collapseAll, True))
        formLayout(form, e=True,
            af=[(expBtn, 'left', 1), (cllBtn, 'right', 1)],
            ap=[(expBtn, 'right', 1, 50), (cllBtn, 'left', 1, 50)]
        )
    
    def createAllTools(self):
        """Loop through all categories and tools and add them"""
        for cat in self._tools['[cats]']:
            #add the category
            self.addCat(cat, self._tools[cat]['[color]'])
            for tool in self._tools[cat]['[tools]']:
                toolData = self._tools[cat][tool]
                ann = getNameAndAnnotation(tool, toolData['annotation'])
                btnKargs = {
                    'ann':ann,
                    'c':toolData['command'],
                    'image':toolData['image'],
                    'stp':toolData['sourceType'],
                }
                self.addToolToCat(cat, tool, btnKargs)
    
    
    def addCat(self, cat, color):
        """Add a frame layout to the window representing a dillo tools category"""
        setParent(self.mainColumn)
        self.cats[cat] = {}
        self.cats[cat]['frame'] = frameLayout(l=cat, li=4,
                                        bgc=color, cll=True, cl=False, bs='etchedOut',
                                        cc=self.updateSize, ec=self.updateSize
                                    )
        self.cats[cat]['form'] = formLayout(nd=100, bgc=[self.bgMult * c for c in color])
        self.cats[cat]['grid'] = gridLayout(bgc=self.gridColor, cwh=[34, 34], nc=6, nr=10)
        formLayout(self.cats[cat]['form'], e=True,
            af=[(self.cats[cat]['grid'], 'top', 2), (self.cats[cat]['grid'], 'bottom', 2),
                (self.cats[cat]['grid'], 'left', 2), (self.cats[cat]['grid'], 'right', 2), ]
        )
        self.updateSize()
    
    
    def addToolToCat(self, cat, title, btnKargs):
        """Add an icon button for the tool to the specificed category.
        stp is the script type (mel/python)"""
        setParent(self.cats[cat]['grid'])
        iconTextButton(w=32, h=32, style="iconOnly", **btnKargs)
    
    def collapseAll(self, collapse):
        layouts = layout(self.mainColumn, q=True, ca=True)
        for lay in layouts:
            if frameLayout(lay, ex=True):
                frameLayout(lay, e=True, cl=collapse)
        self.updateSize()
    
    def updateSize(self):
        """Call the updateSizeDeferred method using mel's evalDeferred"""
        evalDeferred(self.updateSizeDeferred)
    
    def updateSizeDeferred(self):
        """Reset the height of the window to fit all categories and tools appropriately"""
        layouts = layout(self.mainColumn, q=True, ca=True)
        hTotal = 0
        if layouts:
            for lay in layouts:
                hTotal += layout(lay, q=True, h=True)
        hNew = hTotal + self.heightBuffer
        window(self.name, e=True, h=hNew)


def getNameAndAnnotation(toolName, annotation):
    if annotation == '':
        return toolName
    else:
        return '{0}: {1}'.format(toolName, annotation)


