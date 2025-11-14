import connect.addnode as addnode
import connect.deletenode as deletenode
import connect.readnode as readnode
from utils.imports import *

def connect_app_menu():
    try:
        while True:
            choice = inquirer.select(
                            message="CONNECT APPLICATION",
                            border=True,
                            choices=[
                                "ADD NODE",
                                "DELETE NODE",
                                "READ NODE",
                                Separator(),
                                "BACK",
                                "EXIT",
                            ],
                        ).execute()
            if choice == "ADD NODE":
                addnode.add_nodes()
            elif choice == "DELETE NODE":
                deletenode.delete_nodes()
            elif choice == "READ NODE":
                readnode.read_nodes()
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

    

