
import sys
import requests
#import PyQt5
from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,QLineEdit,QPushButton,QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label=QLabel("Enter the City name",self)
        self.city_input=QLineEdit(self)
        self.get_weather_button=QPushButton("Get Weather",self)
        self.temperature_label=QLabel(self)
        self.emoji_label=QLabel(self)
        self.description_label=QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox=QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        #self.get_weather_button.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet(""" 
        QLable,QPushButton{
                           font-family: calibri
                           }
                           QLabel#city_label{
                           font-size:40px;
                           
                           }
                           QLineEdit#city_input{
                           font-size:40px;
                           }
                           QPushButton#get_weather_button{
                           font-size:30px;
                           font-weight:bold;
                           }
                           QLable#temperature_label{
                           
                           font-size:75px;
                           }
                           QLabel#emoji_label{
                           font-size:100px;
                           font-family: Segoe UI emoji;

                           }

                           QLabel#description_label{
                           font-size:50px;}
                           
                           """)



        self.get_weather_button.clicked.connect(self.get_weather)
    def get_weather(self):
        
        api_key="d6bb3c0f8b5a1f08287204e8b4ba57cb"
        city=self.city_input.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response= requests.get(url)
            response.raise_for_status()
            data=response.json()
            
            if data["cod"]==200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request\n Please check your Input")
                case 401:
                    self.display_error("UnAthorized \n Invalid API Key")
                case 403:
                    self.display_error("Forbidden\n Access Denied")
                case 404:
                    self.display_error("Not Found\n City Not Found")
                case 500:
                    self.display_error("Internal Server Error\n Please try again later")
                case 502:
                    self.display_error("Bad Gateway\n Invalid response from server")
                case 503:
                    self.display_errort("Server Unavailabe\n Server is Down")
                case 504:
                    self.display_error("gateWay Time-Out\n No Response from Server")

                case _:
                    self.display_error(f"HTTP Error Occured\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\n Please Check Your Internet Connection ")
        except requests.exceptions.Timeout:
            self.display_error("TimeOut Error:\n The Request time Out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\n Check The URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n {req_error}")
        
    



        

    def display_error(self,message):
        self.temperature_label.setStyleSheet("font-size:30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
    def display_weather(self,data):
        self.temperature_label.setStyleSheet("font-size:60px;")
        temperature_k=data["main"]["temp"]
        temperature_c=temperature_k-273.15
        temperature_f=(temperature_k*9/5)-459.67
        weather_id=data["weather"][0]["id"]
        weather_description=data["weather"][0]["description"]

        
        

        self.temperature_label.setText(f"{temperature_f:.0f}°F")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod    
    def get_weather_emoji(weather_id):
        if weather_id>=200 and weather_id<=232:
            return"⛈️"
        elif weather_id<=300 and weather_id<=321:
            return "🌨️"
        elif weather_id<=500 and weather_id<=531:
            return "🌤️"
        elif weather_id<=600 and weather_id<=622:
            return "❄️"
        elif weather_id<=700 and weather_id<=741:
            return "🌫️"
        elif weather_id==762:
            return "🪭"
        elif weather_id ==771:
            return "😶‍🌫️"
        elif weather_id==781:
            return "🌨️"
        elif weather_id==800:
            return "☀️"
        else:
            return "😊" 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app=WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
