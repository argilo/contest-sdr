#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Vhf Rx
# GNU Radio version: 3.10.2.0

from packaging.version import Version as StrictVersion

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
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import soapy
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore



from gnuradio import qtgui

class vhf_rx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Vhf Rx", catch_exceptions=True)
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
        self.cal_freq = cal_freq = 584309441
        self.samp_rate = samp_rate = 2000000
        self.decimation = decimation = 10
        self.cal_band = cal_band = (cal_freq - 100e3) / 1e6
        self.tx_text = tx_text = ''
        self.tx_gain = tx_gain = 20
        self.tune = tune = 100
        self.offset = offset = 200000
        self.lp_taps_rf = lp_taps_rf = firdes.low_pass(1.0, samp_rate, 75000,25000, window.WIN_HAMMING, 6.76)
        self.lp_taps_if = lp_taps_if = firdes.complex_band_pass(1.0, samp_rate / decimation, 200, 2800, 200, window.WIN_HAMMING, 6.76)
        self.lna_enable = lna_enable = False
        self.if_gain = if_gain = 16
        self.correction = correction = 0
        self.bb_gain = bb_gain = 24
        self.band = band = cal_band
        self.amp_enable = amp_enable = False

        ##################################################
        # Blocks
        ##################################################
        self._tune_range = Range(80, 120, 0.01, 100, 200)
        self._tune_win = RangeWidget(self._tune_range, self.set_tune, "Tune (kHz)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._tune_win, 1, 4, 1, 3)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        _lna_enable_check_box = Qt.QCheckBox("LNA")
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
        self._if_gain_win = RangeWidget(self._if_gain_range, self.set_if_gain, "IF gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._if_gain_win, 0, 3, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._correction_range = Range(-20, 20, 0.1, 0, 200)
        self._correction_win = RangeWidget(self._correction_range, self.set_correction, "PPM", "counter", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._correction_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._bb_gain_range = Range(0, 62, 2, 24, 200)
        self._bb_gain_win = RangeWidget(self._bb_gain_range, self.set_bb_gain, "BB gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._bb_gain_win, 0, 4, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 5):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._band_options = [584.209441, 50, 144, 222, 432, 903, 1296, 2304, 3400, 5760]
        # Create the labels list
        self._band_labels = ['Calib.', '50', '144', '222', '432', '903', '1296', '2304', '3400', '5760']
        # Create the combo box
        self._band_tool_bar = Qt.QToolBar(self)
        self._band_tool_bar.addWidget(Qt.QLabel("Band" + ": "))
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
        self._tx_text_tool_bar = Qt.QToolBar(self)
        self._tx_text_tool_bar.addWidget(Qt.QLabel("CW to send" + ": "))
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
        self._tx_gain_win = RangeWidget(self._tx_gain_range, self.set_tx_gain, "TX gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._tx_gain_win, 0, 6, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.soapy_hackrf_source_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_source_0.set_sample_rate(0, samp_rate)
        self.soapy_hackrf_source_0.set_bandwidth(0, 0)
        self.soapy_hackrf_source_0.set_frequency(0, (band * 1e6 + 100000 - offset) * (1 + correction*1e-6))
        self.soapy_hackrf_source_0.set_gain(0, 'AMP', lna_enable)
        self.soapy_hackrf_source_0.set_gain(0, 'LNA', min(max(if_gain, 0.0), 40.0))
        self.soapy_hackrf_source_0.set_gain(0, 'VGA', min(max(bb_gain, 0.0), 62.0))
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            48000, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)

        self.qtgui_time_sink_x_0.disable_legend()

        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 4, 4, 1, 3)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.interpolator = filter.rational_resampler_fff(
                interpolation=6,
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.if_waterfall = qtgui.waterfall_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            100000, #fc
            samp_rate / decimation, #bw
            "", #name
            1, #number of inputs
            None # parent
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

        self._if_waterfall_win = sip.wrapinstance(self.if_waterfall.qwidget(), Qt.QWidget)

        self.top_grid_layout.addWidget(self._if_waterfall_win, 3, 0, 1, 7)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(25, lp_taps_if, -100000 + tune * 1000 - 700, samp_rate / decimation)
        self.freq_xlating_fft_filter_ccc_0 = filter.freq_xlating_fft_filter_ccc(decimation, lp_taps_rf, offset, samp_rate)
        self.freq_xlating_fft_filter_ccc_0.set_nthreads(1)
        self.freq_xlating_fft_filter_ccc_0.declare_sample_delay(0)
        self.cx_to_real = blocks.complex_to_real(1)
        self.audio_waterfall = qtgui.waterfall_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            8000, #bw
            "", #name
            1, #number of inputs
            None # parent
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

        self._audio_waterfall_win = sip.wrapinstance(self.audio_waterfall.qwidget(), Qt.QWidget)

        self.top_grid_layout.addWidget(self._audio_waterfall_win, 4, 0, 1, 4)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.audio_out = audio.sink(48000, '', True)
        _amp_enable_check_box = Qt.QCheckBox("TX Amp")
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
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.if_waterfall, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.cx_to_real, 0))
        self.connect((self.interpolator, 0), (self.volume_mult, 0))
        self.connect((self.soapy_hackrf_source_0, 0), (self.freq_xlating_fft_filter_ccc_0, 0))
        self.connect((self.volume_mult, 0), (self.audio_out, 0))
        self.connect((self.volume_mult, 0), (self.qtgui_time_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "vhf_rx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_cal_freq(self):
        return self.cal_freq

    def set_cal_freq(self, cal_freq):
        self.cal_freq = cal_freq
        self.set_cal_band((self.cal_freq - 100e3) / 1e6)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_lp_taps_if(firdes.complex_band_pass(1.0, self.samp_rate / self.decimation, 200, 2800, 200, window.WIN_HAMMING, 6.76))
        self.set_lp_taps_rf(firdes.low_pass(1.0, self.samp_rate, 75000, 25000, window.WIN_HAMMING, 6.76))
        self.if_waterfall.set_frequency_range(100000, self.samp_rate / self.decimation)
        self.soapy_hackrf_source_0.set_sample_rate(0, self.samp_rate)

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.set_lp_taps_if(firdes.complex_band_pass(1.0, self.samp_rate / self.decimation, 200, 2800, 200, window.WIN_HAMMING, 6.76))
        self.if_waterfall.set_frequency_range(100000, self.samp_rate / self.decimation)

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
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(-100000 + self.tune * 1000 - 700)

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.freq_xlating_fft_filter_ccc_0.set_center_freq(self.offset)
        self.soapy_hackrf_source_0.set_frequency(0, (self.band * 1e6 + 100000 - self.offset) * (1 + self.correction*1e-6))

    def get_lp_taps_rf(self):
        return self.lp_taps_rf

    def set_lp_taps_rf(self, lp_taps_rf):
        self.lp_taps_rf = lp_taps_rf
        self.freq_xlating_fft_filter_ccc_0.set_taps(self.lp_taps_rf)

    def get_lp_taps_if(self):
        return self.lp_taps_if

    def set_lp_taps_if(self, lp_taps_if):
        self.lp_taps_if = lp_taps_if
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.lp_taps_if)

    def get_lna_enable(self):
        return self.lna_enable

    def set_lna_enable(self, lna_enable):
        self.lna_enable = lna_enable
        self._lna_enable_callback(self.lna_enable)
        self.soapy_hackrf_source_0.set_gain(0, 'AMP', self.lna_enable)

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.soapy_hackrf_source_0.set_gain(0, 'LNA', min(max(self.if_gain, 0.0), 40.0))

    def get_correction(self):
        return self.correction

    def set_correction(self, correction):
        self.correction = correction
        self.soapy_hackrf_source_0.set_frequency(0, (self.band * 1e6 + 100000 - self.offset) * (1 + self.correction*1e-6))

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self.soapy_hackrf_source_0.set_gain(0, 'VGA', min(max(self.bb_gain, 0.0), 62.0))

    def get_band(self):
        return self.band

    def set_band(self, band):
        self.band = band
        self._band_callback(self.band)
        self.soapy_hackrf_source_0.set_frequency(0, (self.band * 1e6 + 100000 - self.offset) * (1 + self.correction*1e-6))

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
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
