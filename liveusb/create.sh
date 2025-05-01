#!/usr/bin/env bash

set -e

SERVER_ISO=~/Downloads/ubuntu-24.04.2-live-server-amd64.iso
BASE_DIR=$(dirname -- "$0")
OUT_IMG_UEFI=${BASE_DIR}/contest-sdr-uefi.img
OUT_IMG_BIOS=${BASE_DIR}/contest-sdr-bios.img
HTTP_PORT=3003

# Find an Open Virtual Machine Firmware file only if none was specified via the
# environment variable
check_for_ovmf_file() {
    # Ensure that the chosen file actually exists
    if [ ! -z "${1}" -a -f "${1}" ]; then
        OVMF_FILE="${1}"
    fi
}
if [ -z "${OVMF_FILE}" ]; then
    # It would be pretty rare for your system to have more than one of these
    check_for_ovmf_file /usr/share/edk2/x64/OVMF.4m.fd  # Arch-based?
    check_for_ovmf_file /usr/share/ovmf/OVMF.fd         # Debian-based?
fi

sudo mount -r ${SERVER_ISO} /mnt
python3 -m http.server -d ${BASE_DIR} ${HTTP_PORT} &
HTTP_SERVER_PID=$!
qemu-img create ${OUT_IMG_UEFI} 14G
qemu-system-x86_64 \
    -enable-kvm \
    -no-reboot \
    -m 2048 \
    -smp 4 \
    -bios ${OVMF_FILE} \
    -drive file=${OUT_IMG_UEFI},format=raw,cache=none,if=virtio \
    -cdrom ${SERVER_ISO} \
    -kernel /mnt/casper/vmlinuz \
    -initrd /mnt/casper/initrd \
    -append "ipv6.disable=1 autoinstall ds=nocloud-net;s=http://_gateway:${HTTP_PORT}/"
qemu-img create ${OUT_IMG_BIOS} 14G
qemu-system-x86_64 \
    -enable-kvm \
    -no-reboot \
    -m 2048 \
    -smp 4 \
    -drive file=${OUT_IMG_BIOS},format=raw,cache=none,if=virtio \
    -cdrom ${SERVER_ISO} \
    -kernel /mnt/casper/vmlinuz \
    -initrd /mnt/casper/initrd \
    -append "ipv6.disable=1 autoinstall ds=nocloud-net;s=http://_gateway:${HTTP_PORT}/"
sudo umount /mnt
kill ${HTTP_SERVER_PID}
