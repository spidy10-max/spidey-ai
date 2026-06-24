"""
Spidey AI — Weather Tool
Get live weather for any city!
Uses OpenWeatherMap API (FREE!)
"""
import requests
import os
from dotenv import load_dotenv
from spidey.logger import app_logger, log_event, log_error

load_dotenv()


class WeatherTool:
    """Get live weather data"""

    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

        if self.api_key:
            app_logger.info("WeatherTool ready")
        else:
            app_logger.warning("WeatherTool: No API key! Set OPENWEATHER_API_KEY in .env")

    def get_weather(self, city):
        """
        Get current weather for a city

        Args:
            city: City name (e.g., "Kotaddu", "Karachi", "London")

        Returns:
            Formatted weather string
        """
        if not self.api_key:
            return "❌ Weather API key not set! Add OPENWEATHER_API_KEY to .env file."

        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"
            }

            response = requests.get(self.base_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return self._format_weather(data, city)
            elif response.status_code == 404:
                return f"❌ City '{city}' not found. Check spelling!"
            elif response.status_code == 401:
                return "❌ Invalid API key! Check OPENWEATHER_API_KEY in .env"
            else:
                return f"❌ Weather API error: {response.status_code}"

        except requests.Timeout:
            return "❌ Weather API timeout. Check internet connection!"
        except requests.ConnectionError:
            return "❌ No internet connection!"
        except Exception as e:
            log_error(str(e), "WeatherTool.get_weather")
            return f"❌ Weather error: {e}"

    def get_forecast(self, city, days=3):
        """
        Get weather forecast

        Args:
            city: City name
            days: Number of days (1-5)
        """
        if not self.api_key:
            return "❌ API key not set!"

        try:
            url = "https://api.openweathermap.org/data/2.5/forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "cnt": days * 8  # 3-hour intervals
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return self._format_forecast(data, city, days)
            elif response.status_code == 404:
                return f"❌ City '{city}' not found!"
            else:
                return f"❌ Forecast error: {response.status_code}"

        except requests.ConnectionError:
            return "❌ No internet!"
        except Exception as e:
            log_error(str(e), "WeatherTool.get_forecast")
            return f"❌ Error: {e}"

    def _format_weather(self, data, city):
        """Format weather data nicely"""
        try:
            temp = round(data["main"]["temp"])
            feels = round(data["main"]["feels_like"])
            humidity = data["main"]["humidity"]
            desc = data["weather"][0]["description"].title()
            wind = round(data["wind"]["speed"] * 3.6)  # m/s to km/h
            pressure = data["main"]["pressure"]
            icon = self._get_icon(data["weather"][0]["main"])
            country = data["sys"]["country"]
            temp_min = round(data["main"]["temp_min"])
            temp_max = round(data["main"]["temp_max"])

            result = f"""
{icon} Weather in {city.title()}, {country}:
   🌡️ Temperature: {temp}°C (Feels like {feels}°C)
   📊 Min/Max: {temp_min}°C / {temp_max}°C
   ☁️ Condition: {desc}
   💧 Humidity: {humidity}%
   💨 Wind: {wind} km/h
   🔽 Pressure: {pressure} hPa"""

            log_event("Weather fetched", f"{city}: {temp}°C, {desc}")
            return result.strip()

        except Exception as e:
            return f"❌ Error formatting weather: {e}"

    def _format_forecast(self, data, city, days):
        """Format forecast data"""
        try:
            result = f"📅 {days}-Day Forecast for {city.title()}:\n"

            seen_dates = set()
            for item in data["list"]:
                date = item["dt_txt"].split(" ")[0]
                time_str = item["dt_txt"].split(" ")[1][:5]

                if date not in seen_dates and time_str == "12:00":
                    seen_dates.add(date)
                    temp = round(item["main"]["temp"])
                    desc = item["weather"][0]["description"].title()
                    icon = self._get_icon(item["weather"][0]["main"])

                    result += f"   {icon} {date}: {temp}°C — {desc}\n"

                    if len(seen_dates) >= days:
                        break

            return result.strip()

        except Exception as e:
            return f"❌ Forecast format error: {e}"

    def _get_icon(self, condition):
        """Get weather emoji"""
        icons = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Drizzle": "🌦️",
            "Thunderstorm": "⛈️",
            "Snow": "❄️",
            "Mist": "🌫️",
            "Fog": "🌫️",
            "Haze": "🌫️",
            "Smoke": "🌫️",
            "Dust": "🌪️",
            "Sand": "🌪️",
        }
        return icons.get(condition, "🌡️")

    def is_available(self):
        """Check if API key is set"""
        return self.api_key is not None