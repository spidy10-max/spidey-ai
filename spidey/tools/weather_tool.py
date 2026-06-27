"""
Spidey Weather Tool
Fetches real-time weather data using OpenWeatherMap API
Day 37 — Internet & Web Tools
"""

import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


class WeatherTool:
    """Real-time weather fetcher for Spidey AI Assistant"""

    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY", "")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        self.name = "weather"
        self.description = "Get current weather and forecast for any city"
        self.enabled = bool(self.api_key)

    def is_available(self):
        """Check if API key is configured"""
        return self.enabled

    def get_current_weather(self, city, units="metric"):
        """
        Fetch current weather for a city.
        Returns formatted string.
        """
        if not self.enabled:
            return "⚠️ Weather tool not configured. Add OPENWEATHER_API_KEY to .env file."

        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units
            }

            response = requests.get(self.base_url, params=params, timeout=10)

            if response.status_code == 404:
                return f"⚠️ City '{city}' not found. Spelling check karo."

            if response.status_code == 401:
                return "⚠️ Invalid API key. OPENWEATHER_API_KEY check karo."

            response.raise_for_status()
            data = response.json()

            unit_symbol = "°C" if units == "metric" else "°F"
            speed_unit = "m/s" if units == "metric" else "mph"

            result = (
                f"\n🌍 Weather in {data['name']}, {data['sys']['country']}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🌡️  Temperature: {data['main']['temp']}{unit_symbol} "
                f"(Feels like {data['main']['feels_like']}{unit_symbol})\n"
                f"📊  Range: {data['main']['temp_min']}{unit_symbol} — "
                f"{data['main']['temp_max']}{unit_symbol}\n"
                f"☁️  Condition: {data['weather'][0]['description'].title()}\n"
                f"💧  Humidity: {data['main']['humidity']}%\n"
                f"💨  Wind: {data['wind']['speed']} {speed_unit}\n"
                f"👁️  Visibility: {data.get('visibility', 'N/A')} meters\n"
                f"☁️  Clouds: {data['clouds']['all']}%\n"
                f"🌅  Sunrise: {datetime.fromtimestamp(data['sys']['sunrise']).strftime('%I:%M %p')}\n"
                f"🌇  Sunset: {datetime.fromtimestamp(data['sys']['sunset']).strftime('%I:%M %p')}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🕐 Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

            return result

        except requests.exceptions.Timeout:
            return "⚠️ Request timed out. Internet check karo."
        except requests.exceptions.ConnectionError:
            return "⚠️ No internet connection."
        except requests.exceptions.RequestException as e:
            return f"⚠️ Request failed: {str(e)}"
        except Exception as e:
            return f"⚠️ Weather error: {str(e)}"

    def get_forecast(self, city, units="metric", days=3):
        """
        Fetch weather forecast (up to 5 days).
        Returns formatted string.
        """
        if not self.enabled:
            return "⚠️ Weather tool not configured. Add OPENWEATHER_API_KEY to .env file."

        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units,
                "cnt": days * 8
            }

            response = requests.get(self.forecast_url, params=params, timeout=10)

            if response.status_code == 404:
                return f"⚠️ City '{city}' not found."

            response.raise_for_status()
            data = response.json()

            unit_symbol = "°C" if units == "metric" else "°F"

            # Group by date
            daily = {}
            for item in data["list"]:
                date = item["dt_txt"].split(" ")[0]
                if date not in daily:
                    daily[date] = {"temps": [], "descriptions": [], "humidity": []}
                daily[date]["temps"].append(item["main"]["temp"])
                daily[date]["descriptions"].append(item["weather"][0]["description"])
                daily[date]["humidity"].append(item["main"]["humidity"])

            # Build output
            lines = [
                f"\n📅 Forecast — {data['city']['name']}, {data['city']['country']}",
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            ]

            count = 0
            for date, info in daily.items():
                if count >= days:
                    break
                avg_temp = sum(info["temps"]) / len(info["temps"])
                min_temp = min(info["temps"])
                max_temp = max(info["temps"])
                avg_hum = sum(info["humidity"]) / len(info["humidity"])
                condition = max(set(info["descriptions"]), key=info["descriptions"].count)

                lines.append(
                    f"📆 {date} | {min_temp:.1f}—{max_temp:.1f}{unit_symbol} | "
                    f"💧{avg_hum:.0f}% | {condition.title()}"
                )
                count += 1

            lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            return "\n".join(lines)

        except requests.exceptions.RequestException as e:
            return f"⚠️ Forecast failed: {str(e)}"
        except Exception as e:
            return f"⚠️ Forecast error: {str(e)}"

    def get_multi_city_weather(self, cities, units="metric"):
        """
        Multiple cities ka weather ek saath.
        """
        results = []
        for city in cities:
            results.append(self.get_current_weather(city.strip(), units))
        return "\n\n".join(results)


# ========================================
# Standalone Test
# ========================================
if __name__ == "__main__":
    print("🕷️ Spidey Weather Tool — Testing\n")

    tool = WeatherTool()

    if not tool.is_available():
        print("❌ OPENWEATHER_API_KEY not found in .env!")
        print("   Add this to your .env file:")
        print("   OPENWEATHER_API_KEY=your_key_here")
        print("\n   Get free key: https://openweathermap.org/api")
        exit()

    # Test 1
    print("=" * 50)
    print("TEST 1: Current Weather — Karachi")
    print("=" * 50)
    print(tool.get_current_weather("Karachi"))

    # Test 2
    print("\n" + "=" * 50)
    print("TEST 2: Current Weather — London")
    print("=" * 50)
    print(tool.get_current_weather("London"))

    # Test 3
    print("\n" + "=" * 50)
    print("TEST 3: 3-Day Forecast — Lahore")
    print("=" * 50)
    print(tool.get_forecast("Lahore", days=3))

    # Test 4
    print("\n" + "=" * 50)
    print("TEST 4: Invalid City")
    print("=" * 50)
    print(tool.get_current_weather("asdfxyz123"))

    # Test 5
    print("\n" + "=" * 50)
    print("TEST 5: Multiple Cities")
    print("=" * 50)
    print(tool.get_multi_city_weather(["Karachi", "Islamabad", "Lahore"]))