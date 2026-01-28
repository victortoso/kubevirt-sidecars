#!/usr/bin/env bash
PVC_MOUNT=/var/run/vdi
MODULE_PATH=$PVC_MOUNT/lib64/qemu-kvm
QEMU_MODULE_DIR=$MODULE_PATH /usr/libexec/qemu-kvm $@
