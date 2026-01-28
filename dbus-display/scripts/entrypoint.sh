#!/usr/bin/env bash
set -euo pipefail

SHARE_DIR="/share"
VDI_DIR="/vdi"
CONF_FILE="/data/vdi-dbus-session.conf"
BUS_SOCKET="${VDI_DIR}/bus"
DBUS_ADDR=unix:path=${BUS_SOCKET}
VNC_PORT=15900
RDP_PORT=13389
RDP_ADDR=0.0.0.0:${RDP_PORT}
DEV_CERT=/data/cert.pem
DEV_KEY=/data/key.pem

echo "[entrypoint] starting..."

# 1. Check that /vdi exists
if [[ ! -d "${VDI_DIR}" ]]; then
  echo "[entrypoint][ERROR] ${VDI_DIR} does not exist"
  exit 1
fi

# 2. Start dbus-daemon
dbus-daemon --config-file="${CONF_FILE}" --fork

# sanity check: socket must exist
if [[ ! -S "${BUS_SOCKET}" ]]; then
  echo "[entrypoint][ERROR] dbus socket not created at ${BUS_SOCKET}"
  exit 1
fi
echo "[entrypoint] dbus started at ${BUS_SOCKET}"

# 3. Start qemu-vnc and qemu-rdp in background
(
    # Wait qemu-kvm connect and expose org.QEMU
    sleep 7

    /usr/bin/qemu-vnc -d ${DBUS_ADDR} -p ${VNC_PORT} &
    QEMU_VNC_PID=$!
    echo "[entrypoint] qemu-vnc started (pid=${QEMU_VNC_PID})"

    /usr/bin/qemu-rdp -d ${DBUS_ADDR} serve -b ${RDP_ADDR} \
        --cert=${DEV_CERT} --key=${DEV_KEY} &
    QEMU_RDP_PID=$!
    echo "[entrypoint] qemu-rdp started (pid=${QEMU_RDP_PID})"
) &

# 4. our gRPC handler 
echo "[entrypoint] starting sidecar-shim"
exec /usr/bin/sidecar-shim --version v1alpha3
