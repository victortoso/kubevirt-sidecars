# Enable QEMU's ISA-DEBUG

## Step by step

1. Enable Sidecar in [featureGates][]

2. Add the configmap with the script. The *key* and ConfigMap *name* will be used in the next step.

```
kubectl create configmap cm-isa-debug --from-file=script=./onDefineDomain.py
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
                  "name": "cm-isa-debug",
                  "key": "script",
                  "hookPath": "/usr/bin/onDefineDomain"
                }
            }
        ]
```
