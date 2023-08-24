import http.server
import socketserver
from dataprovidor import DataProvider

class WeatherDataHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.data_provider = DataProvider('dSST.csv')
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path.startswith('/data'):
            self.handle_data_request()
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_data_request(self):
        try:
            if self.path == '/data/all':
                response_data = self.data_provider.get_all_data()  # Get all data from the data provider
            elif self.path.startswith('/data/') and self.path.count('/') == 2:
                _, _, param = self.path.split('/')
                if param.isdigit():
                    response_data = self.data_provider.get_data_by_year(int(param))  # Get data for a specific year
                else:
                    raise ValueError("Invalid year parameter")
            elif self.path.startswith('/data/') and self.path.count('/') == 3:
                _, _, from_year, to_year = self.path.split('/')
                if from_year.isdigit() and to_year.isdigit():
                    response_data = self.data_provider.get_data_by_range(int(from_year), int(to_year))  # Get data for a range of years
                else:
                    raise ValueError("Invalid year range parameters")
            else:
                raise ValueError("Invalid request")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response_data.encode())
        except ValueError as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(str(e).encode())
            
            
if __name__ == "__main__":
    PORT = 8080

    # The processor for HTTP requests.
    handler = WeatherDataHandler  

     # TCP server
    httpd = socketserver.TCPServer(("", PORT), handler) 

    print("Serving at port", PORT)
    # Start the server
    httpd.serve_forever()  
