

__version__ = '0.5'

import sys, os


def addScript(paths, melenv='MAYA_SCRIPT_PATH', insert=False):
    """Add paths to both python and mel source paths"""
    if not isinstance(paths, list):
        paths = [paths]
    
    # replace \ with /
    paths = [x.replace('\\', '/') for x in paths]
    
    # add to mel
    melResults = addToEnv(melenv, paths, insert)
    
    # add to python
    pyResults = []
    for path in paths:
        if path not in sys.path:
            if insert:
                sys.path.insert(0, path)
            else:
                sys.path.append(path)
            pyResults.append(path)
    
    printPathResults(pyResults, 'Added Python Paths...')
    printPathResults(melResults, 'Added MEL Paths...')
    return pyResults, melResults


def addPlugin(paths, env='MAYA_PLUG_IN_PATH', insert=False):
    """Add paths to maya's plugin path"""
    if not isinstance(paths, list):
        paths = [paths]
    
    # replace \ with /
    paths = [x.replace('\\', '/') for x in paths]
    
    results = addToEnv(env, paths, insert)
    printPathResults(results, 'Added Maya Plugin Paths...')
    return results


def addToEnv(env, paths, insert=False):
    """Split a semi-colon-separated env variable,
    append or insert the specified paths,
    then reassign the new values to the env variable"""
    results = None
    if os.environ.has_key(env):
        envpaths = os.environ[env].split(os.pathsep)
        results = []
        for path in paths:
            if path not in envpaths:
                if insert:
                    envpaths.insert(0, path)
                else:
                    envpaths.append(path)
                results.append(path)
        os.environ[env] = os.pathsep.join(envpaths)
    return results


def printPathResults(paths, msg):
    if paths is not None:
        if paths != []:
            print msg
            for path in paths:
                print '    {0:.<60}{1}'.format( path, (os.path.exists(path) and '(found)' or '(not found)') )


