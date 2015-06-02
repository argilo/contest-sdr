#!/usr/bin/env python2
#
# Copyright 2014 Clayton Smith
#
# This file is part of contest-sdr
#
# contest-sdr is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# contest-sdr is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with contest-sdr; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

from vhf_rx import vhf_rx
from vhf_tx import vhf_tx
from morse_table import morse_seq

from PyQt4 import Qt
from gnuradio.eng_option import eng_option
from gnuradio import gr
from optparse import OptionParser
from distutils.version import StrictVersion

class vhf_rx_tx(vhf_rx):
    def __init__(self):
        super(vhf_rx_tx, self).__init__()
        self.tx = vhf_tx()

    def set_tx_text(self, tx_text):
        self.stop()
        self.wait()
        self.tx.set_cw_vector(morse_seq(tx_text))
        self.tx.start()
        self.tx.wait()
        self.tx.stop()
        self.start()

        self.tx_text = ""
        Qt.QMetaObject.invokeMethod(self._tx_text_line_edit, "setText", Qt.Q_ARG("QString", str(self.tx_text)))

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if(StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0")):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = vhf_rx_tx()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets
