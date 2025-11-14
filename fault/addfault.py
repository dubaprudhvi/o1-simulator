from utils.imports import *

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

def add_faults():
    try:
        while True:
            choice = inquirer.select(
                            message="FAULT MANAGEMENT - ADD FAULTS",
                            border=True,
                            choices=[
                                "ADD SINGLE FAULT",
                                "ADD MULTIPLE FAULTS",
                                Separator(),
                                "BACK",
                                "EXIT",
                            ],
                        ).execute()
            
            if choice == "ADD SINGLE FAULT":
                add_single_fault()
            elif choice == "ADD MULTIPLE FAULTS":
                add_multiple_faults()
            elif choice == "BACK":
                break
            elif choice == "EXIT":
                sys.exit()
            else:
                print("Invalid option. please try again")
    except KeyboardInterrupt:
        print( "\nCtrl+C detected. Exiting the program...")
        sys.exit()
    except Exception as e:
        print( f"{e}")


def add_single_fault():
    node_id = f"{config['FAULT']['NODE_ID']}"
    response = make_request(node_id)
    print(f"Node-id {config['FAULT']['NODE_ID']}: response {response}")

def add_multiple_faults():
    print("Enter the range between the number")
    print("Enter start number : ")
    start_number = input()
    print("Enter End number : ")
    end_number = input()
    start_number, end_number = validate_inputs(start_number, end_number)
    num_iterations = 0

    for count in range(start_number, end_number + 1):
        node_id = f"{config['FAULT']['NODE_ID']}-{count}"
        response = make_request(node_id)
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


def make_request(node_id: str):
    url = f"http://{config['SDNR']['HOST']}:{config['SDNR']['PORT']}/rests/operations/devicemanager:push-fault-notification"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic YWRtaW46YWRtaW4="
    }
    payload = {
	    "input": {
	        "node-id": node_id,
	        "counter": f"{config['FAULT']['COUNTER']}",
	        "timestamp": f"{config['FAULT']['TIMESTAMP']}",
	        "object-id": f"{config['FAULT']['OBJECT_ID']}",
	        "problem": f"{config['FAULT']['PROBLEM']}",
	        "severity": f"{config['FAULT']['SEVERITY']}"
	    }
	}
    success = True
    try:
        response = requests.post(
            url,
            headers={**headers, 'Content-Type': 'application/json'},
            json=payload,
            timeout=30
        )  
        if response.status_code in [200, 204]:
            success = True
        else:
            print(f"First request failed: {response.status_code}")
            success = False        
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        success = False
    return success