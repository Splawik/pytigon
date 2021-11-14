PYTIGON
=======

What is it
----------

Pytigon is a combination of several technologies: python, django, 
wxWidgets to create one coherent development environment.

Key capabilities of Pytigon:

- Create an application using popular technologies:

   - Python language

   - django web framework

   - wxWidgets client for desktop program

   - bootstrap based web client

- Run application everywhere:

   - desktop application for: Linux, Windows, OSX,

   - web based client for mobile and desktop devices.

- The strong integration of all components
   
   - Python philosophy everywhere: modified django templates based on 
     indentations, embeded python to javascript compiler (Transcrypt)
   
   - wxPython widgets integrated with django model fields
   
   - django server integrated with wxPython client program

- All in one Pytigon IDE - ide allows you to create program and
  make instalation program.


Instalation
-----------

1. Windows

   - Download and run instalation program. Instalation program contain
     python enviroment with all needed libraries.
   
2. Linux

   - In the selected folder run command: 
     
     `git clone https://github.com/Splawik/pytigon.git 
     cd pytigon
     bash install.sh`
     
   - Install wxPython-Phoenix 
     ( `https://wiki.wxpython.org/How to install wxPython`_ )
     

Run     
---

run command in pytigon folder: 

Windows:
   
   python\python pytigon.py app_name
   
Linux: 
   
   python/bin/python pytigon.py app_name
   
First application which you can test is schdevtools - Pytigon ide.
Run: ...python pytigon.py schdevtools
     