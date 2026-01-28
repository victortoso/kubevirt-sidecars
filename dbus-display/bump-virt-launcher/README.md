# What

A virt-launcher image that we install required dependencies for -display dbus to work properly

# Why

The first attempt was to use similar techniques that we used for [debuggability][] but I've found a
linking issue that I could not fix timely. A quicker approach is to simply upgrade virt-launcher
image with required dependencies.

# How

We will use a Containerfile that uses FROM a recent compile image from local development environment
and with proceed to copy and extract the RPMs in the packages folder.

Note, there is a better (easier to maintain) method documented [here][]

# On the virt-launcher image

I'm using [Podman --remote][] to run KubeVirt.

1. Find bazel's registry port

```
# The full line
$ podman ps | grep -i registry | grep -i 5000
9ef8697508fb  quay.io/libpod/registry:2.8.2 ...  0.0.0.0:34963->5000/tcp ...

# The port itself
$ podman ps | grep -i registry | grep -oP '\d+(?=->5000/tcp)'
34963

# Save it for late
$ set -x bzregport $(podman ps | grep -i registry | grep -oP '\d+(?=->5000/tcp)')
```

2. Pull the virt-launcher image

```
$ podman pull docker://0.0.0.0:$bzregport/kubevirt/virt-launcher:devel --tls-verify=false
...
Writing manifest to image destination
4b0241574468

# Tag it for aesthetics (and to work with Containerfile)
podman tag 4b0241574468 kubevirt/virt-launcher:devel
```

3. Build the Container image

```
# build
podman build -t qemu-display/virt-launcher:latest .

# validate it has the .so we want
$ podman run --rm -i --entrypoint="" qemu-display/virt-launcher:latest ls /usr/lib64/qemu-kvm/
audio-dbus.so
hw-display-virtio-gpu-pci.so
hw-display-virtio-gpu.so
hw-display-virtio-vga.so
hw-uefi-vars.so
hw-usb-host.so
hw-usb-redirect.so
ui-dbus.so
ui-opengl.so
```

4. Push the image back to bazel's registry

```
# First we save the image
podman image save --quiet -o qemu-display-virt-launcher.tar localhost/qemu-display/virt-launcher:latest

# Now push it to the registry
skopeo copy docker-archive:qemu-display-virt-launcher.tar docker://0.0.0.0:$bzregport/kubevirt/virt-launcher:devel --tls-verify=false
....
Copying config 7dd45e53bd done   |
Writing manifest to image destination
```

You are all set.

[debuggability]: https://kubevirt.io/user-guide/debug_virt_stack/launch-qemu-strace/
[Podman --remote]: https://github.com/kubevirt/kubevirtci/blob/main/PODMAN.md
[here]: https://github.com/kubevirt/kubevirt/blob/main/docs/custom-rpms.md
