# contest-sdr

Author: Clayton Smith  
Email: <argilo@gmail.com>

The intent of this project is to turn a transmit-capable SDR board (HackRF,
BladeRF, PlutoSDR, USRP, or LimeSDR) into a multi-band transceiver for use in
amateur radio contests such as the ARRL June VHF contest. At present it only
supports CW.

## Usage

Install GNU Radio 3.10 or later. Make sure that SoapySDR support is included,
and the SoapySDR driver for your target device is installed. On Ubuntu 22.04,
simply run `sudo apt install gnuradio` to get an appropriate version of GNU
Radio, SoapySDR and drivers.

Run one of the following commands from the command line:

* `./b200_transceiver.py` — USRP B200
* `./blade_transceiver.py` — BladeRF
* `./hackrf_transceiver.py` — HackRF
* `./lime_transceiver.py` — LimeSDR
* `./pluto_transceiver.py` — PlutoSDR

Each of these scripts ties together the corresponding `<device>_rx` (receive)
and `<device>_tx` (transmit) flow graphs, which are built with GNU Radio
Companion. The GUI is part of the receive flow graph.

When the application starts it will be in calibration mode, which uses the
pilot tone of ATSC channel 33 (584.309441 MHz) to help adjust the PPM
correction value. Adjust the PPM setting up or down until the pilot signal is
at 100 kHz in the upper (IF) waterfall, and at 700 Hz in the lower (audio)
waterfall.

Next, select the band you would like to transmit on. Adjust the receive and
transmit gains as desired. The audio scope (lower right) shows the received
audio signal. If clipping occurs, reduce the receive gain.

To transmit CW, type your message into the "CW to send" box and press
enter. Once transmission is complete, the box will empty and the receive
waterfalls will start running again.

## Building a bootable USB flash drive

On an Ubuntu system:

* Download https://releases.ubuntu.com/22.04/ubuntu-22.04-live-server-amd64.iso
  and place it in `~/Downloads/`
* Install the qemu-system-x86 package: `sudo apt install qemu-system-x86`
* Generate the live USB image: `liveusb/create.sh`
* At the prompt, enter your password to allow the Ubuntu ISO to be mounted
* Write the image to a flash drive (16 GB or larger): `sudo dd if=liveusb/disk.img of=/dev/sdb bs=4M conv=fsync`

Boot from the flash drive and double click the "Contest SDR" icon on the
desktop corresponding to your SDR device.

## License

Copyright 2015-2022 Clayton Smith

This file is part of contest-sdr

contest-sdr is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3, or (at your option)
any later version.

contest-sdr is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with contest-sdr; see the file COPYING.  If not, write to
the Free Software Foundation, Inc., 51 Franklin Street,
Boston, MA 02110-1301, USA.
