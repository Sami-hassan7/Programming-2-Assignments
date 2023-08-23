import matplotlib.pyplot as plt
import linecache
import time

class CsvConverter:
    def __init__(self, file_path):

        """
         Creates a CsvConverter object using a file path. 
         It retrieves and retains the header line from the CSV file.

        Args:
            file_path (str): The path to the CSV file.
        """

        self.file_path = file_path
        self.header = linecache.getline(self.file_path, 1).strip('\n').split(',')

    def csv_to_json(self, csv_lines):

        """
        Transforms a collection of CSV lines into a JSON list containing dictionaries. 
        Each dictionary symbolizes a row in the CSV file, where the header values serve as keys paired with the respective row values.
        The function provides a string portrayal of the CsvConverter object.
        """

        return [
            dict(zip(self.header, line.strip('\n').split(',')))
            for line in csv_lines
            if len(line.strip('\n').split(',')) == len(self.header)
        ]

    def __str__(self):

        return f'CSV file: {self.file_path}'


class csv_reader:
    def __init__(self, file_path='dSST.csv', stride=5):

        """
        Sets up the csv_reader instance using a file path and a step size value. 
        It extracts the header line from the CSV file and establishes the starting line as the second line (line number 2). 
        Additionally, it initiates an empty group of observers and the default stride value is 5.
        """

        self.file_path = file_path
        self.stride = stride
        self.header = linecache.getline(self.file_path, 1).strip('\n').split(',')
        self.start = 2
        self.observers = set()

    def register_observation(self, observation):

        """
        Appends an observer to the csv_reader entity. 
        These observers receive notifications containing data read from the CSV file.

        """

        self.observers.add(observation)

    def remove_observation(self, observation):

        """
         Removes an observer from the csv_reader object.
        """

        self.observers.remove(observation)

    def notify_observation(self, data):

        """
        Informs all observers using the given data
        """

        for observation in self.observers:
            observation.update(data)

    def get_csv_lines(self):

        """
        Collects a series of lines from the CSV file, beginning at the current starting line. 
        It transforms these lines into JSON format using the CsvConverter.
        Advances the starting line for subsequent iterations.
        """

        line_list = [
            linecache.getline(self.file_path, self.start + i)
            for i in range(self.stride)
        ]
        line_list = [
            line for line in line_list if line.strip() != ''
        ]
        if line_list:
            result = CsvConverter(self.file_path).csv_to_json(line_list)
            self.start += self.stride
            # Notify observers with the new data
            self.notify_observation(result)
            return result
        else:
            return ''

    def starter_for_reading(self):

        """
        Initiates the process of reading the CSV file and sending data notifications to observers. 
        It iteratively invokes the get_csv_lines() function and pauses for n seconds during each iteration.
        """

        while True:
            lines = self.get_csv_lines()
            if lines == '':
                break
            time.sleep(3)


class AverageYear:
    def __init__(self):

        """
        Initializes the AverageYear object.
        It sets up a figure and axes for plotting average yearly temperatures.
        """

        self.temperatures = []
        self.years = []
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111)

    def update(self, data):

        """
        Updates the observer with new data. It calculates the average temperature from the data and adds it to the list of temperatures.
        It then plots the average yearly temperature using the plot_average_temperature() method.
        """

        avg = self.temperature_average_calculator(data)
        if avg:
            self.years.append(len(self.years) + 1)
            self.temperatures.append(avg)
            self.plot_average_temperature()

    def temperature_average_calculator(self, data):

        """
        Calculates the average temperature from the provided data by summing up the
        "J-D" (January-December) temperature values and dividing by the data count.
        """

        data_count = len(data)
        sum_temp = sum(float(line['J-D']) for line in data)
        if data_count == 0:
            return None
        avg = sum_temp / data_count
        return avg

    def plot_average_temperature(self):

        """
         Plots the average yearly temperature using matplotlib. 
         It clears the axes, plots the temperatures against years, and sets labels, title, and grid for the plot.
        """

        self.ax.clear()
        self.ax.plot(self.years, self.temperatures, 'go--')
        self.ax.set_xlabel('Year')
        self.ax.set_ylabel('Yearly Average Temperature')
        self.ax.set_title('Yearly Average  Temperature')
        self.ax.grid(True)
        plt.pause(0.05)
        plt.show()

class AverageMonth:
    def __init__(self):

        """
        Initializes the AverageMonth object.
        It sets up attributes for storing monthly and yearly average temperatures and creates figures and axes for plotting.
        """

        self.month_names  = [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.monthly_averages = {month: [] for month in self.month_names }
        self.years = []
        self.yearly_averages = []
        self.monthly_figure, self.monthly_ax = plt.subplots()
        self.yearly_figure, self.yearly_ax = plt.subplots()

    def update(self, data):

        """
        Updates the observer with new data. It calculates the average temperature for each month and the yearly average temperature. 
        It then plots the average monthly and yearly temperatures using the plot_average_monthly_temperature() and plot_average_yearly_temperature() methods, respectively.
        """

        self.temperature_average_calculator(data)
        self.plot_average_monthly_temperature()
        self.plot_average_yearly_temperature()

    def temperature_average_calculator(self, data):

        """
        Calculates the average monthly and yearly temperatures from the provided data. 
        It iterates over the months and adds the corresponding temperature values to the monthly averages. 
        It also adds the yearly average temperature to the yearly averages list.
        """

        data_count = len(data)
        sum_temp = sum(float(line['J-D']) for line in data)
        if data_count == 0:
            return None
        avg = sum_temp / data_count
        self.years.append(len(self.years) + 1)
        self.yearly_averages.append(avg)
        for month in self.month_names :
            self.monthly_averages[month].append(float(data[0][month]))

    def plot_average_monthly_temperature(self):
        
        """
        Creates a visualization of average monthly temperatures using matplotlib. 
        This process includes clearing the existing monthly axes, 
        Plotting temperature data points for each month, and configuring labels, a title, a legend, and a grid for the plot.
        """

        self.monthly_ax.clear()
        for month, temps in self.monthly_averages.items():
            self.monthly_ax.plot(range(1, len(temps) + 1), temps, label=month)

        self.monthly_ax.set_xlabel('Data Point')
        self.monthly_ax.set_ylabel('Monthly Average Temperature')
        self.monthly_ax.set_title('Monthly Average Temperatures')
        self.monthly_ax.legend()
        self.monthly_ax.grid(True)
        plt.pause(0.05)

    def plot_average_yearly_temperature(self):

        """
        Generates a graphical representation of average yearly temperatures using matplotlib. 
        This involves clearing the existing yearly axes, 
        plotting temperature values against corresponding years, and configuring labels, a title, and a grid for the plot.
        """

        self.yearly_ax.clear()
        self.yearly_ax.plot(self.years, self.yearly_averages, 'go--')
        self.yearly_ax.set_xlabel('Year')
        self.yearly_ax.set_ylabel('Average Temperature')
        self.yearly_ax.set_title('Average Yearly Temperature')
        self.yearly_ax.grid(True)
        plt.pause(0.05)


input_data = csv_reader('dSST.csv')
avg_month = AverageMonth()
avg_year = AverageYear()
input_data.register_observation(avg_month)
input_data.starter_for_reading()

#In general, these classes and functions collaborate to parse a CSV file, transform it into JSON structure, and inform observers with the extracted data.
#The observers (AverageYear and AverageMonth) compute and visually represent average yearly and monthly temperatures, correspondingly. They utilize the data acquired from the csv_reader class.




