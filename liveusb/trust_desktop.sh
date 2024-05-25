#!/bin/sh

for f in ~/Desktop/*.desktop
do
  chmod +x "$f"
  gio set -t string "$f" metadata::xfce-exe-checksum "$(sha256sum "$f" | awk '{print $1}')"
done

rm ~/.config/autostart/trust_desktop.desktop ~/trust_desktop.sh
