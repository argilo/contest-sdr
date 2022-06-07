#!/usr/bin/env bash

set -e

SERVER_ISO=~/Downloads/ubuntu-22.04-live-server-amd64.iso
BASE_DIR=$(dirname -- "$0")
OUT_IMG=${BASE_DIR}/disk.img
HTTP_PORT=3003

sudo mount -r ${SERVER_ISO} /mnt
python3 -m http.server -d ${BASE_DIR} ${HTTP_PORT} &
HTTP_SERVER_PID=$!
qemu-img create ${OUT_IMG} 12G
qemu-system-x86_64 \
    -enable-kvm \
    -no-reboot \
    -m 2048 \
    -smp 2 \
    -drive file=${OUT_IMG},format=raw,cache=none,if=virtio \
    -cdrom ${SERVER_ISO} \
    -kernel /mnt/casper/vmlinuz \
    -initrd /mnt/casper/initrd \
    -append "ipv6.disable=1 autoinstall ds=nocloud-net;s=http://_gateway:${HTTP_PORT}/"
sudo umount /mnt
kill ${HTTP_SERVER_PID}
