from utils.imports import *

count = 0
fake = Faker()
random.shuffle(list(set(Provider.first_names)))

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)


def gzip_compress_xml(xml_file, gz_file):
    try:
        with open(xml_file, "rb") as f_in, gzip.open(gz_file, "wb") as f_out:
            f_out.writelines(f_in)
        print(f"[GZIP] Created {gz_file}")
    except Exception as e:
        print(f"[GZIP ERROR] {e}")


def send_file_info(file_name, location):
    timestamp_microsec = int(time.time() * 1_000_000)
    global count
    count = count + 1
    
    payload = {
        "event": {
            "commonEventHeader": {
                "version": "4.1",
                "vesEventListenerVersion": "7.2",
                "domain": "notification",
                "eventId": f"FileReady_{file_name}",
                "eventName": "perf3gpp_gnb-wisig_pmMeasResult",
                "sequence": 0,
                "priority": "Normal",
                "sourceName": config["VES"]["SOURCE_NAME"],
                "reportingEntityName": config["VES"]["SOURCE_NAME"],
                "timeZoneOffset": "UTC+05.30",
                "startEpochMicrosec": timestamp_microsec,
                "lastEpochMicrosec": timestamp_microsec,
            },
            "notificationFields": {
                "notificationFieldsVersion": "2.0",
                "changeIdentifier": "PM_MEAS_FILES",
                "changeType": "FileReady",
                "arrayOfNamedHashMap": [
                    {
                        "name": file_name,
                        "hashMap": {
                            "location": location,
                            "compression": "gzip",
                            "fileFormatType": "org.3GPP.28.532#measData",
                            "fileFormatVersion": "V10",
                        },
                    }
                ],
            },
        },
        "systemInfo": {
            "ipAddress": config["SDNR"]["HOST"],
            "username": config["SDNR"]["USERNAME"],
            "password": config["SDNR"]["PASSWORD"],
        },
    }

    try:
        response = requests.post(config["VES"]["BASE_URL"], json=payload, timeout=10)
        print(f"[API] Sent event for {file_name}, code: {response.status_code}")
        print(f"COUNT: -------- {count} -------")
        if response.status_code >= 400:
            print(f"      Response: {response.text}")
    except Exception as e:
        print(f"[API-ERROR] {e}")

def create_files(stop_event):
    with open(config["VES"]["INPUT_FILE_PATH"], "r", encoding="utf-8") as infile:
        data = infile.read()

    while not stop_event.is_set():
        for _ in range(int(config["VES"]["NO_OF_FILES_SEND_IN_SECONDS"])):
            random_digits = "".join(random.choices("0123456789", k=5))
            filename = f"B20250529.1131+00_00-1131+00_00_{random_digits}D_-_13.xml"
            file_path = os.path.join(config["VES"]["TARGET_DIR"], filename)
            gz_file_path = file_path + ".gz"

            with open(file_path, "w", encoding="utf-8") as outfile:
                outfile.write(data)

            gzip_compress_xml(file_path, gz_file_path)

            sftp_location = (
                f"sftp://{config['SDNR']['USERNAME']}@{config['SDNR']['HOST']}:"
                f"{config['VES']['TARGET_DIR']}/{filename}.gz"
            )
            send_file_info(filename, sftp_location)

        print(f"[CREATE] Batch of {config['VES']['NO_OF_FILES_SEND_IN_SECONDS']} files created at {time.strftime('%Y-%m-%d %H:%M:%S')}")

        if stop_event.wait(int(config["VES"]["FILE_SENDING_FREQUENCY_IN_SECONDS"])):
            break

def delete_files(stop_event):
    while not stop_event.is_set():
        current_time = time.time()
        for filename in os.listdir(config["VES"]["TARGET_DIR"]):
            if filename.endswith(".xml") and filename != config["VES"]["INPUT_FILE_NAME"]:
                file_path = os.path.join(config["VES"]["TARGET_DIR"], filename)
                gz_file_path = file_path + ".gz"
                try:
                    file_mtime = os.path.getmtime(file_path)
                    file_age = current_time - file_mtime
                    if file_age >= int(config["VES"]["FILE_DELETE_TIMER_IN_SECONDS"]):
                        os.remove(file_path)
                        print(f"[DELETE] {filename} removed (age: {file_age:.1f}s)")
                        if os.path.isfile(gz_file_path):
                            os.remove(gz_file_path)
                            print(f"[DELETE] {os.path.basename(gz_file_path)} removed")
                except Exception as e:
                    print(f"[DELETE ERROR] {e}")
        if stop_event.wait(10):
            break


def generate_kpi_xml_files():
    print("Loop started. Type 'exit' to stop.")
    stop_event = threading.Event()

    t1 = threading.Thread(target=create_files, args=(stop_event,))
    t2 = threading.Thread(target=delete_files, args=(stop_event,))

    t1.start()
    t2.start()

    try:
        while True:
            cmd = input("> ").strip().lower()
            if cmd in {"exit", "quit", "stop", "q"}:
                print("Stopping...")
                stop_event.set()
                break
    except KeyboardInterrupt:
        print("Stopped manually.")
        stop_event.set()

    t1.join()
    t2.join()
    print("Stopped")
