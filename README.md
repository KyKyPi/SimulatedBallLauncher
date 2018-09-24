# Simulated Ball Launcher
Software and documentation for my Barrett honors thesis. \
Raspberry Pi and voltage divider circuit driven simulated ball launcher, calculations, and graph.

* This ReadMe only includes a small portion of my honors thesis and only a small portion of what was presented in the high school classroom. For more details please read my final report, KyleeBurgess_HonorsThesis_FinalReport.pdf.

## Inspiration
I am studying to become an electrical engineer, but I didn't know what a capacitor was until college. There are many STEM programs that high school students can sign up for to learn more about circuits and electrical engineering. But most students aren't going to sign up for an extra program or elective class if they don't already have interest in the topic.
This lesson, circuit kit, and simulator aims to introduce high school students to circuits in their required math or science classes in order to peak their interest to pursue other available programs.

## The Kit
Each kit was used by a group of 3-4 students. \
1- Multimeter \
1 - Breadboard \
1 - 9V battery \
1 - Battery connector \
1 - LEDs \
3 - Jumper wires \
1 - Switch \
14 - Resistors
![KitCircuit](https://github.com/KyKyPi/SimulatedBallLauncher/blob/master/KitCircuit.png)

## The Simulator
1 - Projector \
1- Raspberry Pi \
1- Analog to Digital converter \
1- HDMI cord \
16 - Alligator clips \
10 - Jumper wires
*All of the launch station components were provided pre-assembled for this lesson. The Raspberry Pi was just plugged into an outlet and the projector.

SimulatedBallLauncher.py takes in readings from the Raspberry Pi. One value is the value measuring the voltage in a voltage divider circuit after going through an ADC. The other value is just a GPIO pin which determines if the connected switch has been flipped. This simulator consists of four instances of a class (Window). This class creates one 'simulator'. By creating four instances, a single screen will display 4 'simulators' so 4 students can use the simulator at the same time. Each instance will include an output of various calculations, a simulated ball launch, and a height vs time graph.
![SingleInstance](https://github.com/KyKyPi/SimulatedBallLauncher/blob/master/SimSingleInstance.png)
![FourInstances](https://github.com/KyKyPi/SimulatedBallLauncher/blob/master/SimFourInstance.png)

The full simulator and kit set up is shown below.
![FullSystem](https://github.com/KyKyPi/SimulatedBallLauncher/blob/master/FullSystem.png)
A: Raspberry Pi \
B: ADC \
C: Wires to switch \
D: Wires to sense voltage \
E: Power/Ground wires

For the lesson, students were asked to preform these calculations by hand prior to connecting their circuit to the simulator. Running the simulator, allows them to check their calculations and see a simulated version of their theoretical launch.

## Important Documents
SimulatedBallLauncher.py
- Actual code used in simulator

KyleeBurgess_HonorsThesis_FinalReport.pdf
- Submitted honors thesis final report
- Includes...
  - Inspiration for the project
  - Related works
  - Initial Designs
  - Final Design
  - User Feedback
  - Reflection/Lessons Learned
  - Future Work

SimReadVoltage.py
- Code used to read in a value from an ADC with a Raspberry Pi and convert it to a voltage.
- This code is already included as necessary in SimulatedBallLauncher.py

[Barrett Honors Thesis Repository](https://repository.asu.edu/items/47900)
