from types import MappingProxyType

def get_fault_description(fault_id):
    faults = fault_id_to_type_mapping()
    return faults.get(fault_id, "Unknown fault ID")

def fault_id_to_type_mapping():
    fault_mapping = {
        1: "Unit temperature is high",
        2: "Unit dangerously overheating",
        3: "Ambient temperature violation",
        4: "Temperature too low",
        5: "Cooling fan broken",
        6: "No fan detected",
        7: "Tuning failure",
        8: "Filter unit faulty",
        9: "Transmission quality deteriorated",
        10: "RF Module overvoltage protection faulty",
        11: "Configuring failed",
        12: "Critical file not found",
        13: "File not found",
        14: "Configuration file corrupted",
        15: "Unit out of order",
        16: "Unit unidentified",
        17: "No external sync source",
        18: "Synchronization Error",
        19: "TX out of order",
        20: "RX out of order",
        21: "Increased BER detected on the optical connection",
        22: "Post test failed",
        23: "FPGA SW update failed",
        24: "Unit blocked",
        25: "Reset Requested",
        26: "Power Supply Faulty",
        27: "Power Amplifier faulty",
        28: "C/U-plane logical Connection faulty",
        29: "Transceiver Fault",
        30: "Transceiver Fault",
        31: "Unexpected C/U-plane message content fault",
        32: "Triggering failure of antenna calibration",
        33: "Dying Gasp"
    }
    return MappingProxyType(fault_mapping)
