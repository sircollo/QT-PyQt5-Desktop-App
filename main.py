import sys
import os
from PySide2 import *
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizeGrip, QShortcut
# Import QT Material
from qt_material import *
from ui_interface import *
from PyQt5.QtGui import QKeySequence

## Main Window Class
class MainWindow(QMainWindow):
	"""docstring for MainWindow"""
	def __init__(self):
		QMainWindow.__init__(self)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		
		quit_shortcut = QShortcut(QKeySequence("*"), self)
		quit_shortcut.activated.connect(self.close)
		# # Load local stylesheet
		apply_stylesheet(app, theme='dark_cyan.xml')

		# # Remove window title bar
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

		# # # Shadow Effect Style
		# self.shadow = QGraphicsDropShadowEffect(self)
		# self.shadow.setBlurRadius(50)
		# self.shadow.setXOffset(0)
		# self.shadow.setYOffset(0)
		# self.shadow.setColor((QColor(0, 92, 157, 550)))

		# self.ui.centralwidget.setGraphicsEffect(self.shadow)
		## Window icon
		# self.setWindowIcon(QIcon(""))
		## Window title
		self.setWindowTitle("Util Manager")
  
		## Window Size grip to resize window
		QSizeGrip(self.ui.size_grip)
  
		# # Navigation Bar Click Events
		# Minimize Window
		self.ui.minimize_window_button.clicked.connect(lambda: self.showMinimized())
  		# Maximize Window
		self.ui.maximize_window_button.clicked.connect(lambda: self.showMaximized())
		# Close Window
		self.ui.close_window_button.clicked.connect(lambda: self.close())
  
		## Stacked Pages Navigation
		#cpu and memory page
		self.ui.cpu_page_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.cpu_and_memory))
		# Battery
		self.ui.battery_page_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.battery))
		# System info 
		self.ui.system_inf_page_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.system_info))
		# Activities
		self.ui.activity_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.activities))
		# Storage
		self.ui.storage_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.storage))
		# Sensors
		self.ui.sensors_page_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.sensors))
		# Networks
		self.ui.networks_page_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.networks))
  
  		## Function to drag window on mouse event on title bar
		def moveWindow(e):
			# detect if window is normal size
			if self.isMaximized() == False:
				# window is normal size and accept only left mouse
				if e.buttons() == Qt.LeftButton:
					self.move(self.pos() + e.globalpPos() - self.clickPosition)
					self.clickPostion = e.globalPos()
					e.accept()
		# Add mouseEvent to top header to move the window
		self.ui.header_frame.mouseMoveEvent = moveWindow
		self.ui.open_close_side_bar_btn.clicked.connect(lambda: self.slideLeftMenu())
		self.show()
	## Slide Left menu function
	def slideLeftMenu(self):
		width = self.ui.left_menu_cont_frame.width()
		if width ==40:
			newWidth = 200
		else:
			newWidth = 40
		# Animate the transition
		self.animation = QPropertyAnimation(self.ui.left_menu_cont_frame, b"minimumWidth") #Animate minimumWidth
		self.animation.setDuration(250)
		self.animation.setStartValue(width)
		self.animation.setEndValue(newWidth)
		self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
		self.animation.start()

	## Add mouse events to the window
	def mousePressEvent(self, event):
		self.clickPostion = event.globalPos()
  
	## Update button icon on minimizing or maximizing window
	def restore_or_maximize_window(self):
		if self.isMaximized():
			self.showNormal()
			self.ui.maximize_window_button.setIcon()
		else:
			self.showMaximized()
			self.ui.maximize_window_button.setIcon()
		



## Execute App
if __name__=="__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	# window.showMaximized()
	sys.exit(app.exec_())