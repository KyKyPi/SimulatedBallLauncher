import sys
from PyQt5.QtWidgets import (QLabel, QLineEdit, QSlider, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QWidget)
import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import time


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.voltage = None
        self.wheelspeed = None
        self.initialvelocity = None
        self.totaltime = None
        self.maxheight = None

        self.times_list = []
        self.heights_list = []

        # Creates number of points for graph
        self.num_div = 100
        self.time_div = [t/self.num_div for t in range(self.num_div)]

        # Timer
        self.timer = QtCore.QTimer(self)
        self.plot_xval = []
        self.plot_yval = []

        self.init_ui()

    def init_ui(self):
        # Calculations
        self.l1 = QLabel('Voltage Read (V)')
        self.le1 = QLineEdit(None)
        self.b1 = QPushButton('Read Voltage')
        self.l2 = QLabel('Speed of Wheel (rad/s)')
        self.le2 = QLineEdit(None)
        self.l3 = QLabel('Initial Velocity of the ball (m/s)')
        self.le3 = QLineEdit(None)
        self.l4 = QLabel('Total Time of Launch (sec)')
        self.le4 = QLineEdit(None)
        self.l5 = QLabel('Maximum Height of Launch (m)')
        self.le5 = QLineEdit(None)
        self.l6 = QLabel('Notes: ')

        self.l7 = QLabel('1.3 meters')  # Slider max label
        self.l8 = QLabel('0 meters')    # Slider min label

        self.plot = pg.PlotWidget(title="Height (m) vs Time (sec)")
        self.plot.setWindowTitle("Graph")
        self.plot.setXRange(0, 1.1, padding=0)
        self.plot.setYRange(0, 1.3, padding=0)

        # Sim Launcher
        self.s1 = QSlider(Qt.Vertical)
        self.s1.setMinimum(0)
        self.s1.setMaximum(130)
        self.s1.setValue(0)
        self.s1.setTickInterval(5)
        self.s1.setTickPosition(QSlider.TicksBelow)

        v_box1 = QVBoxLayout()
        v_box1.addWidget(self.l1)
        v_box1.addWidget(self.le1)
        v_box1.addWidget(self.b1)
        v_box1.addWidget(self.l2)
        v_box1.addWidget(self.le2)
        v_box1.addWidget(self.l3)
        v_box1.addWidget(self.le3)
        v_box1.addWidget(self.l4)
        v_box1.addWidget(self.le4)
        v_box1.addWidget(self.l5)
        v_box1.addWidget(self.le5)
        v_box1.addWidget(self.l6)

        v_box2 = QVBoxLayout()
        v_box2.addWidget(self.l7)
        v_box2.addWidget(self.s1)
        v_box2.addWidget(self.l8)

        v_box3 = QVBoxLayout()
        v_box3.addWidget(self.plot)

        h_box1 = QHBoxLayout()
        h_box1.addLayout(v_box1)
        h_box1.addStretch()
        h_box1.addLayout(v_box2)
        h_box1.addStretch()
        h_box1.addLayout(v_box3)
        h_box1.addStretch()

        self.setLayout(h_box1)
        self.setWindowTitle("Simulated Launch Station")

        self.b1.setDisabled(True)   # Don't press the button if no number is entered - button is disabled the first time but not after that
        self.le1.textChanged.connect(self.button_enable)
        self.b1.clicked.connect(self.typeVoltage)

        self.show()

    def button_enable(self):
        self.b1.setDisabled(False)

    def typeVoltage(self):
        # self.times_list = []
        # self.heights_list = []
        voltage = float(self.le1.text())
        self.voltage = round(voltage, 2)
        self.le1.setText(str(self.voltage))

        if self.voltage < 1:    # if less than 1V supplied then no launch occurs
            self.zero()
        else:
            self.wheelSpeed()
            self.ballVelocity()
            self.totalTime()
            self.maxHeight()
            self.times()
            self.heights()
            self.timer_connect()
            # self.timer_connect()

    def wheelSpeed(self):
        a = 0.034  # Vs/rad
        b = 98.1  # rad/s
        voltage = self.voltage
        w = (voltage/a) + b
        self.wheelspeed = round(w, 2)
        self.le2.setText(str(self.wheelspeed))

    def ballVelocity(self):
        r = 0.02  # m
        w = self.wheelspeed
        v0 = w * r
        self.initialvelocity = round(v0, 2)
        self.le3.setText(str(self.initialvelocity))

    def totalTime(self):
        vf = 0
        v0 = self.initialvelocity
        g = 9.81  # m/s^2
        t = -(vf - v0)/g
        t = t * 2
        self.totaltime = round(t, 2)
        self.le4.setText(str(self.totaltime))

    def maxHeight(self):
        y0 = 0
        g = 9.81  # m/s^2
        t = self.totaltime
        t = t / 2
        v0 = self.initialvelocity
        yf = -0.5 * g * t * t + v0 * t + y0
        self.maxheight = round(yf, 2)
        self.le5.setText(str(self.maxheight))

    def zero(self):
        self.voltage = 0
        self.le1.setText(str(self.voltage))
        self.wheelspeed = 0
        self.le2.setText(str(self.wheelspeed))
        self.initialvelocity = 0
        self.le3.setText(str(self.initialvelocity))
        self.totaltime = 0
        self.le4.setText(str(self.totaltime))
        self.maxheight = 0
        self.le5.setText(str(self.maxheight))
        self.simlaunch()
        self.l6.setText('Notes: Not enough voltage supplied to launch')

    def times(self):
        self.times_list = []
        t = self.totaltime
        for time_div in self.time_div:
            self.times_list.append(self.totaltime * time_div)
        self.times_list.append(t)

    def heights(self):
        self.heights_list = []
        for time_div in self.time_div:
            t = self.totaltime * time_div
            self.heights_list.append(-0.5 * 9.81 * t * t + self.initialvelocity * t + 0)
            # self.plot.plotItem.plot(self.times_list, self.heights_list)
        self.heights_list.append(0)

    def update_plot(self):
        self.plot.clear()
        self.plot.plotItem.plot(self.times_list, self.heights_list)

    def timer_connect(self):
        self.plot.clear()
        self.timer.timeout.connect(self.update)  # TODO: move to init
        self.timer.start(self.totaltime * 1000 / self.num_div)  # ms

    def update(self):
        i = len(self.plot.plotItem.dataItems)

        self.plot.plotItem.plot(self.times_list[:i+1], self.heights_list[:i+1])
        self.s1.setValue(self.heights_list[i] * 100)

        if i == len(self.heights_list) - 1:
            self.timer.stop()
            self.timer.disconnect()  # TODO: Delete


    # def update(self, time_div):
    #     for time_div in self.time_div:
    #         xval = (self.totaltime * time_div)
    #         yval = -0.5 * 9.81 * xval * xval + self.initialvelocity * xval + 0
    #         self.times_list.append(xval)
    #         self.heights_list.append(yval)
    #         # time.sleep(0.1)
    #         self.s1.setValue(yval*100)
    #         self.plot.plotItem.plot(self.times_list, self.heights_list)
    #         self.times_list.append(self.totaltime)
    #     self.heights_list.append(0)
    #     self.s1.setValue(0 * 100)
    #     self.plot.plotItem.plot(self.times_list, self.heights_list)

    # def update(self):
    #     xvals = []
    #     yvals = []
    #     xval = (self.totaltime * time_div)
    #     yval = -0.5 * 9.81 * xval * xval + self.initialvelocity * xval + 0
    #     xvals.append(xval)
    #     yvals.append(yval)
    #     self.timer.setInterval(1000)  # in milliseconds
    #     self.timer.start()
    #     while ~self.timer.timeout:
    #         pass
    #     self.s1.setValue(yval*100)
    #     self.plot.clear()
    #     self.plot.plotItem.plot(xvals, yvals)
    #     xvals.append(self.totaltime)
    #     yvals.append(0)
    #     self.plot.plotItem.plot(xvals, yvals)

# Install a global exception hook to catch pyQt errors that fall through (helps with debugging a ton)
# #TODO: Remove for builds
sys.__excepthook = sys.excepthook
sys._excepthook  = sys.excepthook
def exception_hook(exctype, value, traceback):
   sys._excepthook(exctype, value, traceback)
   sys.exit(1)
sys.excepthook = exception_hook


app = QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())
