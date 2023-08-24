import http.server
import socketserver
import csv

class WeatherDataHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/data'):
            self.handle_data_request()
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_data_request(self):

        # Load the weather data from the CSV file
        try:
            data = self.load_weather_data()  
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Weather data file not found')
            return
        
        path_parts = self.path.split('/')
        if len(path_parts) == 3 and path_parts[2] == 'all':
            
            # Manage requests for complete data.
            self.send_response(200)
            self.send_header('Content-type', 'text/csv')
            self.end_headers()
            self.wfile.write(data.encode())
        elif len(path_parts) == 3 and path_parts[2].isdigit():
            
            # Manage request for year data
            year = int(path_parts[2])
            weather = self.get_weather_for_year(data, year)
            if weather:
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(weather.encode())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Weather data not found for the specified year')
        elif len(path_parts) == 4 and path_parts[2].isdigit() and path_parts[3].isdigit():
            
            # Manage request for data by year range
            from_year = int(path_parts[2])
            to_year = int(path_parts[3])
            weather_range = self.get_weather_range(data, from_year, to_year)
            if weather_range:
                self.send_response(200)
                self.send_header('Content-type', 'text/csv')
                self.end_headers()
                self.wfile.write(weather_range.encode())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Weather data not found for the specified range')
        else:
            # Manage invalid request
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Illegal request')
    
    def load_weather_data(self):
        with open('dSST.csv', 'r') as file:
            return file.read()  
       
    
    def get_weather_for_year(self, data, year):
        reader = csv.DictReader(data.splitlines())
        for row in reader:
            if int(row['Year']) == year:
                return row
        return None
    
    def get_weather_range(self, data, from_year, to_year):
        reader = csv.DictReader(data.splitlines())
        filtered_rows = [row for row in reader if from_year <= int(row['Year']) <= to_year]
        
        # put the rows together into a single string with newline separators
        if filtered_rows:
            output = ['Year,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,J-D,D-N,DJF,MAM,JJA,SON']
            output.extend(row['Year,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,J-D,D-N,DJF,MAM,JJA,SON'] for row in filtered_rows)
            return '\n'.join(output)  
        else:
            return None

PORT = 8080
handler = WeatherDataHandler
http = socketserver.TCPServer(("", PORT), handler)

print("Serving at port", PORT)

# Start the server and run it
http.serve_forever()  
