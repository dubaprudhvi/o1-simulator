import config.model as model
from utils.imports import *

def read_and_update_config(config):
    try:
        while True:
            choice = inquirer.select(
                            message=f"SDNR {config} MANAGEMENT",
                            border=True,
                            choices=[
                                f"View {config} Configuration",
                                f"Edit {config} Configuration",
                                Separator(),
                                "BACK",
                                "EXIT",
                            ],
                        ).execute()
            if choice == f"View {config} Configuration":
                model.view_config(config)
            elif choice == f"Edit {config} Configuration":
                model.edit_config(config)
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