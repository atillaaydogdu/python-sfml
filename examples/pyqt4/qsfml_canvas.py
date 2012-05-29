#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pySFML2 - Cython SFML Wrapper for Python
# Copyright 2012, Jonathan De Wachter <dewachter.jonathan@gmail.com>
#
# This software is released under the GPLv3 license.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, platform

try:
        import sip
        from PyQt4.QtCore import *
        from PyQt4.QtGui import *
except ImportError(e):
        print("Install PyQt4 and sip from Riverbank.The package name is python-pyqt4 and python-sip")
        
import sfml as sf

class QSFMLCanvas(QWidget):
	def __init__(self, parent, position, size, frameTime=0):
		QWidget.__init__(self, parent)
		self.initialized = False
		
		w = size.width()
		h = size.height()
		
		self._HandledWindow = sf.HandledWindow()
		self._HandledWindow.view.size = (w, h)
		self.__dict__['draw'] = self._HandledWindow.draw
		self.__dict__['clear'] = self._HandledWindow.clear
		self.__dict__['view'] = self._HandledWindow.view
		self.__dict__['display'] = self._HandledWindow.display
		
		# setup some states to allow direct rendering into the widget
		self.setAttribute(Qt.WA_PaintOnScreen)
		self.setAttribute(Qt.WA_OpaquePaintEvent)
		self.setAttribute(Qt.WA_NoSystemBackground)
		
		# set strong focus to enable keyboard events to be received
		self.setFocusPolicy(Qt.StrongFocus);
		
		# setup the widget geometry
		self.move(position);
		self.resize(size);

		# setup the timer
		self.timer = QTimer()
		self.timer.setInterval(frameTime)
		
	def onInit(self): pass
	
	def onUpdate(self): pass
	
	def sizeHint(self):
		return self.size()
		
	def paintEngine(self):
		# let the derived class do its specific stuff
		self.onUpdate()

		# display on screen
		self.display()

	def showEvent(self, event):
		if not self.initialized:
			# under X11, we need to flush the commands sent to the server 
			# to ensure that SFML will get an updated view of the windows
			# create the SFML window with the widget handle
			if platform.system() == 'Linux':
				import sfml.graphics.x11 as x11
				display = sip.unwrapinstance(QX11Info.display())
				x11.flush_screen(display)
				
			self._HandledWindow.create(self.winId())
			
			# let the derived class do its specific stuff
			self.onInit()
			
			# setup the timer to trigger a refresh at specified framerate
			self.connect(self.timer,SIGNAL('timeout()'), self, SLOT('repaint()'))
			self.timer.start()
			
			self.initialized = True

	def paintEvent(self, event):
		return None
