#!/usr/bin/env python3
#
# Copyright 2015,2020 Clayton Smith
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

from hackrf_rx import hackrf_rx
from hackrf_tx import hackrf_tx
from morse_table import morse_seq

from PyQt5 import Qt
from gnuradio.eng_option import eng_option
from gnuradio import gr
from optparse import OptionParser
from distutils.version import StrictVersion
import signal


class hackrf_rx_tx(hackrf_rx):
    def __init__(self):
        super(hackrf_rx_tx, self).__init__()
        self.tx = hackrf_tx()

    def set_tx_text(self, tx_text):
        if self.band == self.cal_band:
            return

        self.stop()
        self.wait()
        self.tx.set_rf_gain(self.amp_enable)
        self.tx.set_if_gain(self.tx_gain)
        self.tx.set_correction(self.correction)
        self.tx.set_band(self.band)
        self.tx.set_tune(self.tune)
        self.tx.set_cw_vector(morse_seq(tx_text) + (0,)*20)
        self.tx.run()
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
            print("Warning: failed to XInitThreads()")

if __name__ == '__main__':

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = hackrf_rx_tx()
    tb.start()
    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()
