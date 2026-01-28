# Out of Process VNC & RDP server with QEMU's DBus Display

This is currently a WIP.
![▶️ Watch the demo video](demo.gif)

# Design

The main goal is to showcase the viability of running a VNC server out-of-process, in its own
container. A secondary goal is to enable other remote protocols to be integrated with KubeVirt
without bringing specific domain knowledge to KubeVirt and KubeVirt's APIs.

[QEMU DBus display][] fits perfectly for this and it is already mature enough for usage. We will be
using [qemu-display][] for connecting to QEMU's DBus interface and to provide the VNC server access
point.

We'll be deploying a [Sidecar][] for:
- Configuring [libvirt][] over OnDefineDomain call to configure VMI for Display DBus
- Starting a dbus session. This will be shared between the compute and hook containers
- Starting qemu-vnc and qemu-rdp
- Running the sidecar-shim binary for the gRPC communication with virt-launcher

The initial plan was to include also in the Sidecar, the qemu drivers for dbus, namely audio-dbus.so
and ui-dbus.so and all its depencies but I had issues sharing some of those libraries (between
containers) so;

The second option was to install those dependencies to virt-launcher container image.

For the access to the Pod's container, we will use a Service object and port forwarding.

## Requirements

QEMU's DBus Display is present since [QEMU v7.0][] and Libvirt adopted it in [v8.4][] but it
requires QEMU drivers and libvirt configuration in order to function. Also, those binaries are not
part of Centos Stream 9 mirrorlist (or I could not find them?) but we can use the generated RPMs
from the build process, see koji's build for [qemu-kvm-10.1.0-10.el9][]

## Step by step

1. Enable Sidecar in [featureGates][]

2. Build and Push virt-launcher with deps image, [see](bump-virt-launcher/README.md)

3. Build this container image

```
podman build -t qemu-display/vdi-sidecar:latest .
```

4. Push it to bazel's repository

```
# First we have to save it
podman image save --quiet -o qemu-display-vdi-sidecar.tar localhost/qemu-display/vdi-sidecar:latest

# Now do copy it over
skopeo copy docker-archive:qemu-display-vdi-sidecar.tar docker://0.0.0.0:$bzregport/qemu-display/vdi-sidecar:latest --tls-verify=false
```

Now we have both images in the repository.

5. PVC

We are going to use a PVC to mount a shared folder between vdi-sidecar container and virt-launcher
to share the DBus socket.

pvc.yaml:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: simple-pvc
spec:
  storageClassName: local
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

```
$ kubectl apply -f pvc.yaml
```

6. VMI

The annotation needed to launch configure the sidecar.

```yaml
metadata:
  annotations:
    hooks.kubevirt.io/hookSidecars: >
      [
        {
          "image": "registry:5000/qemu-display/vdi-sidecar:latest",
          "pvc":
          {
            "name": "simple-pvc",
            "volumePath": "/vdi",
            "sharedComputePath": "/var/run/vdi"
          }
        }
      ]
```

```
$ kubectl apply -f vmi.yaml
```

7. Verify

# See that libvirt has set everything.
```
$ kubectl exec -it $(k get pods | grep -i launcher | cut -d' ' -f 1) -- virsh dumpxml 1 | grep -i dbus
    <graphics type='dbus' address='unix:path=/var/run/vdi/bus'/>
    <audio id='1' type='dbus'/>
```

8. TODO: Service

[QEMU V7.0]: https://wiki.qemu.org/ChangeLog/7.0#GUI
[v8.4]: https://libvirt.org/news.html#v8-4-0-2022-06-01
[since v0.59 to be exact]: https://github.com/kubevirt/kubevirt/commit/0a7158c31cf4ce869bc0d86919a4d1a25718d030
[featureGates]: https://kubevirt.io/user-guide/cluster_admin/activating_feature_gates
[qemu-kvm-10.1.0-10.el9]: https://kojihub.stream.centos.org/koji/buildinfo?buildID=92750
[QEMU DBus display]: https://www.qemu.org/docs/master/interop/dbus-display.html
[qemu-display]: https://gitlab.com/marcandre.lureau/qemu-display
[Sidecar]: https://kubevirt.io/user-guide/user_workloads/hook-sidecar/#hook-sidecar-container
[libvirt]: https://libvirt.org/formatdomain.html#graphical-framebuffers#graphic
