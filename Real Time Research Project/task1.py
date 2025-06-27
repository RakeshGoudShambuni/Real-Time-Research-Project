import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# Load existing data or initialize empty structure
data_file = "data.json"
try:
    with open(data_file, "r") as f:
        database = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    database = {"trainers": {}, "subjects": {}}

class TrainerHandler(BaseHTTPRequestHandler):
    def _send_response(self, status=200, content_type="application/json", body=None):
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()
        if body:
            self.wfile.write(json.dumps(body).encode())
    
    def do_GET(self):
        if self.path == "/trainer":
            self._send_response(body=list(database["trainers"].values()))
        elif self.path.startswith("/trainer/"):
            parts = self.path.split("/")
            key = parts[2]
            
            if key in database["trainers"]:
                self._send_response(body=database["trainers"][key])
            else:
                self._send_response(status=404, body={"error": "Trainer not found"})
        elif self.path == "/subject":
            self._send_response(body=list(database["subjects"].values()))
        else:
            self._send_response(status=404, body={"error": "Invalid endpoint"})

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = json.loads(self.rfile.read(content_length).decode())
        
        if self.path == "/trainer":
            trainer_id = post_data.get("empId")
            if trainer_id and trainer_id not in database["trainers"]:
                database["trainers"][trainer_id] = post_data
                self._send_response(body={"message": "Trainer added"})
            else:
                self._send_response(status=400, body={"error": "Invalid or duplicate ID"})
        elif self.path == "/subject":
            subject_name = post_data.get("name")
            if subject_name and subject_name not in database["subjects"]:
                database["subjects"][subject_name] = post_data
                self._send_response(body={"message": "Subject added"})
            else:
                self._send_response(status=400, body={"error": "Invalid or duplicate subject"})
        else:
            self._send_response(status=404, body={"error": "Invalid endpoint"})
    
    def do_DELETE(self):
        if self.path.startswith("/trainer/"):
            trainer_id = self.path.split("/")[-1]
            if trainer_id in database["trainers"]:
                del database["trainers"][trainer_id]
                self._send_response(body={"message": "Trainer deleted"})
            else:
                self._send_response(status=404, body={"error": "Trainer not found"})
        else:
            self._send_response(status=404, body={"error": "Invalid endpoint"})

# Save data on exit
def save_data():
    with open(data_file, "w") as f:
        json.dump(database, f, indent=4)

if __name__ == "__main__":
    try:
        server = HTTPServer(("", 8000), TrainerHandler)
        print("Server started on port 8000")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Saving data and shutting down server...")
        save_data()
        server.server_close()
