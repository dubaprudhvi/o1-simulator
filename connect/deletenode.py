from utils.imports import *

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

def delete_nodes():
    try:
        while True:
            choice = inquirer.select(
                            message="CONNECT APPLICATION - DELETE NODES",
                            border=True,
                            choices=[
                                "DELETE SINGLE NODE",
                                "DELETE MULTIPLE NODES",
                                Separator(),
                                "BACK",
                                "EXIT",
                            ],
                        ).execute()
            if choice == "DELETE SINGLE NODE":
                delete_single_node()
            elif choice == "DELETE MULTIPLE NODES":
                delete_multiple_nodes()
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

def delete_single_node():
    node_id = f"{config['NETCONF']['SINGLE_NODE_ID']}"
    response = make_request(config, node_id)
    print(f"Node-id {config['NETCONF']['SINGLE_NODE_ID']}: response {response}")

def delete_multiple_nodes():
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

def make_request(config: dict, node_id: str):
    url = f"http://{config['SDNR']['HOST']}:{config['SDNR']['PORT']}/rests/operations/data-provider:delete-network-element-connection"

    headers = {
        "Content-Type": "application/xml",
        "Authorization": "Basic YWRtaW46YWRtaW4="
    }
    payload = {
        "data-provider:input": {
            "id": node_id
        }
    }
    success = True
    try:
        response_1 = requests.post(
            url,
            headers={**headers, 'Content-Type': 'application/json'},
            json=payload,
            timeout=30
        )
        
        if response_1.status_code not in [200, 204]:
            # print(f"First request failed: {response_1.status_code} - {response_1.text}")
            print(f"First request failed: {response_1.status_code}")
            success = False        
        url_2 = f"http://{config['SDNR']['HOST']}:{config['SDNR']['PORT']}/rests/data/network-topology:network-topology/topology=topology-netconf/node={node_id}"
        response_2 = requests.delete(
            url_2,
            headers=headers,
            timeout=30
        )
        if response_2.status_code not in [200, 204]:
            # print(f"Second request failed: {response_2.status_code} - {response_2.text}")
            print(f"Second request failed: {response_2.status_code}")
            success = False 
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        success = False
    return success

