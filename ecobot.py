import discord
from discord.ext import commands
import random
import requests
import os

API_KEY = 'OPENWEATHER API KEY HERE'

# Configuración del bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

# Evento de inicio
@bot.event
async def on_ready():
    print(f"Bot iniciado como {bot.user}")

@bot.command()
async def commands(ctx):
    await ctx.send("Estos son mis comandos:\n$info [tema]\n$calidadaire [ciudad]\n$reducir\n$organizaciones\n$impacto [tema]\n$acciones\n")
@bot.command()
async def ayuda(ctx):
    await ctx.send("Estos son mis comandos:\n$info [tema]\n$calidadaire [ciudad]\n$reducir\n$organizaciones\n$impacto [tema]\n$acciones\n")
@bot.command()
async def info(ctx, tema=None):
    temas = {
        "aire": "La contaminación del aire provoca enfermedades respiratorias y millones de muertes al año. Evita usar combustibles fósiles.",
        "agua": "El agua contaminada afecta al 40% de la población mundial. Reduce el uso de plásticos de un solo uso.",
        "suelo": "Los residuos tóxicos contaminan el suelo y afectan la agricultura. Usa fertilizantes orgánicos para minimizar el impacto."
    }
    if tema and tema.lower() in temas:
        await ctx.send(temas[tema.lower()])
    else:
        await ctx.send("Temas disponibles: aire, agua, suelo. Usa `$info [tema]` para más detalles.")

@bot.command()
async def calidadaire(ctx, ciudad=None):
    if ciudad == None:
        await ctx.send("Porfavor ingrese una ciudad.")
    else:

        try:
            # URL para geolocalización
            location_url = f"http://api.openweathermap.org/geo/1.0/direct?q={ciudad}&limit=1&appid={API_KEY}"
            location_response = requests.get(location_url)
            location_data = location_response.json()
            
            print("Datos de geolocalización:", location_data)  # Para ver la respuesta de geolocalización

            # Validar datos de geolocalización
            if not location_data or 'lat' not in location_data[0] or 'lon' not in location_data[0]:
                await ctx.send(f"No se encontró la ciudad '{ciudad}'. Verifica el nombre.")
                return

            lat = location_data[0]['lat']
            lon = location_data[0]['lon']

            # URL para calidad del aire
            air_quality_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
            air_quality_response = requests.get(air_quality_url)
            air_quality_data = air_quality_response.json()

            print("Datos de calidad del aire:", air_quality_data)  # Para ver la respuesta de calidad del aire

            # Validar respuesta de calidad del aire
            if 'list' not in air_quality_data or len(air_quality_data['list']) == 0:
                await ctx.send("No se pudo obtener la calidad del aire. Intenta de nuevo más tarde.")
                return

            # Obtener AQI y niveles
            aqi = air_quality_data['list'][0]['main']['aqi']
            aqi_levels = {
                1: "Bueno 😊",
                2: "Moderado 😐",
                3: "Dañino para grupos sensibles 😷",
                4: "No saludable 😷",
                5: "Peligroso 😱"
            }
            aqi_message = aqi_levels.get(aqi, "Desconocido")

            await ctx.send(f"La calidad del aire en {ciudad} es: {aqi_message} (AQI: {aqi}).")
        except Exception as e:
            await ctx.send(f"Ocurrió un error: {str(e)}")
            print(f"Error al obtener la calidad del aire: {e}")


@bot.command()
async def reducir(ctx):
    consejos = [
        "Usa transporte público o bicicleta para reducir emisiones.",
        "Lleva tu propia botella reutilizable.",
        "Reduce el uso de bolsas plásticas y opta por bolsas de tela.",
        "Apaga luces y electrodomésticos cuando no los uses."
    ]
    await ctx.send("Consejo para reducir contaminación: " + random.choice(consejos))
@bot.command()
async def organizaciones(ctx):
    await ctx.send(
        "Aquí tienes algunas organizaciones destacadas para luchar contra la contaminación:\n"
        "- Greenpeace: 🌍 Enfocada en el cambio climático y la protección de los océanos. Más info: https://www.greenpeace.org/\n"
        "- WWF (World Wildlife Fund): 🐼 Protección de la biodiversidad. Más info: https://www.worldwildlife.org/\n"
        "- The Ocean Cleanup: 🌊 Iniciativa para limpiar plásticos del océano. Más info: https://theoceancleanup.com/"
    )
@bot.command()
async def impacto(ctx, tema=None):
    impactos = {
        "deforestacion": "La deforestación afecta la biodiversidad y contribuye al cambio climático. Cada año se pierden 10 millones de hectáreas de bosque.",
        "plasticos": "Se producen más de 300 millones de toneladas de plástico al año, y 8 millones terminan en el océano.",
        "energia": "El 60% de la electricidad mundial aún proviene de fuentes de energía no renovables."
    }
    if tema and tema.lower() in impactos:
        await ctx.send(impactos[tema.lower()])
    else:
        await ctx.send("Temas disponibles: deforestacion, plasticos, energia. Usa `$impacto [tema]` para más detalles.")
@bot.command()
async def acciones(ctx):
    acciones = [
        "Usa bombillas LED en lugar de incandescentes para ahorrar energía.",
        "Separa tus residuos en orgánicos, reciclables y no reciclables.",
        "Participa en campañas locales de limpieza o reforestación.",
        "Compra productos de comercio local para reducir tu huella de carbono.",
        "Reduce el uso de transporte privado y opta por caminar, usar bicicleta o transporte público."
    ]
    await ctx.send("Aquí tienes algunas acciones para combatir la contaminación:\n- " + "\n- ".join(acciones))

bot.run("DISCORD BOT TOKEN HERE")
