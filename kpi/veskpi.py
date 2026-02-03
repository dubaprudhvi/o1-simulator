from utils.imports import *

def ves_kpi_menu():
    try:
        while True:
            choice = inquirer.select(
                            message="VES KPI'S",
                            border=True,
                            choices=[
                                "ADD VES KPI'S BASED ON TIME INTERVAL",
                                "ADD VES KPI'S BASED ON TIME RANGE",
                                Separator(),
                                "BACK",
                                "EXIT",
                            ],
                        ).execute()
            if choice == "ADD VES KPI'S BASED ON TIME INTERVAL":
                while True:
                    limit = input("Enter the interval range in seconds (1-10): ")
                    validated_limit = validate_number(limit, 1, 10)
                    if validated_limit is not None:
                        print()
                        insert_ves_kpi_based_on_interval(validated_limit)
                        break
            elif choice == "ADD VES KPI'S BASED ON TIME RANGE":
                while True:
                    limit = input("Enter the number of iterations (1-100): ")
                    validated_limit = validate_number(limit, 1, 100)
                    if validated_limit is not None:
                        print()
                        insert_ves_kpi_based_on_limit(validated_limit)
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

KPINAMES = ["RRU.PrbAvailDl", "RRU.PrbUsedUl", "RRU.PrbTotUl", "DRB.RlcDelayUl","DRB.AirIfDelayUl",  "DRB.AirIfDelayDl", "DRB.AvgDlRlcDelay", "AvgCellTPT", "DRB.MaxActiveUeDl.5", "DRB.MaxActiveUeDl.1","RESIDUAL_BLER", "BLER_PLOT", "RRU.PrbUsedDl", "RRU.PrbTotDl", "Normalised.PDSCH.MCS.0", "Normalised.PDSCH.MCS.1" , "Normalised.PDSCH.MCS.2" ,"Normalised.PDSCH.MCS.3" ,"Normalised.PDSCH.MCS.4" ,"Normalised.PDSCH.MCS.5" , "Normalised.PDSCH.MCS.6" ,"Normalised.PDSCH.MCS.7" ,"Normalised.PDSCH.MCS.8", "Normalised.PDSCH.MCS.9", "Normalised.PDSCH.MCS.10", "Normalised.PDSCH.MCS.11" , "Normalised.PDSCH.MCS.12" ,"Normalised.PDSCH.MCS.13" ,"Normalised.PDSCH.MCS.14" ,"Normalised.PDSCH.MCS.15" , "Normalised.PDSCH.MCS.16" ,"Normalised.PDSCH.MCS.17" ,"Normalised.PDSCH.MCS.18", "Normalised.PDSCH.MCS.19", "Normalised.PDSCH.MCS.20","Normalised.PDSCH.MCS.21" , "Normalised.PDSCH.MCS.22" ,"Normalised.PDSCH.MCS.23" ,"Normalised.PDSCH.MCS.24" ,"Normalised.PDSCH.MCS.25" , "Normalised.PDSCH.MCS.26" ,"Normalised.PDSCH.MCS.27" ,"Normalised.PDSCH.MCS.28", "Normalised.PDSCH.MCS.29",              "RRC.ConnEstabAtt.0", "RRC.ConnEstabAtt.1", "RRC.ConnEstabAtt.2", "RRC.ConnEstabAtt.3", "RRC.ConnEstabAtt.4", "RRC.ConnEstabAtt.5", "RRC.ConnEstabAtt.6", "RRC.ConnEstabAtt.7", "RRC.ConnEstabAtt.8", "RRC.ConnEstabAtt.9", "RRC.ConnEstabAtt.10", "RRC.ConnEstabAtt.11", "RRC.ConnEstabSucc.0", "RRC.ConnEstabSucc.1", "RRC.ConnEstabSucc.2", "RRC.ConnEstabSucc.3", "RRC.ConnEstabSucc.4", "RRC.ConnEstabSucc.5", "RRC.ConnEstabSucc.6", "RRC.ConnEstabSucc.7", "RRC.ConnEstabSucc.8", "RRC.ConnEstabSucc.9", "RRC.ConnEstabSucc.10", "RRC.ConnEstabSucc.11", "RRC.ConnMean", "RRC.ConnMax", "RRC.InactiveConnMean", "RRC.InactiveConnMax", "RRC.ReEstabAtt", "DRB.UEThpDl.avg", "DRB.UEThpUl.avg"]
            
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


def generate_random_kpivalue(min_value=100, max_value=150):
    return random.randint(min_value, max_value)

def generate_random_kpivalue_double(min_value=100, max_value=150):
    return round(random.uniform(min_value, max_value), 2)

