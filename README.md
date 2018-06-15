# BattleCOGS
This is a programming game where you customize the look, feel and brain of your robot. Upload code that tells your robot how to work, and watch it battle in a winner takes all arena!

## Installation
The engine is written in Python, as is the logic of your robot. This app requires Python 2.7 or Python 3.4+, and uses _pip_ to install the other required modules. Begin by making sure you have a valid Python installation as well as _pip_.

### Installing Python
[Python Download Page](https://www.python.org/downloads/)

### Installing Pip
Download the get-pip script from [HERE](https://bootstrap.pypa.io/get-pip.py). Now run the following as admin/root:
```bash
C:\Python27\python.exe get-pip.py
```
### Install Modules
```bash
cd BattleCOGS\
C:\Python27\python.exe -m pip install -r requirements.txt
```

## Usage
There are a few important programs. _main.py_ is the code that runs a battle between the specified robots. This can be ran as such:
```bash
C:\Python27\python.exe main.py [ROBOT1] [ROBOT2] 
```

Another available program is the one that allows uploading new code to a BattleCOGS server. The _webapp.py_ program hosts a web server using _flask_ and will allow other on the network to connect at your IP address on port 50. (e.g - 10.25.80.25:5000/). They can then use the web gui or HTTP requests to upload a python file that contains their bot's code. Use the following to launch:
```bash
C:\Python27\python.exe webapp.py
```

The final program that is available is _playback.py_. This program accepts a _.match_ file and will allow the user to step through a previously recorded match. The idea here is that you can run a match, and then share it with someone else, without them needing the entire program to run.

## Creating a Robot
The first step in creating your robot is to make a file, named after your robot. For this example, our robot is called _ExampleRobot_. This file should live in your local repositories bots/ directory. This will allow it to reference the parent class, _Bot_. Now add the following skeleton code, which will create a subclass of the _Bot_ class.
```python
from bots.Bot import Bot
from util.Direction import Direction

class ExampleRobot(Bot):
	def __init__(self):
		Bot.__init__(self)
		self.symbol = "E"

	def configure(self):
		return

	def run(self):
		self.action.shoot()
		return
```

When a match begins, the robot gets a chance to configure its equipment with it's _configure()_ function. Please see the section, _Configuring a Robot_, for the API associated with this step.

The other important function is _run()_. This function is ran everytime your robot is available to take an action. This is where your robot makes decisions on what it will do next. In the above example, this robot merely shoots, and then waits until it can shoot again. It is important to note that it is up to you to maintain logic between calls to _run()_. A basic shoot action for example takes X ticks. This means that once you shoot, it will be X ticks in the game before your _run()_ function is called again. 

Another important note is that calling an ACTION call such as `self.action.shoot()`, doesn't action start the _shoot()_ action. ACTION calls merely queue up the next action that wil happen once the _run()_ function returns. This means you can issue many ACTION calls, but only the last one will actually happen once your function returns.


