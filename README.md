# contest-sdr

Author: Clayton Smith  
Email: <argilo@gmail.com>

The intent of this project is to turn a HackRF (or other SDR board)
into a multi-band transceiver for use in amateur radio contests such as
the ARRL June VHF contest. At present it only supports CW.

At the moment, it depends on patches to hackrf and gr-osmosdr to add
support for transmit/receive switching:

* https://github.com/argilo/hackrf/tree/allow-tr-switching
* https://github.com/argilo/gr-osmosdr/tree/allow-tr-switching

## Usage

Install GNU Radio, and build hackrf and gr-osmosdr using the
"allow-tr-switching" branches indicated above. This can be accomplished
most easily using PyBOMBS.

The main transceiver application is vhf_transceiver.py, which can be
run from the command line. It ties together the receive and transmit
flow graphs (vhf_rx, vhf_tx) which are built with GNU Radio Companion.
The GUI is part of the receive flow graph.

To transmit CW, type your message into the "CW to send" box and press
enter. Once transmission is complete, the box will empty and the
waterfalls will start running again.

## License

Copyright 2015 Clayton Smith

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
