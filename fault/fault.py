import fault.addfault as addfault
import fault.deletefault as deletefault
import fault.readfault as readfault
from utils.imports import *

def fault_app_menu():
    try:
        while True:
            choice = inquirer.select(
                            message="FAULT MANAGEMENT",
                            border=True,
                            choices=[
                                "ADD FAULTS",
                                "DELETE FAULTS",
                                "READ FAULTS",
                                Separator(),
                                "BACK",
                                "EXIT",
                            ],
                        ).execute()
            if choice == "ADD FAULTS":
                addfault.add_faults()
            elif choice == "DELETE FAULTS":
                deletefault.delete_faults()
            elif choice == "READ FAULTS":
                readfault.read_faults()
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

