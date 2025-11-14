from utils.imports import *
import xmlfiles.generatekpixml as generatekpixml 

def kpi_xml_menu():
    try:
        while True:
            choice = inquirer.select(
                            message="GENERATAE XML Files",
                            border=True,
                            choices=[
                                "GENERATE XML FILES BASED ON INTERVAL",
                                Separator(),
                                "BACK",
                                "EXIT",
                            ],
                        ).execute()
            
            if choice == "GENERATE XML FILES BASED ON INTERVAL":
                generatekpixml.generate_kpi_xml_files()
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


