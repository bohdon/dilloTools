"""
Dillo Tools - menu
"""


import dilloTools
from pymel.core import *


LOG = dilloTools.getLog('menu')


__MENU_NAME__ = 'dilloToolsMenu'

def createMenu(tools, p=None):
    """Create and populate the Dillo Tools menu.
    This menu can be created in alternate locations by
    passing a menu or window to the p parameter"""
    LOG.debug('Building...')
    if p is None:
        p = melGlobals['gMainWindow']
    
    setParent(p)
    longName = '{0}|{1}'.format(p, __MENU_NAME__)
    if menu(longName, ex=True):
        deleteUI(__MENU_NAME__)
    
    with menu(__MENU_NAME__, l='Dillo Tools', p=p, to=True):
        createMenuTools(tools)
        createGuiShortcuts()
        menuItem(d=True)
        menuItem(l='v{0}'.format(dilloTools.getVersion()), en=False)


def createMenuTools(tools):
    for cat in tools['[cats]']:
        LOG.debug('submenu: {0}'.format(cat))
        with menuItem(l=cat, subMenu=True, to=True):
            for tool in tools[cat]['[tools]']:
                toolData = tools[cat][tool]
                stp = toolData['sourceType']
                itemKargs = {
                    'ann':toolData['annotation'],
                    'c':toolData['command'],
                    'i':toolData['image'],
                    'l':tool,
                }
                LOG.debug('tool: {0}'.format(tool))
                dilloMenuItem(stp, itemKargs)


def dilloMenuItem(stp, itemKargs):
    """Create a menu item using mel or python depending on stp."""
    if stp == 'python':
        menuItem(**itemKargs)
    elif stp == 'mel':
        mel.menuItem(**itemKargs)


def createGuiShortcuts():
    menuItem(d=True)
    menuItem(l='Window', c=Callback(dilloTools.createWindow))
    with menuItem(l='Shelf', sm=True):
        menuItem(l='Build', c=Callback(dilloTools.createShelf))
        menuItem(l='Delete', c=Callback(dilloTools.deleteShelf))
