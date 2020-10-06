# Intro

These are popular games implemented with the help of the [wxPython](https://wxpython.org/) library.

# Setup

You have TWO CHOICES in installing the required library. 

I. Try to make a 
sh
pip install -r req.txt
If you have errors, try looking at the necessary widgets for your device in https://downloads.codelite.org/. 

<hr>

II. Do the installation manually, below we will leave all the necessary instructions for setting up your environment.

All information about installing and configuring the environment was taken from the official source [wxpython.org](https://wxpython.org/pages/downloads/)

## Current Release

Starting with wxPython 4.0 (the first Phoenix release) the wxPython source archive and, for supported platforms, wxPython binary wheels are available from the Python Package Index (PyPI). wxPython's project page at PyPI is https://pypi.org/project/wxPython.

The source or binary wheels can be downloaded directly from the project page, or you can use the wonderful pip tool to do it for you.

## Windows and macOS

sh
pip install -U wxPython

If you are on Windows or macOS with a compatible Python build, then the command shown above will download the appropriate wheel file from the latest release, and install it in your active Python environment or virtual environment.

If there is no binary wheel file available for your platform or for your version of Python, then pip will download the source archive and will attempt to build it for you. There is some information about that below.

## Yes, we have Linux Wheels. Sort of.

Because of the differences between Linux distributions (mainly different versions of the core libraries installed by default, but also platform architecture and etc.) it is not possible to host binary wheel files for Linux on PyPI unless they can be made to work within the constraints of PEP 513 Unfortunately, attempts to pound the wxPython peg into the manylinux1 hole have not been very successful. Maybe manylinux2 will be a better fit. In the meantime, if you have a Linux similar enough to those used to build the wheels located under the wxPython Extras linux folder, then you can use them and not need to build the wheels yourself.

Since there are various options for distro and wx port (GTK2 or GTK3) then the files can not all be located in the same folder for easy access by pip. This simply just means that you'll need to drill down a little further to find the URL to give to pip. For example, to get the GTK3 wxPython builds for Ubuntu 16.04 (and 16.10, LinuxMint 18, and probably others) you can use a pip command like this:

sh
pip install -U \
    -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 \
    wxPython
Of course you can always download the wheel file yourself and then use pip to install your local copy of the file.

# StackOverflow

- [How to fix “libpng12.so.0: cannot open shared object file: No such file or directory”?](https://askubuntu.com/questions/978294/how-to-fix-libpng12-so-0-cannot-open-shared-object-file-no-such-file-or-direc)
- [ImportError libSDL2-2.0.so.0 in wxPython wx.adv](https://stackoverflow.com/questions/59273517/importerror-libsdl2-2-0-so-0-in-wxpython-wx-adv)