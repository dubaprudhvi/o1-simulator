from utils.imports import *

import mplane.notification_service_pb2 as notification_service_pb2
import mplane.notification_service_pb2_grpc as notification_service_pb2_grpc


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
                        payload=self.random_fault_payload()
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
    
    def SendNotification(self, request, context):
        """Handle single notification requests"""
        try:
            print(f"Received notification - Type: {request.type}, Payload: {request.payload}")
            return notification_service_pb2.NotificationResponse(
                success=True,
                error_message=""
            )
        except Exception as e:
            return notification_service_pb2.NotificationResponse(
                success=False,
                error_message=str(e)
            )
    
    def random_fault_payload(self):
        payloadone = "{\"affected-objects\":[{\"name\":\"Sync Module\"}],\"event-time\":\"2025-11-13T11:39:24+00:00\",\"fault-id\":17,\"fault-severity\":\"WARNING\",\"fault-source\":\"Module\",\"fault-text\":\"Alarm is cleared\",\"hostname\":\"bluerobin\",\"is-cleared\":true,\"ru_id\":\"0\"}"
        payloadtwo = "{\"affected-objects\":[{\"name\":\"Sync Module\"}],\"event-time\":\"2025-11-13T11:38:32+00:00\",\"fault-id\":17,\"fault-severity\":\"MAJOR\",\"fault-source\":\"Module\",\"fault-text\":\"Sync:No external sync source\",\"hostname\":\"bluerobin\",\"is-cleared\":false,\"ru_id\":\"0\"}"
        
        return payloadone if random.choice([True, False]) else payloadtwo


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

