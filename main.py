import sys
import os
from PySide2 import *
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizeGrip, QShortcut, QPushButton, QTableWidgetItem, QProgressBar
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
import shutil
from multiprocessing import cpu_count
import platform
# Global
platforms = {
	'linux': 'Linux',
	'linux1': 'Linux',
	'linux2': 'Linux',
	'darwin': 'OS X',
	'win32': 'Windows'
}
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
		self.processes()
		self.storage()
		self.sensors()
		self.networks()
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
		QtCore.QTimer.singleShot(5000, self.battery)
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
		QtCore.QTimer.singleShot(5000, self.cpu_ram)
  
	# Get System information
	def system_info(self):
		time = datetime.datetime.now().strftime("%I:%M:%S %p")
		self.ui.system_time.setText(str(time))
		date = datetime.datetime.now().strftime("%Y-%m-%d")
		self.ui.system_date.setText(str(date))
		QtCore.QTimer.singleShot(1000, self.system_info)
  
		self.ui.system_machine.setText(platform.machine())
		self.ui.system_version.setText(platform.version())
		self.ui.system_platform.setText(platform.platform())
		self.ui.system_system.setText(platform.system())
		self.ui.system_processor.setText(platform.processor())
	
	# function to create table widgets
	def create_table_widget(self, rowPosition, columnPosition, text, tableName):
		qtablewidgetitem = QTableWidgetItem()
		getattr(self.ui, tableName).setItem(rowPosition,columnPosition, qtablewidgetitem)
		qtablewidgetitem = getattr(self.ui, tableName).item(rowPosition, columnPosition)
  
		qtablewidgetitem.setText(text)
 
	# Get running processes/Activities
	def processes(self):
		for x in psutil.pids():
			rowPosition = self.ui.tableWidget.rowCount()
			self.ui.tableWidget.insertRow(rowPosition)

			try:
				process = psutil.Process(x)

				self.create_table_widget(rowPosition,0,str(process.pid),"tableWidget")
				self.create_table_widget(rowPosition,1,str(process.name()),"tableWidget")
				self.create_table_widget(rowPosition,2,str(process.status()),"tableWidget")
				self.create_table_widget(rowPosition,3,str(datetime.datetime.utcfromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S')),"tableWidget")
    
				# create a cell widget
				suspend_btn = QPushButton(self.ui.tableWidget)
				suspend_btn.setText('Suspend')
				suspend_btn.setStyleSheet("color: brown")
				self.ui.tableWidget.setCellWidget(rowPosition, 4, suspend_btn)

				resume_btn = QPushButton(self.ui.tableWidget)
				resume_btn.setText('Resume')
				resume_btn.setStyleSheet("color: green")
				self.ui.tableWidget.setCellWidget(rowPosition, 5, resume_btn)
    
				terminate_btn = QPushButton(self.ui.tableWidget)
				terminate_btn.setText('Terminate')
				terminate_btn.setStyleSheet("color: orange")
				self.ui.tableWidget.setCellWidget(rowPosition, 6, terminate_btn)
    
				kill_btn = QPushButton(self.ui.tableWidget)
				kill_btn.setText('Kill')
				kill_btn.setStyleSheet("color: red")
				self.ui.tableWidget.setCellWidget(rowPosition, 7, kill_btn)
			except Exception as e:
				# handle exception when a process ID is not found
				print(e)
		self.ui.activity_search.textChanged.connect(self.findName)
	
	# search activity table
	def findName(self):
		name = self.ui.activity_search.text().lower()
		for row in range(self.ui.tableWidget.rowCount()):
			item = self.ui.tableWidget.item(row, 1)
			self.ui.tableWidget.setRowHidden(row, name not in item.text().lower())
   
   
	# Storage Partitions
	def storage(self):
		global platforms
		storage_device = psutil.disk_partitions(all=False)
		z = 0
		path = "/"
		for x in storage_device:
			rowPosition = self.ui.storageTable.rowCount()
			self.ui.storageTable.insertRow(rowPosition)
   
			self.create_table_widget(rowPosition, 0, x.device, "storageTable")
			self.create_table_widget(rowPosition, 1, x.mountpoint, "storageTable")
			self.create_table_widget(rowPosition, 2, x.fstype, "storageTable")
			self.create_table_widget(rowPosition, 3, x.opts, "storageTable")

			# check platform
			if sys.platform == "linux" or sys.platform == "linux1" or sys.platform == "linux2":
				self.create_table_widget(rowPosition, 4, str(x.maxfile), "storageTable")
				self.create_table_widget(rowPosition, 5, str(x.maxpath), "storageTable")
			else:
				self.create_table_widget(rowPosition, 4, "Function not available on "  + platforms[sys.platform], "storageTable")
				self.create_table_widget(rowPosition, 5, "Function not available on "  + platforms[sys.platform], "storageTable")
    
			disk_usage = shutil.disk_usage(path)

			self.create_table_widget(rowPosition, 6, str((disk_usage.total / (1024 * 1024 * 1024))) + " GB", "storageTable")
			self.create_table_widget(rowPosition, 7, str((disk_usage.free / (1024 * 1024 * 1024))) + " GB", "storageTable")
			# self.create_table_widget(rowPosition, 8, str((disk_usage.used / (1024 * 1024 * 1024))) + " GB", "storageTable")

			full_disk = (disk_usage.used / disk_usage.total) * 100
			progressBar = QProgressBar(self.ui.storageTable)
			progressBar.setObjectName(u"progressBar")
			progressBar.setValue(full_disk)
			self.ui.storageTable.setCellWidget(rowPosition, 9, progressBar)
   
	# sensors
	def sensors(self):
		if sys.platform == "linux" or sys.platform == "linux1" or sys.platform == "linux2":
			try:
				for x in psutil.sensors_temperatures():
					for y in psutil.sensors_temperatures()[x]:
						rowPosition = self.ui.sensorTable.rowCount()
						self.ui.sensorTable.insertRow(rowPosition)

						self.create_table_widget(rowPosition, 0, x, "sensorTable")
						self.create_table_widget(rowPosition, 1, y.label, "sensorTable")
						self.create_table_widget(rowPosition, 2, str(y.current), "sensorTable")
						self.create_table_widget(rowPosition, 3, str(y.high), "sensorTable")
						self.create_table_widget(rowPosition, 4, str(y.critical), "sensorTable")
			except Exception as e:
				print(e)
  		# else:
		# 	global platforms
		# 	rowPosition = self.ui.sensorTable.rowCount()
		# 	self.ui.sensorTable.insertRow(rowPosition)

		# 	self.create_table_widget(rowPosition, 0, "Function not supported on " + platforms[sys.platform], "sensorTable")
		# 	self.create_table_widget(rowPosition, 1, "N/A", "sensorTable")
		# 	self.create_table_widget(rowPosition, 2, "N/A", "sensorTable")
		# 	self.create_table_widget(rowPosition, 3, "N/A", "sensorTable")
		# 	self.create_table_widget(rowPosition, 4, "N/A", "sensorTable")
		# 	self.create_table_widget(rowPosition, 5, "N/A", "sensorTable")
  
	def networks(self):
		for x in psutil.net_if_stats():
			z = psutil.net_if_stats()
			print(x)
			rowPosition = self.ui.net_stats_table.rowCount()
			self.ui.net_stats_table.insertRow(rowPosition)
   
			self.create_table_widget(rowPosition, 0, x, "net_stats_table")
			self.create_table_widget(rowPosition, 1, str(z[x].isup), "net_stats_table")
			self.create_table_widget(rowPosition, 2, str(z[x].duplex), "net_stats_table")
			self.create_table_widget(rowPosition, 3, str(z[x].speed), "net_stats_table")
			self.create_table_widget(rowPosition, 4, str(z[x].mtu), "net_stats_table")

		for x in psutil.net_io_counters(pernic=True):
			z = psutil.net_io_counters(pernic=True)
			rowPosition = self.ui.net_io_table.rowCount()
			self.ui.net_io_table.insertRow(rowPosition)

			self.create_table_widget(rowPosition, 0, x, "net_io_table")
			self.create_table_widget(rowPosition, 1, str(z[x].bytes_sent), "net_io_table")
			self.create_table_widget(rowPosition, 2, str(z[x].bytes_recv), "net_io_table")
			self.create_table_widget(rowPosition, 3,str(z[x].packets_sent), "net_io_table")
			self.create_table_widget(rowPosition, 4, str(z[x].packets_recv), "net_io_table")
			self.create_table_widget(rowPosition, 5, str(z[x].errin), "net_io_table")
			self.create_table_widget(rowPosition, 6, str(z[x].errout), "net_io_table")
			self.create_table_widget(rowPosition, 7, str(z[x].dropin), "net_io_table")
			self.create_table_widget(rowPosition, 8, str(z[x].dropout), "net_io_table")
   
		for x in psutil.net_if_addrs():
			z = psutil.net_if_addrs()
			for y in z[x]:
				rowPosition = self.ui.net_addresses_table.rowCount()
				self.ui.net_addresses_table.insertRow(rowPosition)

				self.create_table_widget(rowPosition, 0, str(x), "net_addresses_table")
				self.create_table_widget(rowPosition, 1, str(y.family), "net_addresses_table")
				self.create_table_widget(rowPosition, 2, str(y.address), "net_addresses_table")
				self.create_table_widget(rowPosition, 3,str(y.netmask), "net_addresses_table")
				self.create_table_widget(rowPosition, 4, str(y.broadcast), "net_addresses_table")
				self.create_table_widget(rowPosition, 5, str(y.ptp), "net_addresses_table")
    
		for x in psutil.net_connections():
			z = psutil.net_connections()
			rowPosition = self.ui.net_connections_table.rowCount()
			self.ui.net_connections_table.insertRow(rowPosition)

			self.create_table_widget(rowPosition, 0, str(x.fd), "net_connections_table")
			self.create_table_widget(rowPosition, 1, str(x.family), "net_connections_table")
			self.create_table_widget(rowPosition, 2, str(x.type), "net_connections_table")
			self.create_table_widget(rowPosition, 3,str(x.laddr), "net_connections_table")
			self.create_table_widget(rowPosition, 4, str(x.raddr), "net_connections_table")
			self.create_table_widget(rowPosition, 5, str(x.status), "net_connections_table")
			self.create_table_widget(rowPosition, 5, str(x.pid), "net_connections_table")
			
# ## Execute App
if __name__=="__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	qss = "Combinear.qss"
	with open(qss,"r") as f:
		app.setStyleSheet(f.read())
	# window.showMaximized()
	sys.exit(app.exec_())