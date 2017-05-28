#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Blade Tx
# Generated: Wed Jun  8 20:57:35 2016
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import time


class blade_tx(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Blade Tx")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 4000000
        self.interpolation = interpolation = 80
        self.wpm = wpm = 15
        self.tune = tune = 100
        self.rf_gain = rf_gain = 10
        self.offset = offset = 200000
        self.cw_vector = cw_vector = (1,0,1,0,1,0,1,1,1, 0,0,0, 1,0,1,0,1,0,1,1,1, 0,0,0, 1,0,1,0,1,0,1,1,1, 0,0,0,0,0,0,0, 1,1,1,0,1,0,1, 0,0,0, 1, 0,0,0,0,0,0,0, 1,0,1,0,1,0,1,1,1, 0,0,0, 1, 0,0,0, 1,0,1,0,1,0,1,1,1,0,1,1,1, 0,0,0, 1,0,1, 0,0,0, 1,0,1,1,1,0,1, 0,0,0, 1,0,1,1,1,0,1, 0,0,0,0,0,0,0, 1,1,1, 0,0,0, 1, 0,0,0, 1,0,1,0,1, 0,0,0, 1,1,1, 0,0,0, 1,0,1, 0,0,0, 1,1,1,0,1, 0,0,0, 1,1,1,0,1,1,1,0,1, 0,0,0,0,0,0,0)
        self.correction = correction = 0
        self.bb_gain = bb_gain = -25
        self.band = band = 432
        self.audio_rate = audio_rate = samp_rate / interpolation

        ##################################################
        # Blocks
        ##################################################
        self.resamp = filter.rational_resampler_ccc(
                interpolation=interpolation,
                decimation=1,
                taps=None,
                fractional_bw=None,
        )
        self.out = osmosdr.sink( args="numchan=" + str(1) + " " + "" )
        self.out.set_sample_rate(samp_rate)
        self.out.set_center_freq(band * (1 + correction / 1e6) * 1e6 + 100000 - offset, 0)
        self.out.set_freq_corr(0, 0)
        self.out.set_gain(rf_gain, 0)
        self.out.set_if_gain(0, 0)
        self.out.set_bb_gain(bb_gain, 0)
        self.out.set_antenna("", 0)
        self.out.set_bandwidth(0, 0)
          
        self.offset_osc = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, tune * 1000 + 100000, 0.9, 0)
        self.mixer = blocks.multiply_vcc(1)
        self.cw_vector_source = blocks.vector_source_c(cw_vector, False, 1, [])
        self.cw_repeat = blocks.repeat(gr.sizeof_gr_complex*1, int(1.2 * audio_rate / wpm))
        self.click_filter = filter.single_pole_iir_filter_cc(1e-2, 1)
        self.blocks_add_const_vxx_0 = blocks.add_const_vcc((0.000001, ))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_const_vxx_0, 0), (self.resamp, 0))    
        self.connect((self.click_filter, 0), (self.blocks_add_const_vxx_0, 0))    
        self.connect((self.cw_repeat, 0), (self.click_filter, 0))    
        self.connect((self.cw_vector_source, 0), (self.cw_repeat, 0))    
        self.connect((self.mixer, 0), (self.out, 0))    
        self.connect((self.offset_osc, 0), (self.mixer, 0))    
        self.connect((self.resamp, 0), (self.mixer, 1))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_audio_rate(self.samp_rate / self.interpolation)
        self.out.set_sample_rate(self.samp_rate)
        self.offset_osc.set_sampling_freq(self.samp_rate)

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
        self.out.set_gain(self.rf_gain, 0)

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.out.set_center_freq(self.band * (1 + self.correction / 1e6) * 1e6 + 100000 - self.offset, 0)

    def get_cw_vector(self):
        return self.cw_vector

    def set_cw_vector(self, cw_vector):
        self.cw_vector = cw_vector
        self.cw_vector_source.set_data(self.cw_vector, [])

    def get_correction(self):
        return self.correction

    def set_correction(self, correction):
        self.correction = correction
        self.out.set_center_freq(self.band * (1 + self.correction / 1e6) * 1e6 + 100000 - self.offset, 0)

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self.out.set_bb_gain(self.bb_gain, 0)

    def get_band(self):
        return self.band

    def set_band(self, band):
        self.band = band
        self.out.set_center_freq(self.band * (1 + self.correction / 1e6) * 1e6 + 100000 - self.offset, 0)

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.cw_repeat.set_interpolation(int(1.2 * self.audio_rate / self.wpm))


def main(top_block_cls=blade_tx, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
