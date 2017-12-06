# pyside package 
import sys
import os 
import env_config 
env = env_config.read()

def add(root): 
    packagePath = '%s/%s' % (root, env.get('PACKAGE'))
    qtPath = '%s/%s' % (root, env.get('QTPATH'))
    toolPath = '%s/%s' % (root, env.get('TOOLPATH'))

    appendPaths = [packagePath, qtPath, toolPath]

    # add PySide lib path
    for path in appendPaths:
        if not path in sys.path:
            sys.path.append(path)
