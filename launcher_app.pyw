# v.0.0.1 wip

#Import python modules
import sys
import os 
import json 
import logging
import env_config 
import tool_path

moduleDir = os.path.dirname(sys.modules[__name__].__file__)
appName = os.path.splitext(os.path.basename(sys.modules[__name__].__file__))[0]
# read config environment 
env = env_config.read()

# initial env setup 
RFSCRIPT_VAR = env.get('SCRIPT_VAR')
RFSCRIPT = os.environ.get(RFSCRIPT_VAR)
print 'RFSCRIPT', RFSCRIPT
tool_path.add(RFSCRIPT)

try: 
    import maya.cmds as mc 
    import maya.mel as mm 
    import maya.OpenMayaUI as mui
    isMaya = True 
except ImportError: 
    isMaya = False

from utils import log_utils
from utils import load

logFile = log_utils.name(appName, user='TA')
logger = log_utils.init_logger(logFile)
logger.setLevel(logging.INFO)

os.environ['QT_PREFERRED_BINDING'] = os.pathsep.join(['PySide', 'PySide2'])
from Qt import wrapInstance
from Qt import QtCore
from Qt import QtWidgets
from Qt import QtGui


# If inside Maya open Maya GUI
def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtWidgets.QWidget)

logger.info('\n\n==============================================')



class RFLauncher(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        #Setup Window
        super(RFLauncher, self).__init__(parent)

        # ui read
        uiFile = '%s/ui.ui' % moduleDir

        if isMaya: 
            self.ui = load.setup_ui_maya(uiFile, self)
        else: 
            self.ui = load.setup_ui(uiFile, self)
        self.ui.show()
        self.ui.setWindowTitle('Riff Desktop')


def show():
    if isMaya:
        logger.info('Run in Maya\n')
        uiName = 'RFLauncher'
        deleteUI(uiName)
        myApp = RFLauncher(getMayaWindow())
        # myApp.show()
        return myApp

    else:
        logger.info('Run in standalone\n')
        app = QtWidgets.QApplication.instance()
        if not app: 
            app = QtWidgets.QApplication(sys.argv)
        myApp = RFLauncher()
        # myApp.show()
        if os.path.exists('%s/styleSheet/darkorange.css' % moduleDir) :
            try:
                app.setStyle('plastique')

                data = open('%s/styleSheet/darkorange.css' % moduleDir,'r').read()
                app.setStyleSheet(data+'QLabel { color : white; }')

            except Exception as e:
                logger.info(str(e))

        sys.exit(app.exec_())

def deleteUI(ui):
    if mc.window(ui, exists=True):
        mc.deleteUI(ui)
        deleteUI(ui)

if __name__ == '__main__': 
    show()
