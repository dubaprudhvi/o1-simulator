from utils.imports import *

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

def add_nodes():
    try:
        while True:
            choice = inquirer.select(
                            message="CONNECT APPLICATION - ADD NODES",
                            border=True,
                            choices=[
                                "ADD SINGLE NODE",
                                "ADD MULTIPLE NODES",
                                Separator(),
                                "BACK",
                                "EXIT",
                            ],
                        ).execute()
            if choice == "ADD SINGLE NODE":
                add_single_node()
            elif choice == "ADD MULTIPLE NODES":
                add_multiple_nodes()
            elif choice == "BACK":
                break
            elif choice == "EXIT":
                sys.exit()
            else:
                print("Invalid option. Please try again")
    
    except KeyboardInterrupt:
        print( "\nCtrl+C detected. Exiting the program...")
        sys.exit()
    except Exception as e:
        print( f"{e}")

def add_single_node():
    node_id = f"{config['NETCONF']['SINGLE_NODE_ID']}"
    response = make_request(config, node_id)
    print(f"Node-id {config['NETCONF']['SINGLE_NODE_ID']}: response {response}")

def add_multiple_nodes():
    print("Enter the range between the number")
    print("Enter start number : ")
    start_number = input()
    print("ENter End number : ")
    end_number = input()
    start_number, end_number = validate_inputs(start_number, end_number)
    num_iterations = 0

    for count in range(start_number, end_number + 1):
        node_id = f"{config['NETCONF']['MULTIPLE_NODE_ID']}-{count}"
        response = make_request(config, node_id)
        print(f"Node-id {node_id}: response {response}")
        num_iterations += 1

    print(f"Completed Iterations {num_iterations} times.")

def validate_inputs(start: str, end: str) -> tuple[int, int]:
    """Validate that inputs are positive integers and start <= end."""
    if not (start.isdigit() and end.isdigit()):
        raise ValueError("Both <start_number> and <end_number> must be positive integers.")

    start_number, end_number = int(start), int(end)

    if start_number > end_number:
        raise ValueError("<start_number> must be less than or equal to <end_number>.")

    return start_number, end_number


def make_request(config: dict, node_id: str) -> requests.Response:
    url = f"http://{config['SDNR']['HOST']}:{config['SDNR']['PORT']}/rests/data/network-topology:network-topology/topology=topology-netconf"

    headers = {
        "Content-Type": "application/xml",
        "Authorization": "Basic YWRtaW46YWRtaW4=",
        "Cookie": "JSESSIONID=node01g49jwazciqa0r4cas8j8d6r61437.id.id.id.id.id.node0"
    }

    data = f"""
    <node xmlns="urn:TBD:params:xml:ns:yang:network-topology">
        <node-id>{node_id}</node-id>
        <host xmlns="urn:opendaylight:netconf-node-topology">{config['NETCONF']['HOST']}</host>
        <port xmlns="urn:opendaylight:netconf-node-topology">{config['NETCONF']['PORT']}</port>
        <username xmlns="urn:opendaylight:netconf-node-topology">{config['NETCONF']['USERNAME']}</username>
        <password xmlns="urn:opendaylight:netconf-node-topology">{config['NETCONF']['PASSWORD']}</password>
        <tcp-only xmlns="urn:opendaylight:netconf-node-topology">false</tcp-only>
        <reconnect-on-changed-schema xmlns="urn:opendaylight:netconf-node-topology">false</reconnect-on-changed-schema>
        <connection-timeout-millis xmlns="urn:opendaylight:netconf-node-topology">20000</connection-timeout-millis>
        <max-connection-attempts xmlns="urn:opendaylight:netconf-node-topology">100</max-connection-attempts>
        <between-attempts-timeout-millis xmlns="urn:opendaylight:netconf-node-topology">2000</between-attempts-timeout-millis>
        <sleep-factor xmlns="urn:opendaylight:netconf-node-topology">1.5</sleep-factor>
        <keepalive-delay xmlns="urn:opendaylight:netconf-node-topology">120</keepalive-delay>
    </node>
    """.strip()

    response = requests.post(url, headers=headers, data=data)
    return response
