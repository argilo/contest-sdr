#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Vhf Tx
# GNU Radio version: 3.10.2.0

from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy




class vhf_tx(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Vhf Tx", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 4000000
        self.interpolation = interpolation = 80
        self.wpm = wpm = 15
        self.tune = tune = 100
        self.rf_gain = rf_gain = False
        self.offset = offset = 200000
        self.if_gain = if_gain = 20
        self.cw_vector = cw_vector = (1,0,1,0,1,0,1,1,1, 0,0,0, 1,0,1,0,1,0,1,1,1, 0,0,0, 1,0,1,0,1,0,1,1,1, 0,0,0,0,0,0,0, 1,1,1,0,1,0,1, 0,0,0, 1, 0,0,0,0,0,0,0, 1,0,1,0,1,0,1,1,1, 0,0,0, 1, 0,0,0, 1,0,1,0,1,0,1,1,1,0,1,1,1, 0,0,0, 1,0,1, 0,0,0, 1,0,1,1,1,0,1, 0,0,0, 1,0,1,1,1,0,1, 0,0,0,0,0,0,0, 1,1,1, 0,0,0, 1, 0,0,0, 1,0,1,0,1, 0,0,0, 1,1,1, 0,0,0, 1,0,1, 0,0,0, 1,1,1,0,1, 0,0,0, 1,1,1,0,1,1,1,0,1, 0,0,0,0,0,0,0)
        self.correction = correction = 0
        self.band = band = 432
        self.audio_rate = audio_rate = samp_rate / interpolation

        ##################################################
        # Blocks
        ##################################################
        self.soapy_hackrf_sink_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_sink_0 = soapy.sink(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_sink_0.set_sample_rate(0, samp_rate)
        self.soapy_hackrf_sink_0.set_bandwidth(0, 0)
        self.soapy_hackrf_sink_0.set_frequency(0, band * 1e6 + 100000 - offset)
        self.soapy_hackrf_sink_0.set_gain(0, 'AMP', rf_gain)
        self.soapy_hackrf_sink_0.set_gain(0, 'VGA', min(max(if_gain, 0.0), 47.0))
        self.resamp = filter.rational_resampler_ccc(
                interpolation=interpolation,
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.offset_osc = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, tune * 1000 + 100000, 0.9, 0, 0)
        self.mixer = blocks.multiply_vcc(1)
        self.cw_vector_source = blocks.vector_source_c(cw_vector, False, 1, [])
        self.cw_repeat = blocks.repeat(gr.sizeof_gr_complex*1, int(1.2 * audio_rate / wpm))
        self.click_filter = filter.single_pole_iir_filter_cc(1e-2, 1)
        self.blocks_add_const_vxx_0 = blocks.add_const_cc(0.000001)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_const_vxx_0, 0), (self.resamp, 0))
        self.connect((self.click_filter, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.cw_repeat, 0), (self.click_filter, 0))
        self.connect((self.cw_vector_source, 0), (self.cw_repeat, 0))
        self.connect((self.mixer, 0), (self.soapy_hackrf_sink_0, 0))
        self.connect((self.offset_osc, 0), (self.mixer, 0))
        self.connect((self.resamp, 0), (self.mixer, 1))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_audio_rate(self.samp_rate / self.interpolation)
        self.offset_osc.set_sampling_freq(self.samp_rate)
        self.soapy_hackrf_sink_0.set_sample_rate(0, self.samp_rate)

    def get_interpolation(self):
        return self.interpolation

    def set_interpolation(self, interpolation):
        self.interpolation = interpolation
        self.set_audio_rate(self.samp_rate / self.interpolation)

    def get_wpm(self):
        return self.wpm

    def set_wpm(self, wpm):
        self.wpm = wpm
        self.cw_repeat.set_interpolation(int(1.2 * self.audio_rate / self.wpm))

    def get_tune(self):
        return self.tune

    def set_tune(self, tune):
        self.tune = tune
        self.offset_osc.set_frequency(self.tune * 1000 + 100000)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.soapy_hackrf_sink_0.set_gain(0, 'AMP', self.rf_gain)

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.soapy_hackrf_sink_0.set_frequency(0, self.band * 1e6 + 100000 - self.offset)

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.soapy_hackrf_sink_0.set_gain(0, 'VGA', min(max(self.if_gain, 0.0), 47.0))

    def get_cw_vector(self):
        return self.cw_vector

    def set_cw_vector(self, cw_vector):
        self.cw_vector = cw_vector
        self.cw_vector_source.set_data(self.cw_vector, [])

    def get_correction(self):
        return self.correction

    def set_correction(self, correction):
        self.correction = correction

    def get_band(self):
        return self.band

    def set_band(self, band):
        self.band = band
        self.soapy_hackrf_sink_0.set_frequency(0, self.band * 1e6 + 100000 - self.offset)

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.cw_repeat.set_interpolation(int(1.2 * self.audio_rate / self.wpm))




def main(top_block_cls=vhf_tx, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
