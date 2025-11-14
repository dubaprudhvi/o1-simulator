from utils.imports import *

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

def read_nodes():

    try:
        while True:
            choice = inquirer.select(
                            message="CONNECT APPLICATION - READ NODES",
                            border=True,
                            choices=[
                                "READ ALL NODES",
                                "FILTER NODE BASED ON NODE-ID",
                                "FILTER NODE BASED ON USERNAME",
                                "FILTER NODE BASED on HOST",
                                Separator(),
                                "BACK",
                                "EXIT",
                            ],
                        ).execute()

            if choice == "READ ALL NODES":
                read_all_nodes()
            elif choice == "FILTER NODE BASED ON NODE-ID":
                read_nodes_based_on_node_id()
            elif choice == "FILTER NODE BASED ON USERNAME":
                read_nodes_based_on_username()
            elif choice == "FILTER NODE BASED on HOST":
                read_nodes_based_on_host()
            elif choice == "FILTER NODE BASED on CONNECTION STATUS":
                read_nodes_based_on_connection_status()
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

def read_all_nodes():
    payload = {
        "data-provider:input": {
            "filter": [],
            "sortorder": [
                {
                    "property": "node-id",
                    "sortorder": "ascending"
                }
            ],
            "pagination": {
                "size": 1000,
                "page": 1
            }
        }
    }
    print_nodes(payload)

def read_nodes_based_on_node_id():
    value = input("Enter the node-id: ").strip()
    read_node_based_on_filter("node-id", value)

def read_nodes_based_on_username():
    value = input("Enter the username: ").strip()
    read_node_based_on_filter("username", value)


def read_nodes_based_on_host():
    value = input("Enter the host: ").strip()
    read_node_based_on_filter("host", value)

def read_nodes_based_on_connection_status():
    value = input("Enter the connection status: ").strip()
    read_node_based_on_filter("status", value)

def read_node_based_on_filter(property: str, value: str):
    payload = {
        "data-provider:input": {
            "filter": [
                {
                    "property": property,
                    "filtervalue": value
                }
            ],
            "sortorder": [],
            "pagination": {
                "size": 1000,
                "page": 1
            }
        }
    }
    print_nodes(payload)

def print_nodes(payload):
    url = f"http://{config['SDNR']['HOST']}:{config['SDNR']['PORT']}/rests/operations/data-provider:read-network-element-connection-list"

    headers = {
        "Content-Type": "application/xml",
        "Authorization": "Basic YWRtaW46YWRtaW4="
    }
    success = True
    try:
        response_1 = requests.post(
            url,
            headers={**headers, 'Content-Type': 'application/json'},
            json=payload,
            timeout=30
        )
        
        if response_1.status_code in [200, 204]:
            print(f"First request success: {response_1.status_code} - {response_1.text}")
            success = True
        else:
            # print(f"First request failed: {response_1.status_code} - {response_1.text}")
            # print(f"First request failed: {response_1.status_code}")
            success = False        
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        success = False
    return success

