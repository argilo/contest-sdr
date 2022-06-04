# contest-sdr

Author: Clayton Smith  
Email: <argilo@gmail.com>

The intent of this project is to turn a HackRF (or other SDR board)
into a multi-band transceiver for use in amateur radio contests such as
the ARRL June VHF contest. At present it only supports CW.

## Usage

Install GNU Radio 3.10 or later.

The main transceiver application is vhf_transceiver.py, which can be
run from the command line. It ties together the receive and transmit
flow graphs (vhf_rx, vhf_tx) which are built with GNU Radio Companion.
The GUI is part of the receive flow graph.

To transmit CW, type your message into the "CW to send" box and press
enter. Once transmission is complete, the box will empty and the
waterfalls will start running again.

## Building a bootable USB flash drive

On an Ubuntu system:

* Download https://releases.ubuntu.com/22.04/ubuntu-22.04-live-server-amd64.iso
  and place it in `~/Downloads/`
* Install the qemu-system-x86 package: `sudo apt install qemu-system-x86`
* Generate the Live USB image: `liveusb/create.sh`
* Write the image to a flash drive (16 GB or larger): `sudo dd if=liveusb/disk.img of=/dev/sdb bs=4M`

Boot from the flash drive and double click the "Contest SDR" icon on the
desktop.

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
