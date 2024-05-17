import Constant
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class MyApp(QMainWindow):

  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.statusBar().showMessage('initUI')

    self.setWindowTitle(f'{Constant.PROGRAM_NAME}')
    self.setWindowIcon(QIcon(f'{Constant.RESOURCE_PATH}icon.jpg'))
    
    self.CreateMenuBar()
    self.show()

#region 메뉴 바

  def CreateMenuBar(self):
    menubar = self.menuBar()
    menubar.setNativeMenuBar(False)
    self.CreateMenuBar_File(menubar)
    self.CreateMenuBar_Help(menubar)
  
  #region Menubar -> File
  
  def CreateMenuBar_File(self,menubar:QMenuBar):
    filemenu = menubar.addMenu('&File')
    #종료
    self.exitAction = QAction(QIcon('exit.png'), 'Exit', self)
    self.exitAction.setShortcut('Alt+Q')
    self.exitAction.setStatusTip('Exit application')
    self.exitAction.triggered.connect(qApp.quit)
    filemenu.addAction(self.exitAction)
  
  #endregion

  #region Menubar -> Help
  
  def CreateMenuBar_Help(self,menubar:QMenuBar):  
    helpmenu = menubar.addMenu('&Help')
    self.helpAction = QAction(QIcon('About.png'), 'About', self)
    self.helpAction.setShortcut('Alt+H')
    self.helpAction.setStatusTip('About Program')
    self.helpAction.triggered.connect(self.ShowAboutMessageBox)
    helpmenu.addAction(self.helpAction)
  # About 기능
  def ShowAboutMessageBox(self):
    message:str = ""
    message += f"Version {Constant.PROGRAM_VERSION}\n"
    message += f"made by {Constant.MADE_BY}\n"

    QMessageBox.about(self,f'About {Constant.PROGRAM_NAME}', message)
  
  #endregion

#endregion


if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = MyApp()
  sys.exit(app.exec_())