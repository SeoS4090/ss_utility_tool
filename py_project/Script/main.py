import Constant
import sys
import WinAlarm
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import WinEvt
import datetime

class MyApp(QMainWindow):

  def __init__(self):
    super().__init__()
    self.LoadDatas()
    self.initUI()
    

  def initUI(self):
    self.statusBar().showMessage('initUI')
    self.setWindowTitle(f'{Constant.PROGRAM_NAME}')
    self.setWindowIcon(QIcon(f'{Constant.RESOURCE_PATH}icon.jpg'))
    
    self.CreateMenuBar()
    
    tabs = QTabWidget()
    tabs.addTab(self.CreateContents_Calandar(), '출석부')
    tabs.addTab( QWidget(), '텀 확인')

    tab_widget = QWidget()
    self.setCentralWidget(tab_widget)
    vbox = QHBoxLayout()
    vbox.addWidget(tabs)
    tab_widget.setLayout(vbox)
    
    self.setGeometry(300, 300, 300, 200)
    self.show()
    self.statusBar().showMessage('')

#region Data Load

  def LoadDatas(self):
    self.statusBar().showMessage('Data Loading...')
    self.logonEvent = WinEvt.GetEvent("Security",WinEvt.LOGON_QUERY)
    self.systemOffEvent = WinEvt.GetEvent("System",WinEvt.SYSTEM_OFF_QUERY)
    

#endregion

#region 메뉴 바

  def CreateMenuBar(self):
    self.statusBar().showMessage('Create Menu Bar')

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

#region Contents

  def CreateContents_Calandar(self):
    frame = QFrame()
    hbox = QHBoxLayout()

    cal = QCalendarWidget()
    cal.setGridVisible(True)
    cal.showToday()
    
    hbox.addWidget(cal)

    #---------------------------------------#
    vbox = QVBoxLayout()
    gr_data = QGroupBox()
    gr_data_v = QGridLayout()

    gr_data.setLayout(gr_data_v)
    vbox.addWidget(gr_data)

    selected_date = QLabel(self)
    selected_date.setAlignment(Qt.AlignCenter)
    selected_date.setText(cal.selectedDate().toString('yyyy-MM-dd'))

    
    LogOnTime = QTimeEdit(self)
    LogOnTime.setDisplayFormat('hh:mm:ss')
    
    cal.selectionChanged.connect(lambda: self.showDate(selected_date,LogOnTime,cal))
    gr_data_v.addWidget(selected_date , 0,1)
    
    label_logonTime = QLabel("OnTime")
    label_logonTime.setAlignment(Qt.AlignCenter)

    gr_data_v.addWidget(label_logonTime,1,0)
    gr_data_v.addWidget(LogOnTime,1,1)

    label_work_time = QLabel("업무 시간")
    work_time = QTimeEdit()
    work_time.setTime(QTime(9,0,0))
    work_time.setDisplayFormat('hh:mm')

    gr_data_v.addWidget(label_work_time,2,0)
    gr_data_v.addWidget(work_time,2,1)
    

    #---------------------------------------#
    btn_Today = QPushButton("오늘")
    btn_Today.clicked.connect(lambda: cal.setSelectedDate(QDate.currentDate()))

    gr_func_v = QVBoxLayout()
    gr_func_v.addWidget(btn_Today)

    gr_func = QGroupBox()
    gr_func.setLayout(gr_func_v)

    vbox.addWidget(gr_func)
    vbox.addStretch(1)
    
    hbox.addSpacing(20)
    hbox.addLayout(vbox)
    frame.setLayout(hbox)

    self.showDate(selected_date,LogOnTime,cal)
    return frame
  
  def showDate(self, label:QLabel,time:QTimeEdit, cal:QCalendarWidget):
    date = cal.selectedDate().toString('yyyy-MM-dd')
    label.setText(date)
    
    #print(f"{date} | {QDateTime.currentDateTime().toString('yyyy-MM-dd')} : {QDateTime.currentDateTime().toString('yyyy-MM-dd') == date}")
    time.setEnabled(True)
    if date in self.logonEvent:
      qtime = QTime.fromString(self.logonEvent[date].strftime('%H:%M:%S'))
      time.setTime(qtime)
      if(QDateTime.currentDateTime().toString('yyyy-MM-dd') == date):
        WinAlarm.Show_Toast()

    elif QDateTime.currentDateTime().toString('yyyy-MM-dd') == date:
      time.setTime(QTime.currentTime())
      self.logonEvent[date] = datetime.datetime.strptime(QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss'),Constant.TIME_OUTPUT_FORMAT)
    else:
      time.setEnabled(False)
      print('NOT FOUNDED')

#endregion

if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = MyApp()
  sys.exit(app.exec_())