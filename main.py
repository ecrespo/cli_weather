import sys
from datetime import *
import pytz
from pytz import timezone
from timezonefinder import TimezoneFinder
from deep_translator import GoogleTranslator

# This is a sample Python script.
import httpx
from geopy.geocoders import Nominatim
import typer  # pip install "typer[all]"
from rich import print  # pip install rich
from rich.table import Table


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
api_key = ''

tf = TimezoneFinder()
fmt = '%Y-%m-%d %H:%M:%S %Z%z'
def __prompt() -> str:
    prompt = typer.prompt("\n¿Quieres conocer el clima? (Y/n)")

    if prompt in ["exit", "n", "N", ""]:
        if exit := typer.confirm("✋ ¿Estás seguro?"):
            print("👋 ¡Hasta luego!")
            sys.exit(typer.Abort())

        return __prompt()

    return prompt

def fah_to_cel(value:float)->  float:
    """Convierte grados Fahrenheit a grados Celsius."""
    return (value - 32) * 5/9

def main(name):
    # Use a breakpoint in the code line below to debug your script.
    # Give city name
    print("💬 [bold green]Weather API en Python[/bold green]")
    table = Table("Comando", "Comando que permite averiguar el clima actual de cualquier ciudad del mundo")
    table.add_row("exit", "Salir de la aplicación")
    table.add_row("consult", "Consulta del clima")
    print(table)

    while True:
        content = __prompt()
        if content in ["y", "Y"]:
            city = typer.prompt("\n¿Ciudad? ")
            country = typer.prompt("\n¿País? ")

            geolocator = Nominatim(user_agent="Ernesto Crespo")
            location = geolocator.geocode(city+','+country)
            lat, lon = location.latitude, location.longitude
            tz = tf.timezone_at(lng=lon, lat=lat)
            time_zone = timezone(tz)
            table2 = Table("País", f"{country}")
            table2.add_row("Ciudad", f"{city}")
            table2.add_row("Latitud", f"{lat}")
            table2.add_row("Longitud", f"{lon}")
            table2.add_row("Timezone", f"{tz}")
            now = datetime.now()
            loc_dt = now.astimezone(time_zone).strftime(fmt)

            table2.add_row("Hora", f"{loc_dt}")
            lang= 'es'
            units = 'metric'
            base_url =f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&lang={lang}&appid={api_key}&units={units}'
            response = httpx.get(base_url)
            results = response.json()
            clima = results['weather'][0]['description']
            temperatura = results['main']['temp']
            presion = results['main']['pressure']
            humedad = results['main']['humidity']
            temp_min = results['main']['temp_min']
            temp_max = results['main']['temp_max']
            velocidad = results['wind']['speed']
            deg = results['wind']['deg']
            nubosidad = results['clouds']['all']
            #translated = GoogleTranslator(source='en', target='es').translate(clima)
            table2.add_row("Clima", f"{clima}")
            table2.add_row("Temperatura", f"{temperatura}")
            table2.add_row("Presión", f"{presion}")
            table2.add_row("Humedad", f"{humedad}")
            table2.add_row("Temperatura min", f"{temp_min}")
            table2.add_row("Temperatura max", f"{temp_max}")
            table2.add_row("Velocidad viento", f"{velocidad}")
            table2.add_row("Grados viento", f"{deg}")
            table2.add_row("Nubosidad", f"{nubosidad}")
            print(table2)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
