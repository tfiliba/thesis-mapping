# Copyright (c) 2012, Terry Filiba
# All rights reserved.
# 
# This file is part of ORCAS.
# 
# ORCAS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# ORCAS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with ORCAS.  If not, see <http://www.gnu.org/licenses/>.

#from pulp import *
#import numpy
from instrument import Instrument
from cblock import CBlock
from platform import Platform
        
        
class Spectrometer(Instrument):
    def __init__(self, numchannels, accumulation_length, bandwidth, input_bitwidth, fft_out_bitwidth, antennas=1):
        self.maxdesigns = 1
        self.blocks = {}
        self.totalblocks = 0
        
        #add the platform array
        self.platforms = {}
        
        # add platforms: cost, inputbw, outputbw, resources
        self.platforms['ROACH'] = Platform.createRoach('dollars')
        self.platforms['GTX580'] = Platform.createGTX580Server('dollars')
        #self.platforms['IBOB'] = Platform('IBOB',2000,10,1,['resources'])

        # add the ADC
        adc_bw = bandwidth*input_bitwidth
        self.blocks['ADC'] = CBlock('ADC',CBlock.getADCModel(self.platforms, bandwidth, input_bitwidth),-1,0,0,'PFB',0,adc_bw,antennas)
        self.totalblocks += antennas

        # add the PFB
        pfb_bw = bandwidth*32
        self.blocks['PFB'] = CBlock('PFB',CBlock.getPFBModel(self.platforms, bandwidth, input_bitwidth, numchannels),'ADC',0,pfb_bw,'FFT',0,adc_bw,antennas)
        self.totalblocks += antennas

        # add the FFT
        fft_out_bandwidth = bandwidth* fft_out_bitwidth
        self.blocks['FFT'] = CBlock('FFT',CBlock.getFFTModel(self.platforms, bandwidth, numchannels),'PFB',0,pfb_bw,'VAcc',0,fft_out_bandwidth,antennas)
        self.totalblocks += antennas

        #add the Vacc
        self.blocks['VAcc'] = CBlock('VAcc',CBlock.getVAccModel(self.platforms, bandwidth, fft_out_bitwidth, accumulation_length),'FFT',0,fft_out_bandwidth,-1,0,0,antennas)
        self.totalblocks += antennas

        
        
        
        


    
    