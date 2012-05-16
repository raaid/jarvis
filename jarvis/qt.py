import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt
import os.path
import codecs
import osgqt
import osgDB
import osg
import shutil

class MyTextEdit(QtGui.QTextEdit):
    def __init__(self, text, father):
        super(MyTextEdit, self).__init__(text, father)
#    def keyPressEvent(self, event):
#        print event
    
class JarvisMain(QtGui.QWidget):
    
    def __init__(self):
        self.osg_enable = True
        super(JarvisMain, self).__init__()
        
        self.initUI()

    def display(self):
        print self.editor.toPlainText()

#    def wheelEvent(self, event):
#        print self.editor.setFocus(False)

#    def keyPressEvent(self, event):
#         print event

    def createEditor(self, text, width, height):
        editor = MyTextEdit(text, self)
        editor.setMinimumWidth(width)
        editor.setMinimumHeight(height)
        return editor

    def createOSG(self, width, height):        
        osgWidget = osgqt.PyQtOSGWidget(self)
        osgWidget.setMinimumWidth(width)
        osgWidget.setMinimumHeight(height)
        return osgWidget
                
    def initUI(self):        
        self.setWindowTitle('Icon')
        WIDTH=480
        HEIGHT=1024
        self.setGeometry(1440 - WIDTH, 0, WIDTH, 1024)
#        self.setWindowIcon(QtGui.QIcon('web.png'))

        text = ""
#        for i in range(10):
#            text += '<b>Text%d</b><br/>' % i

        self.topBox = QtGui.QHBoxLayout(self)
        self.topBox.setContentsMargins(0,0,0,0)
        self.topBox.setSpacing(0)
        self.topBox.setGeometry(QtCore.QRect(0, 0, WIDTH, HEIGHT))
  
#        self.editor = self.createEditor(text, 300, 600)
#        self.editor.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
#        self.topBox.addWidget(self.editor)

        self.rightBox = QtGui.QVBoxLayout()
        self.rightBox.setSpacing(0)
        self.topBox.addLayout(self.rightBox)

        self.error = self.createEditor("", WIDTH, 300)
        self.debug = self.createEditor("", WIDTH, 300)
        if self.osg_enable:
            self.osgView = self.createOSG(WIDTH, int(WIDTH * 9 / 16.0))

        self.rightBox.addWidget(self.error, 0, Qt.AlignRight)
        self.rightBox.addWidget(self.debug, 0, Qt.AlignRight)
        if self.osg_enable:
            self.rightBox.addWidget(self.osgView, 0, Qt.AlignRight)

#        editor.textChanged.connect(self.display)
#        editor.wheelEvent.connect(self.wheelEvent)
#        self.editor.setFocus()
        self.filename = None
        self.show()

    def atomic_write(self, filename, text):
        f = open(filename + ".tmp", "w")
        f.write(text)
        f.close()
        shutil.move(filename + ".tmp", filename)        

    def debug_text(self, text):
#        print "DEBUG TEXT", text
        if text == None:
            text = ""
            self.debug.clear()
        else:            
            self.debug.append(text)
            text = self.debug.toPlainText()

        self.atomic_write("/tmp/debug.txt", text)
        

    def error_text(self, text):
#        print "ERROR TEXT", text
        if text == None:
            text = ""
            self.error.clear()
        else:            
            self.error.append(text)
            text = self.error.toPlainText()

        self.atomic_write("/tmp/error.txt", text)

        self.error.setText(text)

    def setSceneData(self, data):
        self.osgView.setSceneData(data)

    def setLoopTime(self, loopTime):
        self.osgView.setLoopTime(loopTime)

    def get_osg_viewer(self):
        return self.osgView.get_osg_viewer()

    def file_dialog(self):
        fd = QtGui.QFileDialog(self)
        filename = fd.getOpenFileName()
        if os.path.isfile(filename):
            text = open(filename).read()
            self.editor.setText(text)
            self.filename = filename

            s = codecs.open(self.filename,'w','utf-8')
            s.write(unicode(self.ui.editor_window.toPlainText()))
            s.close()

    def run_command(self):
        self.fun()




def main():    
    app = QtGui.QApplication(sys.argv)
    
    ex = JarvisMain()
#    ex.raise_()


    # create a root node
    node = osg.Group()
    # open a file
    loadedmodel = osgDB.readNodeFile("/Users/lagunas/tmp/osgIphoneExampleGLES2/cow.osg")
    node.addChild(loadedmodel)
    
    ex.osgView.viewer.setSceneData(node)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()    
