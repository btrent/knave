knave
==========

Work in progress chess app for Mac, Linux, and Android.

This is based on the hard work and open source projects of:
* Shivkumar Shivaji - https://github.com/sshivaji/kivy-chess
* Mario Balibrera - https://pypi.python.org/pypi/chesstools/0.1.8
* Niklas Fiekas - https://github.com/niklasf/python-chess

As well as the legions who have contributed to Kivy, Python-For-Android, Python, etc.

To build for Mac or Linux:
   1. Download Kivy
   2. Install and test that kivy works
   3. Execute "kivy main.py"

To build/install for Android:
   1. Do everything in the above list and make sure the app doesn't crash
   2. Install Buildozer
   3. Install (via Buildozer or directly) Android SDK (at least version 21) including platform-tools and NDK (at least version 8e)
   4. Make sure the JAVA_HOME environment variable is set correctly
   5. Execute "buildozer android debug deploy run"
   6. If deployed to a connected device, execute "adb logcat"
