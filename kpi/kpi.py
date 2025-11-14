import kpi.veskpi as veskpi
import kpi.hvveskpi as hvveskpi
from utils.imports import *

def kpi_menu():
    try:
        while True:
            choice = inquirer.select(
                            message="ADD KPI's",
                            border=True,
                            choices=[
                                "VES KPI'S",
                                "HV-VES KPI'S",
                                Separator(),
                                "BACK",
                                "EXIT",
                            ],
                        ).execute()
            
            if choice == "VES KPI'S":
                veskpi.ves_kpi_menu()
            elif choice == "HV-VES KPI'S":
                hvveskpi.hv_ves_kpi_menu()
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


