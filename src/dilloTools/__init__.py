"""
    Dillo Tools
    3.0
    
    Copyright (C) 2010 Bohdon Sayre and Keith Osborn
    All Rights Reserved.
    bsayre@c.ringling.edu
    kosborn@c.ringling.edu
    
    Description:
        The Ringling College of Art and Design toolset.
    
    Version 3.0:
        > Access Dillo Tools Window from a main menu in the Maya Window
        > Build window or shelf version easily
        > Easily add Mel and Python tools
        > Easily add and change tool categories
    
    Instructions:
        >>> import dilloTools
        >>> dilloTools.doIt()
    
    For Developers:
        The only necessity for scripts within dilloTools is to
        use the dilloTools_getImage global procedure to acquire
        proper image locations.
"""


import logging, os
import dilloTools.userScriptPaths
import dilloTools.tools as tools
from pymel.core import mel


__DILLO_DIR__ = os.path.normpath(os.path.dirname(__file__))
__IMAGES_DIR__ = os.path.normpath(os.path.join(__DILLO_DIR__, 'images'))
__SCRIPTS_DIR__ = os.path.normpath(os.path.join(__DILLO_DIR__, 'scripts')).replace('\\', '/')
__PLUGIN_DIR__ = os.path.normpath(os.path.join(__DILLO_DIR__, 'plugins')).replace('\\', '/')
__LOG_LEVEL__ = logging.INFO
__VERSION__ = (3, 0, 34)
__MAIN_VERSION__ = '.'.join([ str(__VERSION__[0]), str(__VERSION__[1]) ])
__version__ = '.'.join([str(n) for n in __VERSION__])
__author__ = 'Bohdon Sayre'

def getLog(name):
    fullName = '{0} : {1}'.format('Dillo Tools', name)
    log = logging.getLogger(fullName)
    log.setLevel(__LOG_LEVEL__)
    return log


def init():
    """Instance Dillo Tools and build the Dillo Tools menu.
    Also ensure that the shelf background colors are correct (Maya dropped the ball)"""
    dillo = getInstance()
    tools.addAllTools(dillo)
    dillo.createMenu()
    dillo.checkShelfColors()

def reinit():
    import dilloTools.core as core
    core.DilloTools.delInstance()
    init()

def getInstance():
    """Return the instance of DilloTools"""
    import dilloTools.core as core
    return core.DilloTools.getInstance()

def getTools():
    """Return the current tool data"""
    return getInstance().getTools()

def getDilloImage(image):
    """Return the full path to a dillo tools image"""
    fullImage = os.path.normpath(os.path.join(__IMAGES_DIR__, image))
    return fullImage

def getDilloDir():
    return __DILLO_DIR__

def getVersion():
    return __version__

def getMainVersion():
    return __MAIN_VERSION__

def createWindow():
    getInstance().createWindow()

def createShelf():
    getInstance().createShelf()

def deleteShelf():
    getInstance().deleteShelf()


#extension of userSetup, dilloTools must be imported during maya startup
dilloTools.userScriptPaths.add([__SCRIPTS_DIR__])
if os.environ.has_key('MAYA_PLUG_IN_PATH'):
        os.environ['MAYA_PLUG_IN_PATH'] += ';{0}'.format(__PLUGIN_DIR__)
mel.eval("source boRightClickManager")


