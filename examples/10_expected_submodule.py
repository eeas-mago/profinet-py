#!/usr/bin/env python3
"""Build ExpectedSubmoduleBlockReq for device configuration."""

from profinet import ExpectedSubmoduleBlockReq

# One builder per slot (slot 0 = DAP/interface/ports, slot 1 = I/O module)
builders = {}


def builder_for(slot: int) -> ExpectedSubmoduleBlockReq:
    if slot not in builders:
        builders[slot] = ExpectedSubmoduleBlockReq()
    return builders[slot]


# Add DAP (Device Access Point)
builder_for(0).add_submodule(
    api=0,
    slot=0,
    subslot=0x0001,  # DAP
    module_ident=0x00000001,
    submodule_ident=0x00000001,
    submodule_type=0,  # NO_IO
)

# Add interface submodule
builder_for(0).add_submodule(
    api=0,
    slot=0,
    subslot=0x8000,  # Interface
    module_ident=0x00000001,
    submodule_ident=0x00008000,
    submodule_type=0,  # NO_IO
)

# Add port submodules
for port_num in range(1, 3):
    builder_for(0).add_submodule(
        api=0,
        slot=0,
        subslot=0x8000 + port_num,  # Port 1, 2
        module_ident=0x00000001,
        submodule_ident=0x00008000 + port_num,
        submodule_type=0,  # NO_IO
    )

# Add I/O module with input data
builder_for(1).add_submodule(
    api=0,
    slot=1,
    subslot=0x0001,
    module_ident=0x00001234,
    submodule_ident=0x00005678,
    submodule_type=1,  # INPUT
    input_length=16,
)

# Build the blocks (one per slot), concatenated as in a Connect request
block_data = b"".join(b.to_bytes() for b in builders.values())
print(f"ExpectedSubmoduleBlockReq blocks: {len(builders)} slots, {len(block_data)} bytes total")
for slot, builder in builders.items():
    print(f"  Slot {slot}:")
    for api in builder.apis:
        print(f"    API {api.api}:")
        for sub in api.submodules:
            print(f"      Subslot 0x{sub.subslot_number:04X}, Type {sub.submodule_type}")
