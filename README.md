# Sidecars

Those are custom configurations we can apply to libvirt in KubeVirt. It is useful to test or tweak
behavior that is not supported.

## Feature Gate

The Sidecar feature is gated in KubeVirt. It is a requirement to enable it for any of this to work.

If you are running Openshift, you can `oc annotate` a config patch.

```
    oc annotate --overwrite -n openshift-cnv hco kubevirt-hyperconverged \
        kubevirt.kubevirt.io/jsonpatch='[{"op": "add", "path": "/spec/configuration /developerConfiguration/featureGates/-", "value": "Sidecar" }]'
```


## VM and VMI annotation

Most of my examples uses VMI annotation for the hookSidecar configuration but it is also possible to
edit the VM kind instead, a simple example:

```yaml
    apiVersion: kubevirt.io/v1
    kind: VirtualMachine
    spec:
      template:
        metadata:
          annotations:
            hooks.kubevirt.io/hookSidecars: >
              [
                {
                  "args": ["--version", "v1alpha3"],
                  "configMap": {
                    "name": "fixed-resolution-cm",
                    "key": "my_script.sh",
                    "hookPath": "/usr/bin/onDefineDomain"}
                }
              ]
```
