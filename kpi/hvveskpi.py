from utils.imports import *

def hv_ves_kpi_menu():
    try:
        while True:
            choice = inquirer.select(
                            message="HV-VES KPI'S",
                            border=True,
                            choices=[
                                "ADD HV_VES KPI'S BASED ON TIME INTERVAL",
                                "ADD HV_VES KPI'S BASED ON TIME RANGE",
                                Separator(),
                                "BACK",
                                "EXIT",
                            ],
                        ).execute()
            if choice == "ADD HV_VES KPI'S BASED ON TIME INTERVAL":
                while True:
                    limit = input("Enter the interval range in seconds (1-10): ")
                    validated_limit = validate_number(limit, 1, 10)
                    if validated_limit is not None:
                        print()
                        insert_hv_ves_kpi_based_on_interval(validated_limit)
                        break
            elif choice == "ADD HV_VES KPI'S BASED ON TIME RANGE":
                while True:
                    limit = input("Enter the number of iterations (1-100): ")
                    validated_limit = validate_number(limit, 1, 100)
                    if validated_limit is not None:
                        print()
                        insert_hv_ves_kpi_based_on_limit(validated_limit)
                        break
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

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)
            
def validate_number(input_str, min_value, max_value, value_type=int):
    try:
        value = value_type(input_str)
        if min_value <= value <= max_value:
            return value
        else:
            print(f"\nValue must be between {min_value} and {max_value}. Please try again.")
            return None
    except ValueError:
        print(f"\nInvalid input. Please enter a valid {value_type.__name__}.")
        return None


def insert_hv_ves_kpi_based_on_interval(interval):
    print("Loop started. Type 'exit' and press Enter to stop.")
    while True:
        insert_hv_ves_kpi()
        if select.select([sys.stdin], [], [], 0.1)[0]:
            user_input = sys.stdin.readline().strip().lower()
            if user_input in ['exit', 'quit', 'stop', 'q']:
                print("Stopping loop...")
                break
        time.sleep(interval)

def insert_hv_ves_kpi_based_on_limit(limit):
    for _ in range(limit):
        insert_hv_ves_kpi()

KPINAMES = ["RRC.ConnMean", "RRC.ConnMax", "RRC.InactiveConnMean", "RRC.InactiveConnMax", "UECNTX.RelCmd.sum", "QF.EstabAttNbr.sum", "QF.EstabSuccNbr.sum", "QF.EstabFailNbr.sum",  "MM.HoPrepInterReq",  "MM.HoResAlloInterReq",  "MM.HoExeInterReq", "MM.HoPrepInterSucc", "MM.HoResAlloInterSucc", "MM.HoExeInterSucc", "MM.HoPrepIntraReq", "MM.HoExeIntraReq", "MM.HoPrepIntraSucc", "MM.HoExeIntraSucc", "RRU.PrbTotDl", "RRU.PrbAvailDl", "RRU.PrbTotUl", "RRU.PrbAvailUl", "RRU.PrbUsedDl",  "RRU.PrbUsedUl", "TB.TotNbrDlInitial", "TB.TotNbrUlInit", "TB.IntialErrNbrDl", "TB.ErrNbrUlInitial", "TB.ResidualErrNbrDl", "TB.ResidualErrNbrUl", "TB.TotNbrUlInit.Qpsk", "TB.IntialErrNbrDl.Qpsk", "TB.ErrNbrUlInitial.Qpsk", "TB.TotNbrDlInitial.16Qam", "TB.TotNbrUlInit.16Qam", "TB.IntialErrNbrDl.16Qam", "TB.ErrNbrUlInitial.16Qam", "TB.TotNbrDlInitial.64Qam", "TB.TotNbrUlInit.64Qam", "TB.TotNbrUlInit.64Qam", "TB.IntialErrNbrDl.64Qam", "TB.ErrNbrUlInitial.64Qam", "TB.TotNbrDlInitial.256Qam", "TB.TotNbrUlInit.256Qam", "DRB.UEThpDl", "DRB.UEUnresVolDl", "DRB.PeakVolDl", "DRB.PeakTimeDl", "DRB.UEThpUl", "DRB.UEUnresVolUl", "DRB.PeakVolUl", "DRB.PeakTimeUl", "DRB.AirIfDelayDl", "DRB.AirIfDelayUl", "RRC.ConnEstabAtt.0",  "RRC.ConnEstabSucc.0",  "RRC.ConnEstabAtt.1",  "RRC.ConnEstabSucc.1", "RRC.ConnEstabAtt.2", "RRC.ConnEstabSucc.2", "RRC.ConnEstabAtt.3", "RRC.ConnEstabSucc.3", "RRC.ConnEstabAtt.4", "RRC.ConnEstabSucc.4", "RRC.ConnEstabAtt.5", "RRC.ConnEstabSucc.5", "RRC.ConnEstabAtt.6", "RRC.ConnEstabSucc.6", "RRC.ConnEstabAtt.7", "RRC.ConnEstabSucc.7",	"RRC.ConnEstabAtt.8", "RRC.ConnEstabSucc.8", "RRC.ConnEstabAtt.9", "RRC.ConnEstabSucc.9", "RRC.ConnEstabAtt.10", "RRC.ConnEstabSucc.10", "RRC.ConnEstabAtt.11", "RRC.ConnEstabSucc.11", "RRC.ConnEstabAtt.12", "RRC.ConnEstabSucc.12", "RRC.ConnEstabAtt.13", "RRC.ConnEstabSucc.13", "RRC.ConnEstabAtt.14", "RRC.ConnEstabSucc.14", "RRC.ConnEstabAtt.15", "RRC.ConnEstabSucc.15" ]

def generate_random_kpivalue(min_value=100, max_value=150):
    return random.randint(min_value, max_value)

def insert_hv_ves_kpi():
    try:
        line_protocol_batch = []
        for KPINAME in KPINAMES:
            KPIValue = generate_random_kpivalue(100,150)
            # line_protocol = (
            #     f'hvvesdata,sourceName={config["HVVESINFLUX"]["SOURCE_NAME"]},KPINAME={KPINAME} '
            #     f'KPIValue="{KPIValue}"'
            # )

            line_protocol = (
                f'{config["HVVESINFLUX"]["measurement"]},{config["HVVESINFLUX"]["sourcename"]}={config["HVVESINFLUX"]["SOURCE_NAME"]},{config["HVVESINFLUX"]["kpiname"]}={KPINAME} '
                f'{config["HVVESINFLUX"]["kpivalue"]}="{KPIValue}"'
            )

            line_protocol_batch.append(line_protocol)

        batch_data = "\n".join(line_protocol_batch)

        url = f'http://{config["HVVESINFLUX"]["HOST"]}:{config["HVVESINFLUX"]["PORT"]}/write?db={config["HVVESINFLUX"]["DATABASE"]}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(url, data=batch_data, headers=headers)

        if response.status_code == 204:
            print(f"Batch inserted: {len(KPINAMES)} kpi's")
        else:
            print(f"Error inserting batch: {response.status_code} - {response.text}")

    except KeyboardInterrupt:
        print("Process stopped manually.")

