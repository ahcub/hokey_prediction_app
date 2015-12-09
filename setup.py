from distutils.core import setup
import py2exe

setup(windows=[{"script": "hockey_prediction_app.py"}], options={"py2exe":{"includes":["sip", 'lxml.etree', 'lxml._elementpath', 'gzip', 'pandas', 'numpy']}},
      requires=['requests', 'lxml', 'PyQt4', 'pandas'])
