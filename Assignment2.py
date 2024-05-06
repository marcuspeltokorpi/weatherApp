from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from bs4 import BeautifulSoup
from kivy.properties import StringProperty
import requests
import json


class HomeScreen(Screen):
    wundergroundWeather = StringProperty()
    wundergroundVisibility = StringProperty()
    wundergroundPressure = StringProperty()
    wundergroundHumidity = StringProperty()

    timeanddateWeather = StringProperty()
    timeanddateVisibility = StringProperty()
    timeanddatePressure = StringProperty()
    timeanddateHumidity = StringProperty()

    def firebase(self, data):
        firebaseUrl = 'https://assignment2-3fa56-default-rtdb.firebaseio.com/weather_data.json'
        response = requests.put(url=firebaseUrl, json=data)
        if response.status_code == 200:
            print("Data successfully stored")
        else:
            print(f"Failed to store data: {response.status_code}")

    def localData(self, data):
        with open('local_weather_data.json', 'w') as file:
            json.dump(data, file)
            print("Data successfully stored")

    def search(self):
        cityName = self.ids.cityName.text.replace(' ', '-').lower()
        countryName = self.ids.countryName.text.replace(' ', '-').lower()

        # Check if both cityName and countryName are not empty
        if not cityName or not countryName:
            print("Please enter both city and country names.")
            return  # Don't proceed with the search if fields are empty

        # Try fetching data from Timeanddate first
        timeanddateData = self.getTimeanddate(countryName, cityName)
        if timeanddateData:
            self.timeanddateWeather = timeanddateData['weather']
            self.timeanddateHumidity = timeanddateData['humidity']
            self.timeanddatePressure = timeanddateData['pressure']
            self.timeanddateVisibility = timeanddateData['visibility']

            # Prepare and store data
            weather_data = {"Timeanddate": timeanddateData}

        else:
            # If fetching from Timeanddate fails, try Wunderground
            wundergroundData = self.getWunderground(countryName, cityName)
            if wundergroundData:
                self.wundergroundWeather = wundergroundData["weather"]
                self.wundergroundHumidity = wundergroundData["humidity"]
                self.wundergroundPressure = wundergroundData["pressure"]
                self.wundergroundVisibility = wundergroundData["visibility"]

                # Prepare and store data
                weather_data = {"Wunderground": wundergroundData}


    def countryCodes(self, countryName):
        # Dictionary of country names and their corresponding country codes
        replacements = {
            'Afghanistan': 'af',
            'Albania': 'al',
            'Algeria': 'dz',
            'Andorra': 'ad',
            'Angola': 'ao',
            'Antigua and Barbuda': 'ag',
            'Argentina': 'ar',
            'Armenia': 'am',
            'Australia': 'au',
            'Austria': 'at',
            'Azerbaijan': 'az',
            'Bahamas': 'bs',
            'Bahrain': 'bh',
            'Bangladesh': 'bd',
            'Barbados': 'bb',
            'Belarus': 'by',
            'Belgium': 'be',
            'Belize': 'bz',
            'Benin': 'bj',
            'Bhutan': 'bt',
            'Bolivia': 'bo',
            'Bosnia and Herzegovina': 'ba',
            'Botswana': 'bw',
            'Brazil': 'br',
            'Brunei': 'bn',
            'Bulgaria': 'bg',
            'Burkina Faso': 'bf',
            'Burundi': 'bi',
            'Cabo Verde': 'cv',
            'Cambodia': 'kh',
            'Cameroon': 'cm',
            'Canada': 'ca',
            'Central African Republic': 'cf',
            'Chad': 'td',
            'Chile': 'cl',
            'China': 'cn',
            'Colombia': 'co',
            'Comoros': 'km',
            'Congo (Congo-Brazzaville)': 'cg',
            'Costa Rica': 'cr',
            'Croatia': 'hr',
            'Cuba': 'cu',
            'Cyprus': 'cy',
            'Czechia (Czech Republic)': 'cz',
            'Democratic Republic of the Congo (Congo-Kinshasa)': 'cd',
            'Denmark': 'dk',
            'Djibouti': 'dj',
            'Dominica': 'dm',
            'Dominican Republic': 'do',
            'East Timor (Timor-Leste)': 'tl',
            'Ecuador': 'ec',
            'Egypt': 'eg',
            'El Salvador': 'sv',
            'Equatorial Guinea': 'gq',
            'Eritrea': 'er',
            'Estonia': 'ee',
            'Eswatini (fmr. "Swaziland")': 'sz',
            'Ethiopia': 'et',
            'Fiji': 'fj',
            'Finland': 'fi',
            'Gabon': 'ga',
            'Gambia': 'gm',
            'Georgia': 'ge',
            'Germany': 'de',
            'Ghana': 'gh',
            'Greece': 'gr',
            'Grenada': 'gd',
            'Guatemala': 'gt',
            'Guinea': 'gn',
            'Guinea-Bissau': 'gw',
            'Guyana': 'gy',
            'Haiti': 'ht',
            'Honduras': 'hn',
            'Hungary': 'hu',
            'Iceland': 'is',
            'India': 'in',
            'Indonesia': 'id',
            'Iran': 'ir',
            'Iraq': 'iq',
            'Ireland': 'ie',
            'Israel': 'il',
            'Italy': 'it',
            'Ivory Coast': 'ci',
            'Jamaica': 'jm',
            'Jordan': 'jo',
            'Kazakhstan': 'kz',
            'Kenya': 'ke',
            'Kiribati': 'ki',
            'Kosovo': 'xk',
            'Kuwait': 'kw',
            'Kyrgyzstan': 'kg',
            'Laos': 'la',
            'Latvia': 'lv',
            'Lebanon': 'lb',
            'Lesotho': 'ls',
            'Liberia': 'lr',
            'Libya': 'ly',
            'Liechtenstein': 'li',
            'Lithuania': 'lt',
            'Luxembourg': 'lu',
            'Madagascar': 'mg',
            'Malawi': 'mw',
            'Malaysia': 'my',
            'Maldives': 'mv',
            'Mali': 'ml',
            'Malta': 'mt',
            'Marshall Islands': 'mh',
            'Mauritania': 'mr',
            'Mauritius': 'mu',
            'Mexico': 'mx',
            'Micronesia': 'fm',
            'Moldova': 'md',
            'Monaco': 'mc',
            'Mongolia': 'mn',
            'Montenegro': 'me',
            'Morocco': 'ma',
            'Mozambique': 'mz',
            'Myanmar (formerly Burma)': 'mm',
            'Namibia': 'na',
            'Nauru': 'nr',
            'Nepal': 'np',
            'Netherlands': 'nl',
            'New Zealand': 'nz',
            'Nicaragua': 'ni',
            'Niger': 'ne',
            'Nigeria': 'ng',
            'North Korea': 'kp',
            'North Macedonia (fmr. "Macedonia")': 'mk',
            'Norway': 'no',
            'Oman': 'om',
            'Pakistan': 'pk',
            'Palau': 'pw',
            'Palestine State': 'ps',
            'Panama': 'pa',
            'Papua New Guinea': 'pg',
            'Paraguay': 'py',
            'Peru': 'pe',
            'Philippines': 'ph',
            'Poland': 'pl',
            'Portugal': 'pt',
            'Qatar': 'qa',
            'Romania': 'ro',
            'Russia': 'ru',
            'Rwanda': 'rw',
            'Saint Kitts and Nevis': 'kn',
            'Saint Lucia': 'lc',
            'Saint Vincent and the Grenadines': 'vc',
            'Samoa': 'ws',
            'San Marino': 'sm',
            'Sao Tome and Principe': 'st',
            'Saudi Arabia': 'sa',
            'Senegal': 'sn',
            'Serbia': 'rs',
            'Seychelles': 'sc',
            'Sierra Leone': 'sl',
            'Singapore': 'sg',
            'Slovakia': 'sk',
            'Slovenia': 'si',
            'Solomon Islands': 'sb',
            'Somalia': 'so',
            'South Africa': 'za',
            'South Korea': 'kr',
            'South Sudan': 'ss',
            'Spain': 'es',
            'Sri Lanka': 'lk',
            'Sudan': 'sd',
            'Suriname': 'sr',
            'Sweden': 'se',
            'Switzerland': 'ch',
            'Syria': 'sy',
            'Taiwan': 'tw',
            'Tajikistan': 'tj',
            'Tanzania': 'tz',
            'Thailand': 'th',
            'Togo': 'tg',
            'Tonga': 'to',
            'Trinidad and Tobago': 'tt',
            'Tunisia': 'tn',
            'Turkey': 'tr',
            'Turkmenistan': 'tm',
            'Tuvalu': 'tv',
            'Uganda': 'ug',
            'Ukraine': 'ua',
            'United Arab Emirates': 'ae',
            'United Kingdom': 'gb',
            'United States of America': 'us',
            'Uruguay': 'uy',
            'Uzbekistan': 'uz',
            'Vanuatu': 'vu',
            'Vatican City (Holy See)': 'va',
            'Venezuela': 've',
            'Vietnam': 'vn',
            'Yemen': 'ye',
            'Zambia': 'zm',
            'Zimbabwe': 'zw',
        }

        countryCode = countryName.title()

        return replacements.get(countryCode)

    def getWunderground(self, countryName, cityName):
        countryCode = self.countryCodes(countryName)
        url = f'https://www.wunderground.com/weather/{countryCode}/{cityName}'
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract temperature and general weather description
            weatherSection = soup.find(class_='current-temp')
            weather = weatherSection.get_text(strip=True) if weatherSection else 'Temperature not found'

            # Extract humidity, pressure, and visibility
            additionalConditions = soup.find('div', class_='data-module additional-conditions')
            visibility, pressure, humidity = 'Not found', 'Not found', 'Not found'
            if additionalConditions:
                rows = additionalConditions.find_all('div', class_='row')
                for row in rows:
                    title = row.find('div', class_='small-4 columns').get_text(strip=True)
                    value = row.find('div', class_='small-8 columns').get_text(strip=True)

                    if title == 'Pressure':
                        pressure = value
                    elif title == 'Visibility':
                        visibility = value
                    elif title == 'Humidity':
                        humidity = value

            return {
                "weather": weather,
                "visibility": visibility,
                "pressure": pressure,
                "humidity": humidity
            }
        else:
            print("Error fetching data from Wunderground")
            return None

    def encodeTimeanddate(self, cityName):
        replacements = {'å': 'a', 'ä': 'a', 'ö': 'o'}
        for swedishChar, englishChar in replacements.items():
            cityName = cityName.replace(swedishChar, englishChar)
        return cityName

    def getTimeanddate(self, countryName, cityName):
        encodedCityName = self.encodeTimeanddate(cityName)
        url = f'https://www.timeanddate.com/weather/{countryName}/{encodedCityName}'
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extracting temperature and condition
            weatherSection = soup.find('div', class_='h2')
            weather = weatherSection.get_text(strip=True) if weatherSection else 'Temperature not found'

            # Extracting the table containing weather details
            weatherTable = soup.find('div', class_='bk-focus__info').find('table')
            visibility, pressure, humidity = 'N/A', 'N/A', 'N/A'

            if weatherTable:
                rows = weatherTable.find_all('tr')
                for row in rows:
                    cells = row.find_all(['th', 'td'])
                    if len(cells) == 2:
                        title = cells[0].get_text(strip=True)
                        value = cells[1].get_text(strip=True)

                        if 'Visibility' in title:
                            visibility = value
                        elif 'Pressure' in title:
                            pressure = value
                        elif 'Humidity' in title:
                            humidity = value

            return {
                "weather": weather,
                "visibility": visibility,
                "pressure": pressure,
                "humidity": humidity
            }
        else:
            print("Error fetching data from timeanddate.com")
            return None



class ASSignmentApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.theme_style = "Light"
        Window.size = (700, 700)

ASSignmentApp().run()
