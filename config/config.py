from utils.imports import *
import config.readandupdateconfig as readandupdateconfig

def config_menu():
    try:
        while True:
            choice = inquirer.select(
                            message="CONFIGURATION MENU",
                            border=True,
                            choices=[
                                "SDNR CONFIGS",
                                "NETCONF CONFIGS",
                                "FAULT CONFIGS",
                                "VES CONFIGS",
                                "VES INFLUX CONFIGS",
                                "HV-VES INFLUX CONFIGS",
                                Separator(),
#                                "BACK",
                                "EXIT",
                            ],
                        ).execute()
            if choice == "SDNR CONFIGS":
                readandupdateconfig.read_and_update_config("SDNR")
            elif choice == "NETCONF CONFIGS":
                readandupdateconfig.read_and_update_config("NETCONF")
            elif choice == "FAULT CONFIGS":
                readandupdateconfig.read_and_update_config("FAULT")
            elif choice == "VES CONFIGS":
                readandupdateconfig.read_and_update_config("VES")
            elif choice == "VES INFLUX CONFIGS":
                readandupdateconfig.read_and_update_config("VESINFLUX")
            elif choice == "HV-VES INFLUX CONFIGS":
                readandupdateconfig.read_and_update_config("HVVESINFLUX")
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
