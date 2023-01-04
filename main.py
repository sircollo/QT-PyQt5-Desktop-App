import sys
import os
from PySide2 import *
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizeGrip, QShortcut, QPushButton
# Import QT Material
from qt_material import *
from ui_interface import *
from PyQt5.QtGui import QKeySequence
import psutil
import PySide2extn
from PySide2extn.RoundProgressBar import roundProgressBar
from PySide2extn.SpiralProgressBar import spiralProgressBar
import time
import datetime
from multiprocessing import cpu_count
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
		self.battery()
		self.cpu_ram()
		self.system_info()
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
   
   	# Fuction to convert seconds to hours
	def secs2hours(self, seconds):
		minutes, seconds = divmod(seconds, 60)
		hours, minutes = divmod(minutes, 60)
		return "%d:%02d:%02d (H:M:S)" % (hours, minutes, seconds)
	#####################################################
	## Get System battery Information
	#####################################################
	def battery(self):
		batt = psutil.sensors_battery()
		# print("Battery percentage : ", batt.percent)

		if not hasattr(psutil, "sensors_battery"):
			self.ui.battery_status.setText("Platform not supported")
		if batt is None:
			self.ui.battery_status.setText("No battery Installed")
		if batt.power_plugged:
			self.ui.battery_charge.setText(str(round(batt.percent, 2))+"%")
			self.ui.battery_time_left.setText("N/A")

			if batt.percent < 100:
				self.ui.battery_status.setText("Charging")
			else:
				self.ui.battery_status.setText("Fully Charged")

			self.ui.battery_plugged.setText("Yes")

		else:
			self.ui.battery_charge.setText(str(round(batt.percent, 2))+"%")
			self.ui.battery_time_left.setText(self.secs2hours(batt.secsleft))

			if batt.percent < 100:
				self.ui.battery_status.setText("Discharging")
			else:
				self.ui.battery_status.setText("Fully Charged")
			self.ui.battery_plugged.setText("No")
   
	# Get CPU and RAM information
	def cpu_ram(self):
		# total ram
		totalRam = 1.0
		totalRam = psutil.virtual_memory()[0] * totalRam
		totalRam = totalRam / (1024 * 1024 * 1024)
		self.ui.total_ram.setText(str("{: .2f}".format(totalRam) + ' GB'))

		# availbale ram
		available_ram = 1.0
		available_ram = psutil.virtual_memory()[1] * available_ram
		available_ram = available_ram / (1024 * 1024 * 1024)
		self.ui.available_ram.setText(str("{: .2f}".format(available_ram) + ' GB'))

		# used RAM
		used_ram = 1.0
		used_ram = psutil.virtual_memory()[3] * used_ram
		used_ram = used_ram / (1024 * 1024 * 1024)
		self.ui.used_ram.setText(str("{: .2f}".format(used_ram) + ' GB'))
  
		# free RAM
		free_ram = 1.0
		free_ram = psutil.virtual_memory()[4] * free_ram
		free_ram = free_ram / (1024 * 1024 * 1024)
		self.ui.free_ram.setText(str("{: .2f}".format(free_ram) + ' GB'))
  
		# RAM Useage
		ram_usage = str(psutil.virtual_memory()[2]) + ' %'
		self.ui.ram_usage.setText(str("{}".format(ram_usage)))

		# Number of processors
		core = cpu_count()
		self.ui.cpu_count.setText(str(core))
  
		# CPU Percentage
		cpu_per = psutil.cpu_percent()
		self.ui.cpu_per.setText(str(cpu_per) + " %")
  
		# CPU Main COre
		cpu_main_core = psutil.cpu_count(logical=False)
		self.ui.cpu_main_core.setText(str(cpu_main_core))
  
	# Get System information
	def system_info(self):
		time = datetime.datetime.now().strftime("%I:%M:%S %p")
		self.ui.system_time.setText(str(time))
		date = datetime.datetime.now().strftime("%Y-%m-%d")
		self.ui.system_date.setText(str(date))
		QtCore.QTimer.singleShot(1000, self.system_info)
  
## Execute App
if __name__=="__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	# window.showMaximized()
	sys.exit(app.exec_())