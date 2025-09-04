# Enable QEMU's VNC clipboard capability

## Requirements

The clipboard protocol exists in VNC and this Sidecar will enable it in the
virtualization stack. It still requires a supported client and spice-vdagent
installed and running in the guest.

## Step by step

1. Enable Sidecar featureGates

2. Add the configmap with the script. The *key* and ConfigMap *name* will be used in the next step.

```
kubectl create configmap cm-vnc-clipboard --from-file=script=./onDefineDomain.py
```

3. Add the following annotation to your VMI

```yaml
metadata:
  annotations:
      hooks.kubevirt.io/hookSidecars: >
        [
            {
                "args": ["--version", "v1alpha3"],
                "configMap": {
                  "name": "cm-vnc-clipboard",
                  "key": "script",
                  "hookPath": "/usr/bin/onDefineDomain"
                }
            }
        ]
```

# Related

- Support NoVNC clipboard copy paste feature [#10306][]
- Add support for Clipboard in VNC [#10971][]

[#10306]: https://github.com/kubevirt/kubevirt/issues/10306
[#10971]: https://github.com/kubevirt/kubevirt/pull/10971
