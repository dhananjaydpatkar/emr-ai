from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time

PORT = 8080

class MockFHIRHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests (e.g. Fetch Patient)."""
        print(f"[MockServer] GET request: {self.path}")
        
        # Simulate Patient Fetch
        if "Patient" in self.path:
            patient_id = self.path.split("/")[-1]
            self.send_response(200)
            self.send_header("Content-type", "application/fhir+json")
            self.end_headers()
            
            # Return Mock Patient
            response = {
                "resourceType": "Patient",
                "id": patient_id,
                "name": [{"family": "Argonaut", "given": ["Jason"]}],
                "gender": "male",
                "birthDate": "1985-08-01"
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        """Handle POST requests (e.g. Save Bundle)."""
        print(f"[MockServer] POST request: {self.path}")
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        bundle = json.loads(post_data)
        
        print(f"[MockServer] Received Bundle with {len(bundle.get('entry', []))} entries.")
        
        # Simulate processing delay
        time.sleep(0.5)
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status": "success", "message": "Bundle persisted"}')

def run(server_class=HTTPServer, handler_class=MockFHIRHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Starting Mock FHIR Server on port {PORT}...")
    print(f"Endpoint: http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Stopping Server.")

if __name__ == '__main__':
    run()