def insert_ves_kpi_based_on_interval(interval):
    print("Loop started. Type 'exit' and press Enter to stop.")
    while True:
        insert_ves_kpi()
        if select.select([sys.stdin], [], [], 0.1)[0]:
            user_input = sys.stdin.readline().strip().lower()
            if user_input in ['exit', 'quit', 'stop', 'q']:
                print("Stopping loop...")
                break
        time.sleep(interval)

def insert_ves_kpi_based_on_limit(limit):
    for _ in range(limit):
        insert_ves_kpi()

def insert_ves_kpi():
    try:
        current_timestamp = int(time.time() * 1000)
        line_protocol_batch = []
        
        for KPINAME in KPINAMES:
            if KPINAME == "DRB.UEThpDl.avg" or KPINAME == "DRB.UEThpUl.avg":
                KPIValue = tpt(KPINAME)
            else:
                KPIValue = kpivalue(KPINAME)
            KPIValue_str = str(KPIValue)
            
            line_protocol = (
                f'kpidata,measObjInstId={config["VESINFLUX"]["MEASOBJINSTID_ONE"]},measuredEntityUserName={config["VESINFLUX"]["MEASUREDENTITYUSERNAME"]},'
                f'sourceName={config["VESINFLUX"]["SOURCE_NAME"]},KPINAME={KPINAME} '
                f'KPIValue="{KPIValue_str}",suspectFlag="{str(config["VESINFLUX"]["SUSPECT_FLAG"]).lower()}",timeStamp={current_timestamp}i'
            )
            line_protocol_batch.append(line_protocol)

            line_protocol = (
                f'kpidata,measObjInstId={config["VESINFLUX"]["MEASOBJINSTID_TWO"]},measuredEntityUserName={config["VESINFLUX"]["MEASUREDENTITYUSERNAME"]},'
                f'sourceName={config["VESINFLUX"]["SOURCE_NAME"]},KPINAME={KPINAME} '
                f'KPIValue="{KPIValue_str}",suspectFlag="{str(config["VESINFLUX"]["SUSPECT_FLAG"]).lower()}",timeStamp={current_timestamp}i'
            )
            line_protocol_batch.append(line_protocol)

        batch_data = "\n".join(line_protocol_batch)

        url = f'http://{config["VESINFLUX"]["HOST"]}:{config["VESINFLUX"]["PORT"]}/write?db={config["VESINFLUX"]["DATABASE"]}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(url, data=batch_data, headers=headers)

        if response.status_code == 204:
            print(f"Batch inserted: {len(KPINAMES)} kpi's")
        else:
            print(f"Error inserting batch: {response.status_code} - {response.text}")

    except KeyboardInterrupt:
        print("Process stopped manually.")
    except Exception as e:
        print(f"Unexpected error: {e}")

def kpivalue(KPINAME):
    KPIValue = 0 
    if KPINAME == "RRU.PrbAvailDl":
        KPIValue = 189
    elif KPINAME == "RRU.PrbUsedDl" or KPINAME == "RRU.PrbTotDl" or KPINAME == "DRB.AvgDlRlcDelay" or KPINAME == "DRB.AirIfDelayDl":
        KPIValue = generate_random_kpivalue(100, 150)
    elif KPINAME == "DRB.RlcDelayUl" or KPINAME == "DRB.AirIfDelayUl" or KPINAME == "RRU.PrbUsedUl" or KPINAME == "RRU.PrbTotUl":
        KPIValue = generate_random_kpivalue(100, 150)
    elif KPINAME == "AvgCellTPT":
        KPIValue = 100
    elif KPINAME == "DRB.MaxActiveUeDl.5":
        KPIValue = 1
    elif KPINAME == "BLER_PLOT" or KPINAME == "RESIDUAL_BLER":
        KPIValue = generate_random_kpivalue(0, 10)
    elif KPINAME == "Normalised.PDSCH.MCS.8":
        KPIValue = 20
    elif KPINAME == "Normalised.PDSCH.MCS.21":
        KPIValue = 80
    elif KPINAME == "RRC.ConnMean" or KPINAME == "RRC.ConnMax" or KPINAME == "RRC.ConnEstabSucc.11" or KPINAME == "RRC.ConnEstabAtt.11":
        KPIValue = 3
    elif KPINAME == "RRC.InactiveConnMean" or KPINAME == "RRC.InactiveConnMax" or KPINAME == "RRC.ReEstabAtt" or KPINAME == "DRB.MaxActiveUeDl.1":
        KPIValue = 0
    return KPIValue

def tpt(KPINAME):
    KPIValue = 0 
    if KPINAME == "DRB.UEThpDl.avg":
        KPIValue = generate_random_kpivalue_double(0,400)
    elif KPINAME == "DRB.UEThpUl.avg":
        KPIValue = generate_random_kpivalue_double(0,10)
    return KPIValue

