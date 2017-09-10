
3. Write a README.md document that describes your project. 
- What did you do?
- What equipment, tools, software, and/or hardware did you use?
- Who is this project for?
- Can others contribute to your project?
- Remember the confetti cannon - it's so sad when you find a confetti cannon but no one knows how to use it. Tradegies like these can be avoided by writing great documentation as you go!

4. Don't be shy about sharing your code, project plan, or designs! Open Source is all about colaboration. Nothing is perfect, and that's ok! [Done is better than perfect](https://twitter.com/lettershoppe/status/897213248260460544), so get it up on GitHub! Your code lives in the repository along with these text documents.

5. Link out to a [CONTRIBUTING.md](https://github.com/ScienceHackDayPDX/TEMPLATE-project-repository/blob/master/CONTRIBUTING.md) guide that will show people how they can help. 

6. If your project is going to involve people, get everyone on the same page with a [CODEOFCONDUCT.md](https://github.com/ScienceHackDayPDX/TEMPLATE-project-repository/blob/master/CODE_OF_CONDUCT.md).

7. Is this just the beginning for your project? Write a [ROADMAP.md](https://github.com/ScienceHackDayPDX/TEMPLATE-project-repository/blob/master/ROADMAP.md) to let contributors know where the project is going!

# Requirements
* Arduino uno
* python 2.7
* Use your package manager to `install pip`
* On your command line run
```  
# for Mac: 
$ brew install portaudio  

# then: 
$ sudo pip install flask requests serial pyaudio 
```

# Usage
* Clone this repository
* Connect your arduino
* Discover your serial port name by:
```
# Before connecting Arduino:
$ ls /dev/ >> ~/before.txt

# After conencting Arduino:
$ ls /dev/ >> ~/after.txt

# Find the new device:
$ diff ~/before.txt ~/after.txt

# On Mac OS, the device will be something like /dev/tty.usbmodem14611.
# On Linux, the device will be something like /dev/ttyACM0
```
* Update the `ser` variable on line 34 in `climate.py`
* In your terminal:
```
$ cd climate
$ python climate.py
# some systems need to run: python2 climate.py
```

