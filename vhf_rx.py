#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Vhf Rx
# GNU Radio version: 3.8.0.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio.qtgui import Range, RangeWidget
import osmosdr
import time
from gnuradio import qtgui

class vhf_rx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Vhf Rx")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Vhf Rx")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "vhf_rx")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.cal_freq = cal_freq = 626309441
        self.cal_band = cal_band = (cal_freq - 100e3) / 1e6
        self.tx_text = tx_text = ''
        self.tx_gain = tx_gain = 20
        self.tune = tune = 100
        self.samp_rate = samp_rate = 4000000
        self.offset = offset = 200000
        self.lna_enable = lna_enable = False
        self.if_gain = if_gain = 16
        self.decimation = decimation = 20
        self.correction = correction = 0
        self.bb_gain = bb_gain = 24
        self.band = band = cal_band
        self.amp_enable = amp_enable = False

        ##################################################
        # Blocks
        ##################################################
        self._tune_range = Range(80, 120, 0.01, 100, 200)
        self._tune_win = RangeWidget(self._tune_range, self.set_tune, 'Tune (kHz)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._tune_win, 1, 4, 1, 3)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        _lna_enable_check_box = Qt.QCheckBox('LNA')
        self._lna_enable_choices = {True: True, False: False}
        self._lna_enable_choices_inv = dict((v,k) for k,v in self._lna_enable_choices.items())
        self._lna_enable_callback = lambda i: Qt.QMetaObject.invokeMethod(_lna_enable_check_box, "setChecked", Qt.Q_ARG("bool", self._lna_enable_choices_inv[i]))
        self._lna_enable_callback(self.lna_enable)
        _lna_enable_check_box.stateChanged.connect(lambda i: self.set_lna_enable(self._lna_enable_choices[bool(i)]))
        self.top_grid_layout.addWidget(_lna_enable_check_box, 0, 2, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._if_gain_range = Range(0, 40, 8, 16, 200)
        self._if_gain_win = RangeWidget(self._if_gain_range, self.set_if_gain, 'IF gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._if_gain_win, 0, 3, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._correction_range = Range(-20, 20, 1, 0, 200)
        self._correction_win = RangeWidget(self._correction_range, self.set_correction, 'PPM', "counter", float)
        self.top_grid_layout.addWidget(self._correction_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._bb_gain_range = Range(0, 62, 2, 24, 200)
        self._bb_gain_win = RangeWidget(self._bb_gain_range, self.set_bb_gain, 'BB gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._bb_gain_win, 0, 4, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 5):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._band_options = [cal_band, 50, 144, 222, 432, 903, 1296, 2304, 3456, 5760]
        # Create the labels list
        self._band_labels = ["Calib.", "50", "144", "222", "432", "903", "1296", "2304", "3456", "5760"]
        # Create the combo box
        self._band_tool_bar = Qt.QToolBar(self)
        self._band_tool_bar.addWidget(Qt.QLabel('Band' + ": "))
        self._band_combo_box = Qt.QComboBox()
        self._band_tool_bar.addWidget(self._band_combo_box)
        for _label in self._band_labels: self._band_combo_box.addItem(_label)
        self._band_callback = lambda i: Qt.QMetaObject.invokeMethod(self._band_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._band_options.index(i)))
        self._band_callback(self.band)
        self._band_combo_box.currentIndexChanged.connect(
            lambda i: self.set_band(self._band_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._band_tool_bar, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.volume_mult = blocks.multiply_const_ff(10)
        self.usb_filter = filter.fir_filter_ccc(
            25,
            firdes.complex_band_pass(
                1,
                samp_rate / decimation,
                200,
                2800,
                200,
                firdes.WIN_HAMMING,
                6.76))
        self._tx_text_tool_bar = Qt.QToolBar(self)
        self._tx_text_tool_bar.addWidget(Qt.QLabel('CW to send' + ": "))
        self._tx_text_line_edit = Qt.QLineEdit(str(self.tx_text))
        self._tx_text_tool_bar.addWidget(self._tx_text_line_edit)
        self._tx_text_line_edit.returnPressed.connect(
            lambda: self.set_tx_text(str(str(self._tx_text_line_edit.text()))))
        self.top_grid_layout.addWidget(self._tx_text_tool_bar, 1, 0, 1, 4)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._tx_gain_range = Range(0, 47, 1, 20, 200)
        self._tx_gain_win = RangeWidget(self._tx_gain_range, self.set_tx_gain, 'TX gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._tx_gain_win, 0, 6, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.rf_in = osmosdr.source(
            args="numchan=" + str(1) + " " + 'hackrf=0'
        )
        self.rf_in.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rf_in.set_sample_rate(samp_rate)
        self.rf_in.set_center_freq(band * 1e6 + 100000 - offset, 0)
        self.rf_in.set_freq_corr(correction, 0)
        self.rf_in.set_gain(14 if lna_enable else 0, 0)
        self.rf_in.set_if_gain(if_gain, 0)
        self.rf_in.set_bb_gain(bb_gain, 0)
        self.rf_in.set_antenna('', 0)
        self.rf_in.set_bandwidth(1750000, 0)
        self.offset_osc_2 = analog.sig_source_c(samp_rate / decimation, analog.GR_COS_WAVE, 100000 - tune * 1000 + 700, 1, 0, 0)
        self.offset_osc_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -offset, 1, 0, 0)
        self.mixer_2 = blocks.multiply_vcc(1)
        self.mixer_1 = blocks.multiply_vcc(1)
        self.interpolator = filter.rational_resampler_fff(
                interpolation=6,
                decimation=1,
                taps=None,
                fractional_bw=None)
        self.if_waterfall = qtgui.waterfall_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            100000, #fc
            samp_rate / decimation, #bw
            "", #name
            1 #number of inputs
        )
        self.if_waterfall.set_update_time(0.10)
        self.if_waterfall.enable_grid(False)
        self.if_waterfall.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.if_waterfall.set_line_label(i, "Data {0}".format(i))
            else:
                self.if_waterfall.set_line_label(i, labels[i])
            self.if_waterfall.set_color_map(i, colors[i])
            self.if_waterfall.set_line_alpha(i, alphas[i])

        self.if_waterfall.set_intensity_range(-120, 0)

        self._if_waterfall_win = sip.wrapinstance(self.if_waterfall.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._if_waterfall_win, 3, 0, 1, 7)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.if_filter = filter.fir_filter_ccf(
            decimation,
            firdes.low_pass(
                1,
                samp_rate,
                75000,
                25000,
                firdes.WIN_HAMMING,
                6.76))
        self.cx_to_real = blocks.complex_to_real(1)
        self.audio_waterfall = qtgui.waterfall_sink_f(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            8000, #bw
            "", #name
            1 #number of inputs
        )
        self.audio_waterfall.set_update_time(0.10)
        self.audio_waterfall.enable_grid(False)
        self.audio_waterfall.enable_axis_labels(True)


        self.audio_waterfall.set_plot_pos_half(not False)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.audio_waterfall.set_line_label(i, "Data {0}".format(i))
            else:
                self.audio_waterfall.set_line_label(i, labels[i])
            self.audio_waterfall.set_color_map(i, colors[i])
            self.audio_waterfall.set_line_alpha(i, alphas[i])

        self.audio_waterfall.set_intensity_range(-120, 0)

        self._audio_waterfall_win = sip.wrapinstance(self.audio_waterfall.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._audio_waterfall_win, 4, 0, 1, 7)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.audio_out = audio.sink(48000, '', True)
        _amp_enable_check_box = Qt.QCheckBox('TX Amp')
        self._amp_enable_choices = {True: True, False: False}
        self._amp_enable_choices_inv = dict((v,k) for k,v in self._amp_enable_choices.items())
        self._amp_enable_callback = lambda i: Qt.QMetaObject.invokeMethod(_amp_enable_check_box, "setChecked", Qt.Q_ARG("bool", self._amp_enable_choices_inv[i]))
        self._amp_enable_callback(self.amp_enable)
        _amp_enable_check_box.stateChanged.connect(lambda i: self.set_amp_enable(self._amp_enable_choices[bool(i)]))
        self.top_grid_layout.addWidget(_amp_enable_check_box, 0, 5, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(5, 6):
            self.top_grid_layout.setColumnStretch(c, 1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.cx_to_real, 0), (self.audio_waterfall, 0))
        self.connect((self.cx_to_real, 0), (self.interpolator, 0))
        self.connect((self.if_filter, 0), (self.if_waterfall, 0))
        self.connect((self.if_filter, 0), (self.mixer_2, 1))
        self.connect((self.interpolator, 0), (self.volume_mult, 0))
        self.connect((self.mixer_1, 0), (self.if_filter, 0))
        self.connect((self.mixer_2, 0), (self.usb_filter, 0))
        self.connect((self.offset_osc_1, 0), (self.mixer_1, 1))
        self.connect((self.offset_osc_2, 0), (self.mixer_2, 0))
        self.connect((self.rf_in, 0), (self.mixer_1, 0))
        self.connect((self.usb_filter, 0), (self.cx_to_real, 0))
        self.connect((self.volume_mult, 0), (self.audio_out, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "vhf_rx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_cal_freq(self):
        return self.cal_freq

    def set_cal_freq(self, cal_freq):
        self.cal_freq = cal_freq
        self.set_cal_band((self.cal_freq - 100e3) / 1e6)

    def get_cal_band(self):
        return self.cal_band

    def set_cal_band(self, cal_band):
        self.cal_band = cal_band
        self.set_band(self.cal_band)

    def get_tx_text(self):
        return self.tx_text

    def set_tx_text(self, tx_text):
        self.tx_text = tx_text
        Qt.QMetaObject.invokeMethod(self._tx_text_line_edit, "setText", Qt.Q_ARG("QString", str(self.tx_text)))

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain

    def get_tune(self):
        return self.tune

    def set_tune(self, tune):
        self.tune = tune
        self.offset_osc_2.set_frequency(100000 - self.tune * 1000 + 700)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.if_filter.set_taps(firdes.low_pass(1, self.samp_rate, 75000, 25000, firdes.WIN_HAMMING, 6.76))
        self.if_waterfall.set_frequency_range(100000, self.samp_rate / self.decimation)
        self.offset_osc_1.set_sampling_freq(self.samp_rate)
        self.offset_osc_2.set_sampling_freq(self.samp_rate / self.decimation)
        self.rf_in.set_sample_rate(self.samp_rate)
        self.usb_filter.set_taps(firdes.complex_band_pass(1, self.samp_rate / self.decimation, 200, 2800, 200, firdes.WIN_HAMMING, 6.76))

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.offset_osc_1.set_frequency(-self.offset)
        self.rf_in.set_center_freq(self.band * 1e6 + 100000 - self.offset, 0)

    def get_lna_enable(self):
        return self.lna_enable

    def set_lna_enable(self, lna_enable):
        self.lna_enable = lna_enable
        self._lna_enable_callback(self.lna_enable)
        self.rf_in.set_gain(14 if self.lna_enable else 0, 0)

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.rf_in.set_if_gain(self.if_gain, 0)

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.if_waterfall.set_frequency_range(100000, self.samp_rate / self.decimation)
        self.offset_osc_2.set_sampling_freq(self.samp_rate / self.decimation)
        self.usb_filter.set_taps(firdes.complex_band_pass(1, self.samp_rate / self.decimation, 200, 2800, 200, firdes.WIN_HAMMING, 6.76))

    def get_correction(self):
        return self.correction

    def set_correction(self, correction):
        self.correction = correction
        self.rf_in.set_freq_corr(self.correction, 0)

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self.rf_in.set_bb_gain(self.bb_gain, 0)

    def get_band(self):
        return self.band

    def set_band(self, band):
        self.band = band
        self._band_callback(self.band)
        self.rf_in.set_center_freq(self.band * 1e6 + 100000 - self.offset, 0)

    def get_amp_enable(self):
        return self.amp_enable

    def set_amp_enable(self, amp_enable):
        self.amp_enable = amp_enable
        self._amp_enable_callback(self.amp_enable)



def main(top_block_cls=vhf_rx, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
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


if __name__ == '__main__':
    main()
