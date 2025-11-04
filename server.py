import socket
import threading
import queue
import json

class TaskServer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.task_queue = queue.Queue()
        self.workers = []
        self.worker_threads = 4  # Número de workers
        
    def start(self):
        # Iniciar socket servidor
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        
        # Iniciar workers
        for _ in range(self.worker_threads):
            worker = threading.Thread(target=self.worker_process)
            worker.daemon = True
            worker.start()
            self.workers.append(worker)
            
        print(f"Servidor iniciado en {self.host}:{self.port}")
        
        while True:
            client, address = self.server.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client, address))
            client_thread.daemon = True
            client_thread.start()
    
    def handle_client(self, client, address):
        print(f"Nueva conexión desde {address}")
        try:
            while True:
                data = client.recv(1024).decode()
                if not data:
                    break
                
                task = json.loads(data)
                self.task_queue.put((task, client))
                
        except Exception as e:
            print(f"Error con cliente {address}: {e}")
        finally:
            client.close()
            
    def worker_process(self):
        while True:
            task, client = self.task_queue.get()
            result = self.process_task(task)
            try:
                response = json.dumps({"result": result})
                client.send(response.encode())
            except:
                pass
            self.task_queue.task_done()
            
    def process_task(self, task):
        # Simular procesamiento
        return f"Procesado: {task}"

if __name__ == "__main__":
    server = TaskServer()
    server.start()