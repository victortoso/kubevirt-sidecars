# Set fixed display for VNC

## Step by step

1. Enable Sidecar in [featureGates][]

2. Add the configmap with the script. The *key* and ConfigMap *name* will be used in the next step.

```
kubectl create configmap cm-dual-display --from-file=script=./onDefineDomain.py
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
                  "name": "cm-dual-display",
                  "key": "script",
                  "hookPath": "/usr/bin/onDefineDomain"
                }
            }
        ]
```

# Related

- Allow having multi display configuration on Windows (multihead) [CNV-59656][]

[featureGates]: https://kubevirt.io/user-guide/cluster_admin/activating_feature_gates
[CNV-59656]: https://issues.redhat.com/browse/CNV-59656
