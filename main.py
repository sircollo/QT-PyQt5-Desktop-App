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
		self.show()
		



## Execute App
if __name__=="__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	# window.showMaximized()
	sys.exit(app.exec_())