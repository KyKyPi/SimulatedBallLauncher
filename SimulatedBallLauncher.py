# This script creates a Raspberry Pi simulator to teach high school students
# about circuits and parabolic motion.
# The simulator takes in readings from the Raspberry Pi. One value is the
# value measuring the voltage in a voltage divider after going through an ADC.
# The other value is just a GPIO pin which determines if the connected switch
# has been flipped.
# This simulator consists of four instances of a class (Window). This class
# creates one 'simulator'. By creating four instances, a single screen will
# display 4 'simulators' so 4 students can use the simulator at the same time.
# Each instance will include an output of various calculations, a simulated
# ball launch, and a height vs time graph.

import sys
from PyQt5.QtWidgets import (QLabel, QLineEdit, QSlider, QVBoxLayout,
                             QHBoxLayout, QApplication, QWidget,
                             QDesktopWidget)
import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import Adafruit_ADS1x15
import RPi.GPIO as GPIO


# This class creates one widget window which will contain one launch simulator
# including calculation outputs, vertical launch simulator, and height vs
# time plot. The overall simulator will include 4 instances of this class.
class Window(QWidget):

    def __init__(self, input):
        super().__init__()
        self.screen = QDesktopWidget().availableGeometry(-1)
        # Position instance 0, assign pins, background = cyan
        if input == 0:
            self.setGeometry(0, 0, self.screen.width() / 2,
                             self.screen.height() / 2)
            self.button_pin = 14
            self.adc_pin = 0
            self.background_color = Qt.cyan
        # Position instance 1, assign pins, background = yellow
        elif input == 1:
            self.setGeometry(self.screen.width() / 2, 0,
                             self.screen.width() / 2, self.screen.height() / 2)
            self.button_pin = 15
            self.adc_pin = 1
            self.background_color = Qt.yellow
        # Position instance 2, assign pins, background = magenta
        elif input == 2:
            self.setGeometry(0, self.screen.height() / 2,
                             self.screen.width() / 2, self.screen.height() / 2)
            self.button_pin = 17
            self.adc_pin = 2
            self.background_color = Qt.magenta
        # Position instance 3, assign pins, background = green
        else:
            self.setGeometry(self.screen.width() / 2,
                             self.screen.height() / 2, self.screen.width() / 2,
                             self.screen.height() / 2)
            self.button_pin = 18
            self.adc_pin = 3
            self.background_color = Qt.green

        # Hides window title bar
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)

        # Create calculation variables
        self.voltage = None
        self.wheelspeed = None
        self.initialvelocity = None
        self.totaltime = None
        self.maxheight = None
        self.times_list = []
        self.heights_list = []

        # Set window background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), self.background_color)
        self.setPalette(p)

        # Creates number of points for graph
        self.num_div = 15
        self.time_div = [t/self.num_div for t in range(self.num_div)]

        # Create plot timer
        self.timer = QtCore.QTimer(self)
        self.plot_xval = []
        self.plot_yval = []
        self.timer.timeout.connect(self.update)

        # Initialize the user interface
        self.init_ui()

        # GPIO Timer
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.timer1 = QtCore.QTimer(self)
        self.timer1.timeout.connect(self.readVoltage)
        self.timer1.start(100)

    # Initialize the user interface
    def init_ui(self):
        # Calculations
        self.l1 = QLabel('Voltage Read (V)')
        self.le1 = QLineEdit(None)
        self.l2 = QLabel('Speed of Wheel (rad/s)')
        self.le2 = QLineEdit(None)
        self.l3 = QLabel('Initial Velocity of the ball (m/s)')
        self.le3 = QLineEdit(None)
        self.l4 = QLabel('Total Time of Launch (sec)')
        self.le4 = QLineEdit(None)
        self.l5 = QLabel('Maximum Height of Launch (m)')
        self.le5 = QLineEdit(None)
        self.l6 = QLabel('Notes: ')

        # Slider - projectile simulator
        self.l7 = QLabel('0.9 meters')  # Slider max label
        self.l8 = QLabel('0 meters')    # Slider min label

        # Height vs Time plot
        self.plot = pg.PlotWidget(title="Height (m) vs Time (sec)")
        self.plot.setWindowTitle("Graph")
        self.plot.setXRange(0, 0.9, padding=0)
        self.plot.setYRange(0, 0.9, padding=0)

        # Sim Launcher
        self.s1 = QSlider(Qt.Vertical)
        self.s1.setMinimum(0)
        self.s1.setMaximum(90)
        self.s1.setValue(0)
        self.s1.setTickInterval(5)
        self.s1.setTickPosition(QSlider.TicksBelow)

        # Create user interface layout and add widgets
        v_box1 = QVBoxLayout()
        v_box1.addWidget(self.l1)
        v_box1.addWidget(self.le1)
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

        # Show the user interface
        self.show()

    # Read in the value from the ADC and calculate the voltage
    # From the calculated voltage value, calculate the wheel speed, ball
    # velocity, total time, and max height
    # Also, move the slider to simulate the launch and plot the height vs
    # time graph
    def readVoltage(self):
        # If the switch is flipped, start the simulator
        if GPIO.input(self.button_pin) == 1:
            adc = Adafruit_ADS1x15.ADS1115()

            GAIN = 1

            adc_val = adc.read_adc(self.adc_pin, gain=GAIN)
            self.voltage = (3.3 * adc_val) / 26551
            self.voltage = round(self.voltage, 2)

            # If voltage less than 1V supplied then no launch occurs
            if self.voltage < 1:
                self.zero()
            # Otherwise, start the simulator launch
            else:
                self.l6.setText('Notes:')
                self.le1.setText(str(self.voltage))
                self.wheelSpeed()
                self.ballVelocity()
                self.totalTime()
                self.maxHeight()
                self.times()
                self.heights()
                self.timer_connect()

    # Calculate the wheel speed based on the voltage
    def wheelSpeed(self):
        a = 0.034  # Vs/rad
        b = 98.1  # rad/s
        voltage = self.voltage
        w = (voltage/a) + b
        self.wheelspeed = round(w, 2)
        self.le2.setText(str(self.wheelspeed))

    # Calculate the ball velocity based on the wheel speed
    def ballVelocity(self):
        r = 0.02  # m
        w = self.wheelspeed
        v0 = w * r
        self.initialvelocity = round(v0, 2)
        self.le3.setText(str(self.initialvelocity))

    # Calculate the total time based on the initial velocity and the total time
    def totalTime(self):
        vf = 0
        v0 = self.initialvelocity
        g = 9.81  # m/s^2
        t = -(vf - v0)/g
        t = t * 2
        self.totaltime = round(t, 2)
        self.le4.setText(str(self.totaltime))

    # Calculate the maximum height based on the total time and initial velocity
    def maxHeight(self):
        y0 = 0
        g = 9.81  # m/s^2
        t = self.totaltime
        t = t / 2
        v0 = self.initialvelocity
        yf = -0.5 * g * t * t + v0 * t + y0
        self.maxheight = round(yf, 2)
        self.le5.setText(str(self.maxheight))

    # If the voltage is < 1V, there is not enough voltage to launch
    # Print a note saying not enough voltage and set all calculated values to 0
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
        self.plot.clear()
        self.l6.setText('Notes: Not enough voltage supplied to launch')

    # Create a list of times by dividing the total time by a time divisor
    def times(self):
        self.times_list = []
        t = self.totaltime
        for time_div in self.time_div:
            self.times_list.append(self.totaltime * time_div)
        self.times_list.append(t)

    # Find the height at each time in the times list, store the height values
    # in a list
    def heights(self):
        self.heights_list = []
        for time_div in self.time_div:
            t = self.totaltime * time_div
            self.heights_list.append(-0.5 * 9.81 * t * t + self.initialvelocity
                                     * t + 0)
        self.heights_list.append(0)

    # Stop and start the plot timer
    def timer_connect(self):
        self.plot.clear()
        self.timer1.stop()
        self.timer.start(self.totaltime * 1000 / self.num_div)  # ms

    # Each time the timer runs out, pdate the slider to the current height of
    # the launcher and update the height vs time plot with the current height
    # and time of the launch
    def update(self):
        i = len(self.plot.plotItem.dataItems)

        self.plot.plotItem.plot(self.times_list[i-1:i+1],
                                self.heights_list[i-1:i+1])
        self.s1.setValue(self.heights_list[i] * 100)

        if i == len(self.heights_list) - 1:
            self.timer.stop()
            self.timer1.start()


# # Install a global exception hook to catch pyQt errors that fall through
# # (helps with debugging a ton)
# # #TODO: Remove for builds
# sys.__excepthook = sys.excepthook
# sys._excepthook  = sys.excepthook
# def exception_hook(exctype, value, traceback):
#    sys._excepthook(exctype, value, traceback)
#    sys.exit(1)
# sys.excepthook = exception_hook

# Create the overall simulator and 4 instances of the Window class.
# This will allow for 4 students to use the simulator at the same time.
app = QApplication(sys.argv)
a_window = Window(0)
b_window = Window(1)
c_window = Window(2)
d_window = Window(3)
sys.exit(app.exec_())
