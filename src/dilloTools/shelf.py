"""
Dillo Tools - shelf
"""


import dilloTools
import logging
from pymel.core import *


LOG = logging.getLogger('dilloTools')


__SHELF_NAME__ = 'DilloTools'
__USEBGC__ = False

def createShelf(tools):
    """Create the DilloTools shelf. If it
    already exists, it will be recreated, but the
    user will be prompted as all custom shelf buttons
    will be removed."""
    dilloShelf = __SHELF_NAME__
    if shelfExists(dilloShelf):
        if not dilloClearWarningDialog():
            LOG.info('Rebuild cancelled by user')
            return
    clearShelfTab(dilloShelf, create=True)
    createShelfTools(dilloShelf, tools)
    selectShelf(dilloShelf)

def createShelfTools(shelfName, tools):
    for cat in tools['[cats]']:
        catColor = tools[cat]['[color]']
        shelfButton(l='{0} Separator'.format(cat), p=shelfName, i=os.path.join(dilloTools.__IMAGES_DIR__, 'separator.png'))
        LOG.debug('category: {0}, color: {1}'.format(cat, catColor))
        for tool in tools[cat]['[tools]']:
            toolData = tools[cat][tool]
            ann = getNameAndAnnotation(tool, toolData['annotation'])
            btnKargs = {
                'ann':ann,
                'c':toolData['command'],
                'i':toolData['image'],
                'l':tool,
                'stp':toolData['sourceType'],
                'p':shelfName,
            }
            if __USEBGC__:
                btnKargs['bgc'] = catColor
            LOG.debug('tool: {0}'.format(tool))
            shelfButton(**btnKargs)


def dilloClearWarningDialog():
    kargs = {
        't':'Rebuilding DilloTools Shelf',
        'm':'''The Dillo Tools shelf will be cleared and rebuilt,
if you have any custom buttons, please move them to
a custom shelf before rebuilding, or they will be lost.''',
        'icn':'warning',
        'b':['Clear and Rebuild', 'Cancel'],
        'cb':'Cancel',
        'ma':'center',
    }
    result = confirmDialog(**kargs)
    if result == 'Clear and Rebuild':
        return True
    else:
        return False

def deleteShelf():
    """Delete the DilloTools shelf"""
    deleteShelfTab(__SHELF_NAME__)


def checkShelfColors(tools):
    """A lame glitch in Maya causes shelf button background colors to be forgotten,
    This function sets the colors of all known buttons every time Maya is started"""
    if not __USEBGC__:
        return
    dilloShelf = __SHELF_NAME__
    curShelf = getCurrentShelf()
    if curShelf is None:
        return
    if shelfExists(dilloShelf):
        selectShelf(dilloShelf)
        LOG.debug('checking background colors')
        shelf = getShelfLayout(dilloShelf)
        
        children = shelfLayout(shelf, q=True, ca=True)
        if not children is None:
            childDict = {}
            for child in children:
                childFull = '{0}|{1}'.format(shelf, child)
                childLabel = shelfButton(childFull, q=True, l=True)
                childDict[childLabel] = childFull
            
            for cat in tools['[cats]']:
                catColor = tools[cat]['[color]']
                for tool in tools[cat]['[tools]']:
                    if tool in childDict:
                        shelfButton(childDict[tool], e=True, bgc=catColor)
        selectShelf(curShelf)


#All the following functions are utils, not DilloTools specific\
def clearShelfTab(shelfName, create=False):
    """Clear all itmes in a shelf."""
    shelf = None
    if create:
        shelf = createShelfTab(shelfName)
    elif shelfExists(shelfName):
        shelf = getShelfLayout(shelfName)
    else:
        return None
    
    children = shelfLayout(shelf, q=True, ca=True)
    if not children is None:
        for child in children:
            deleteUI(child)
            LOG.debug('{0} has been cleared'.format(shelfName))
    return shelf



def createShelfTab(shelfName):
    """Create a new shelf"""
    if not shelfExists(shelfName):
        mel.addNewShelfTab(shelfName)
        LOG.debug('{0} has been created'.format(shelfName))
    return getShelfLayout(shelfName)

def deleteShelfTab(shelfName):
    """Delete a shelf"""
    if shelfExists(shelfName):
        mel.deleteShelfTab(shelfName)
        LOG.debug('{0} has been deleted'.format(shelfName))



def deleteShelfButton(title):
    """Delete a shelf button by label"""
    LOG.debug('deleteShelfButton: this function is not yet implemented')




def shelfExists(shelfName):
    """Return whether or not a shelf exists."""
    result = False
    
    mainShelf = getMainShelf()
    if mainShelf is None:
        return False
    
    tabs = shelfTabLayout(mainShelf, q=True, ca=True)
    if not tabs is None:
        result = (shelfName in tabs)
    
    return result


def selectShelf(shelfName):
    """Make a shelf the active shelf."""
    if shelfExists(shelfName):
        mainShelf = getMainShelf()
        shelfTabLayout(mainShelf, e=True, st=shelfName)



def getMainShelf():
    """Return the full path to the main shelfTabLayout in Maya"""
    mainShelf = melGlobals['gShelfTopLevel']
    if shelfTabLayout(mainShelf, ex=True):
        return mainShelf
    else:
        return None

def getCurrentShelf():
    """Return the name of the current shelf tab"""
    mainShelf = getMainShelf()
    if mainShelf is None:
        return None
    curShelf = shelfTabLayout(mainShelf, q=True, st=True)
    return curShelf

def getShelfLayout(shelfName):
    """Return the full path to the layout of a shelf"""
    if shelfExists(shelfName):
        shelf = '{0}|{1}'.format(getMainShelf(), shelfName)
        return shelf
    else:
        return None

def getNameAndAnnotation(toolName, annotation):
    if annotation == '':
        return toolName
    else:
        return '{0}: {1}'.format(toolName, annotation)


