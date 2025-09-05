# Set fixed display for VNC

## Step by step

1. Enable Sidecar in [featureGates][]

2. Add the configmap with the script. The *key* and ConfigMap *name* will be used in the next step.

```
kubectl create configmap cm-vnc-fixed-resolution --from-file=script=./onDefineDomain.py
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
                  "name": "cm-vnc-fixed-resolution",
                  "key": "script",
                  "hookPath": "/usr/bin/onDefineDomain"
                }
            }
        ]
```

# Related

- Allow to set a fixed screen resolution [CNV-63749][]

[featureGates]: https://kubevirt.io/user-guide/cluster_admin/activating_feature_gates
[CNV-63749]: https://issues.redhat.com/browse/CNV-63749
