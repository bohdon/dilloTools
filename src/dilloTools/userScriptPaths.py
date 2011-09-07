

import sys, os

def add(paths):
    """Add paths to both python and mel source paths"""
    #get maya path
    mPath = os.environ['MAYA_SCRIPT_PATH'].split(';')
    addListPy = []
    addListMel = []
    for path in paths:
        if path not in sys.path:
            sys.path.append(path)
            addListPy.append(path)
        if path not in mPath:
            mPath.append(path)
            addListMel.append(path)
    #set maya path
    os.environ['MAYA_SCRIPT_PATH'] = ';'.join(mPath)
    #print results
    if addListPy != []:
        print 'Added python script paths...'
        for path in addListPy:
            print '    {0:<60}{1}'.format( path.ljust(60, '.'), (os.path.exists(path) and '(found)' or '(not found)'))
    if addListMel != []:
        print 'Added mel script paths...'
        for path in addListMel:
            print '    {0:<60}{1}'.format( path.ljust(60, '.'), (os.path.exists(path) and '(found)' or '(not found)'))
