#!/usr/bin/env bash

set -e

SERVER_ISO=~/Downloads/ubuntu-22.04.2-live-server-amd64.iso
BASE_DIR=$(dirname -- "$0")
OUT_IMG_UEFI=${BASE_DIR}/contest-sdr-uefi.img
OUT_IMG_BIOS=${BASE_DIR}/contest-sdr-bios.img
HTTP_PORT=3003

sudo mount -r ${SERVER_ISO} /mnt
python3 -m http.server -d ${BASE_DIR} ${HTTP_PORT} &
HTTP_SERVER_PID=$!
qemu-img create ${OUT_IMG_UEFI} 15G
qemu-system-x86_64 \
    -enable-kvm \
    -no-reboot \
    -m 2048 \
    -smp 2 \
    -bios /usr/share/ovmf/OVMF.fd \
    -drive file=${OUT_IMG_UEFI},format=raw,cache=none,if=virtio \
    -cdrom ${SERVER_ISO} \
    -kernel /mnt/casper/vmlinuz \
    -initrd /mnt/casper/initrd \
    -append "ipv6.disable=1 autoinstall ds=nocloud-net;s=http://_gateway:${HTTP_PORT}/"
qemu-img create ${OUT_IMG_BIOS} 15G
qemu-system-x86_64 \
    -enable-kvm \
    -no-reboot \
    -m 2048 \
    -smp 2 \
    -drive file=${OUT_IMG_BIOS},format=raw,cache=none,if=virtio \
    -cdrom ${SERVER_ISO} \
    -kernel /mnt/casper/vmlinuz \
    -initrd /mnt/casper/initrd \
    -append "ipv6.disable=1 autoinstall ds=nocloud-net;s=http://_gateway:${HTTP_PORT}/"
sudo umount /mnt
kill ${HTTP_SERVER_PID}
