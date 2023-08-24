import pandas as pd

class DataProvider:
    def __init__(self, data_file):
        self.data = pd.read_csv(data_file)
    
    def get_data(self, year_range=None):

        # Obtain weather data within the given range of years
        # If no range is specified, retrieve all available data.

        if year_range is None:
            return self.data.to_json(orient='records')
        elif isinstance(year_range, int):
            # If a singular year is given, obtain data for that specific year.
            return self.get_data_by_year(year_range)
        elif isinstance(year_range, list) and len(year_range) == 2:
            # If a range of years is provided, retrieve data for that range
            return self.get_data_by_range(year_range[0], year_range[1])
        else:
            raise ValueError("Invalid parameter. Expected an integer or a list of two integers.")
    
    def get_data_by_year(self, year):
        # Retrieve data for a specific year and format it as JSON
        data_by_year = self.data[self.data['Year'] == year].transpose()
        data_by_year.columns = ['Value']
        return data_by_year.to_json()
    
    def get_data_by_range(self, from_year, to_year):
        # Retrieve data for a range of years and format it as JSON
        data_by_range = self.data[(self.data['Year'] >= from_year) & (self.data['Year'] <= to_year)]
        return data_by_range.to_json(orient='records')

# Examples
d = DataProvider('dSST.csv')
print(d.get_data())  # returns all the data in the CSV as a JSON stream
print(d.get_data(1991))  # returns one line of data; the one that corresponds to the year 1991
print(d.get_data([1991, 2000]))  # returns 10 lines of data, from the year 1991 to 2000


from server2 import WeatherDataHandler  
import socketserver

# Start the server
PORT = 8080
handler = WeatherDataHandler
http = socketserver.TCPServer(("", PORT), handler)

print("Serving at port", PORT)
http.serve_forever()
