import socket
import json
import random
from dice import Dice   # ใช้คลาสที่แยกไว้

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server socket to an IP address and port
server_socket.bind(('localhost', 8081))

# Start listening for incoming connections
server_socket.listen(1)
print("Server is listening on port 8081...")

# Accept incoming client connections
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} established.")
    
    # Receive the HTTP request from the client
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Request received ({len(request)}):")
    print("*"*50)
    print(request)
    print("*"*50)

    # ตรวจสอบว่าเป็น POST /roll_dice หรือไม่
    if request.startswith("POST /roll_dice"):
        # หา body ของ JSON (หลังจากบรรทัดว่าง)
        parts = request.split('\r\n\r\n', 1)
        if len(parts) < 2:
            response = "HTTP/1.1 400 Bad Request\r\n\r\n"
        else:
            body = parts[1]
            try:
                data = json.loads(body)
                probs = data.get("probabilities")
                count = data.get("number_of_random")
                if not probs or not count:
                    raise ValueError("Missing fields")
                # สร้าง Dice object (จะ validate ผลรวม 1.0 เอง)
                dice = Dice(probs)
                rolls = dice.roll_multiple(int(count))
                response_data = {
                    "random_numbers": rolls,
                    "status": "success"
                }
                response_json = json.dumps(response_data)
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{response_json}"
            except Exception as e:
                error_response = {"status": "error", "message": str(e)}
                response_json = json.dumps(error_response)
                response = f"HTTP/1.1 400 Bad Request\r\nContent-Type: application/json\r\n\r\n{response_json}"
    
    # กรณี GET /myjson (ของเดิม)
    elif request.startswith("GET /myjson"):
        response_data = {
            "status": "success",
            "message": "Hello, KU!"
        }
        response_json = json.dumps(response_data)
        response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{response_json}"
    
    # กรณี GET อื่น ๆ (ของเดิม)
    elif request.startswith("GET"):
        response = f"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n
                        <html><body><h1>Hello, World!</h1><hr>{request}</body></html>"""
    
    else:
        response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"

    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()
    
    print("Waiting for the next TCP request...")