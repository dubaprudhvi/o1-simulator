from utils.imports import *

import mplane.notification_service_pb2 as notification_service_pb2
import mplane.notification_service_pb2_grpc as notification_service_pb2_grpc
import mplane.fault.mplanefaultmapping as mplanefaultmapping


with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

class NotificationService(notification_service_pb2_grpc.NotificationService):
    
    def SubscribeNotifications(self, request, context):
        print(f"Client-ID: {request.client_id}")
        
        self._active = True
        
        def send_notifications():
            while self._active and context.is_active():
                try:
                    response = notification_service_pb2.NotificationRequest(
                        type="fault",
                        payload=self.generate_fault_payload()
                    )
                    yield response
                    time.sleep(config['MPLANEFAULT']['MESSAGE_FREQUENCY'])
                except Exception as e:
                    print(f"Error sending notification: {e}")
                    break
        
        def on_rpc_done():
            self._active = False
            print("Client disconnected")
        
        context.add_callback(on_rpc_done)
        
        return send_notifications()
 
    def generate_fault_payload(self):
        
        fault_id = random.choice(config['MPLANEFAULT']['FAULT_ID_LIST'])
        fault_text = mplanefaultmapping.get_fault_description(fault_id)
        fault_severity = random.choice(config['MPLANEFAULT']['SEVERITY'])
        is_cleared = random.choice(config['MPLANEFAULT']['IS_CLEAR'])
        fault_source = random.choice(config['MPLANEFAULT']['FAULT_SOURCE'])
        hostname = random.choice(config['MPLANEFAULT']['NODE'])
        ru_id = random.choice(config['MPLANEFAULT']['RU_ID_LIST'])
        affected_object_name = random.choice(config['MPLANEFAULT']['AFFECTED_OBJECT_NAME'])
        event_time = datetime.utcnow().isoformat() + "+00:00"

        payload = {
            "affected-objects": [{"name": affected_object_name}],
            "event-time": event_time,
            "fault-id": fault_id,
            "fault-severity": fault_severity,
            "fault-source": fault_source,
            "fault-text": fault_text,
            "hostname": hostname,
            "is-cleared": is_cleared,
            "ru_id": ru_id
        }
        print(payload)
        return json.dumps(payload)

def mplane_fault():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    notification_service_pb2_grpc.add_NotificationServiceServicer_to_server(
        NotificationService(), server
    )
    server.add_insecure_port(f"[::]:{config['MPLANEFAULT']['PORT']}")
    server.start()
    print("Notification Server started on port 50052")
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
        print("Server stopped")

