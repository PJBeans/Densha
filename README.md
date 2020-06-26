# Densha
Densha is a desktop environment for Linux (targeted at Ubuntu) written in Python with PyQT

This DE is considered in Alpha. Don't use it except for dev purposes!

Folders:

- `main`: The top panel application. This should be renamed at some point.
- `dock`: The bottom dock application. Includes app launcher.
- `Settings`: The Densha Settings application.

Compiling:

There is no straight-forward process to compiling in that there is no make file or anything neat like that. Just use `pyinstaller` to compile each application individually. From there, they can be started independently. A compile script and installation script will be created to automate this process.
