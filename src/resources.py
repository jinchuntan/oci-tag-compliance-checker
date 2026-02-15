import oci


def get_instances(config, signer, compartment_id: str):
    compute = oci.core.ComputeClient(config, signer=signer)
    items = compute.list_instances(compartment_id=compartment_id).data

    out = []
    for i in items:
        out.append({
            "type": "compute_instance",
            "name": i.display_name,
            "ocid": i.id,
            "tags": i.freeform_tags or {},
        })
    return out


def get_vcns_and_subnets(config, signer, compartment_id: str):
    vcn = oci.core.VirtualNetworkClient(config, signer=signer)
    vcns = vcn.list_vcns(compartment_id=compartment_id).data

    out = []
    for v in vcns:
        out.append({
            "type": "vcn",
            "name": v.display_name,
            "ocid": v.id,
            "tags": v.freeform_tags or {},
        })

        subs = vcn.list_subnets(compartment_id=compartment_id, vcn_id=v.id).data
        for s in subs:
            out.append({
                "type": "subnet",
                "name": s.display_name,
                "ocid": s.id,
                "tags": s.freeform_tags or {},
                "vcn": v.display_name,
            })
    return out
