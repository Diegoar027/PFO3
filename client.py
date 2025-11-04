import socket
import json

class TaskClient:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        
    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        
    def send_task(self, task):
        try:
            task_json = json.dumps(task)
            self.client.send(task_json.encode())
            
            response = self.client.recv(1024).decode()
            return json.loads(response)
        except Exception as e:
            print(f"Error al enviar tarea: {e}")
            return None
            
    def close(self):
        self.client.close()

if __name__ == "__main__":
    client = TaskClient()
    client.connect()
    
    # Ejemplo de uso
    result = client.send_task("Tarea de prueba")
    print(f"Resultado: {result}")
    
    client.close()