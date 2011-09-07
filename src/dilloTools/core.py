"""
Dillo Tools - core
"""


import dilloTools
from pymel.core import *


LOG = dilloTools.getLog('core')


class DilloTools(object):
    """
    The main Dillo Tools class.
    Keeps track of all the tools included in Dillo Tools
    and provides methods for building windows/menus/shelves.
    """
    
    _instance = None
    
    @staticmethod
    def getInstance():
        """Static method for implementing the Singleton class technique"""
        if not DilloTools._instance:
            DilloTools._instance = DilloTools()
        return DilloTools._instance
        
    @staticmethod
    def delInstance():
        """Deletes the instance of DilloTools if it exists"""
        if DilloTools._instance:
            del DilloTools._instance
            DilloTools._instance = None
    
    
    def __init__(self):
        LOG.debug('Building toolset...')
        self._tools = {}
        self._curCat = None
        self._initTools()
    
    def _initTools(self):
        """Clear the tools dictionary"""
        self._tools = {'[cats]':[]}
    
    def getTools(self):
        """Return the current tool data"""
        return self._tools
    
    #Category Management
    def addCat(self, cat, color=None, colorDepth=1, setCurrent=True):
        """Adds a category and sets it as current"""
        normColor = [c/float(colorDepth) for c in color]
        if cat not in self._tools.keys():
            self._tools[cat] = {'[tools]':[], '[color]':normColor}
            self._tools['[cats]'].append(cat)
        self.setCat(cat)
    
    def setCat(self, cat):
        """Sets the specified category as current if it exists"""
        if cat in self._tools.keys():
            self._curCat = cat
    
    
    #Tool Management
    def addToolToCat(self, cat, title, command, image, sourceType='mel', annotation=''):
        """Add a tool to the specificed category.
        sourceType is the script type (mel/python)"""
        if cat in self._tools.keys():
            fullImage = dilloTools.getDilloImage(image)
            self._tools[cat][title] = {'command':command, 'image':fullImage, 'sourceType':sourceType, 'annotation':annotation}
            self._tools[cat]['[tools]'].append(title) #to simulate an OrderedDict
    
    def addTool(self, title, command, image, sourceType='mel', annotation=''):
        """Add a tool to the current category
        sourceType is the script type (mel/python)"""
        self.addToolToCat(self._curCat, title, command, image, sourceType, annotation)
    
    def addPyTool(self, title, command, image, annotation=''):
        """Adds a python tool to the current category"""
        self.addTool(title, command, image, 'python', annotation)
    
    def addMelTool(self, title, command, image, annotation=''):
        """Adds a mel tool to the current category"""
        self.addTool(title, command, image, 'mel', annotation)
    
    def clearAllTools(self, clearCats=True):
        """Clear all tools and categories."""
        if clearCats:
            #remove all categories and tools
            self._initTools()
        else:
            #clear all tools but keep the categories
            for key in self._tools.keys():
                self._tools[key]['[tools]'] = []
    
    
    #GUI Creation
    def createMenu(self):
        """Create the Dillo Tools menu"""
        import dilloTools.menu
        evalDeferred( Callback(dilloTools.menu.createMenu, self._tools) )
    
    def createWindow(self):
        """Create an instance of the DilloToolsWindow class and call create() on it.
        Then add all categories and tools to the window."""
        import dilloTools.window
        dilloTools.window.createWindow(self._tools)   
    
    def createShelf(self):
        """Create the DilloTools shelf if it does not exist,
        Then clear/rebuild all shelf items. Prompt if clearing."""
        import dilloTools.shelf
        dilloTools.shelf.createShelf(self._tools)
        
    def deleteShelf(self):
        """Create the DilloTools shelf if it does not exist,
        Then clear/rebuild all shelf items. Prompt if clearing."""
        import dilloTools.shelf
        dilloTools.shelf.deleteShelf()
    
    def checkShelfColors(self):
        """Update the DilloTools shelf button colors, since
        Maya always forgets them."""
        import dilloTools.shelf
        evalDeferred( Callback(dilloTools.shelf.checkShelfColors, self._tools) )



