"""
    Dillo Tools
    
    Copyright (C) 2011 Ringling College
    All Rights Reserved.
    bsayre@c.ringling.edu
    
    See licenses of individual tools for more usage and copyright information.
    
    See the README or Dillo Tools Wiki for more information.
    https://github.com/bohdon/dilloTools/wiki
    
    For Developers:
        The only necessity for scripts within dilloTools is to
        use the dillo_getImage global procedure to acquire
        proper image locations.
"""

from dilloTools import userPaths, tools
from pymel.core import mel
import logging
import os

__version__ = '3.1'
__author__ = 'Bohdon Sayre'

DILLO_DIR = os.path.normpath(os.path.dirname(__file__))
IMAGES_DIR = os.path.normpath(os.path.join(DILLO_DIR, 'images'))
SCRIPTS_DIR = os.path.normpath(os.path.join(DILLO_DIR, 'scripts')).replace('\\', '/')
PLUGIN_DIR = os.path.normpath(os.path.join(DILLO_DIR, 'plugins')).replace('\\', '/')

log = logging.getLogger('dilloTools')
log.setLevel(logging.INFO)


def init():
    """Instance Dillo Tools and build the Dillo Tools menu.
    Also ensure that the shelf background colors are correct (Maya dropped the ball)"""
    dillo = getInstance()
    tools.addAllTools(dillo)
    dillo.createMenu()
    dillo.checkShelfColors()

def reinit():
    from dilloTools import core
    core.DilloTools.delInstance()
    init()

def getInstance():
    """Return the instance of DilloTools"""
    from dilloTools import core
    return core.DilloTools.getInstance()

def getTools():
    """Return the current tool data"""
    return getInstance().getTools()

def getDilloImage(image):
    """Return the full path to a dillo tools image"""
    fullImage = os.path.normpath(os.path.join(IMAGES_DIR, image))
    return fullImage

def getVersion():
    return __version__

def createWindow():
    getInstance().createWindow()

def createShelf():
    getInstance().createShelf()

def deleteShelf():
    getInstance().deleteShelf()


#extension of userSetup, dilloTools must be imported during maya startup
userPaths.addScript(SCRIPTS_DIR)
userPaths.addPlugin(PLUGIN_DIR)
mel.eval("source boRightClickManager")


