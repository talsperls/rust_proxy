import http.server
import socketserver
import urllib.request
import json

PORT = 4444
CRATES_REGISTRY_URL = "https://crates.io"

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print("START")
        # Extract the requested path from the original URL
        requested_path = self.path

        # Construct the crates.io registry URL
        crates_registry_url = f"{CRATES_REGISTRY_URL}{requested_path}"

        try:
            # Forward the request to the crates.io registry
            with urllib.request.urlopen(crates_registry_url) as response:
                # Read the response from the crates.io registry
                crates_response = response.read()

                # Parse the JSON response to extract package name and version
                metadata = json.loads(crates_response)
                package_name = metadata['name']
                package_version = metadata['version']

                # Print the package name and version
                print(f"Package Name: {package_name}")
                print(f"Package Version: {package_version}")

                # Send the crates.io registry's response back to the client
                self.send_response(200)
                self.end_headers()
                self.wfile.write(crates_response)

        except urllib.error.HTTPError as e:
            # Handle HTTP errors from the crates.io registry
            self.send_error(e.code, e.reason)

with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
    print("Proxy server running at port", PORT)
    httpd.serve_forever()
