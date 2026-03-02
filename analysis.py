import requests
from scipy.stats import poisson
import os
from datetime import datetime

API_KEY = os.getenv("API_KEY")

HEADERS = {
    "x-apisports-key": API_KEY
}

def calcular_over25(lambda_home, lambda_away):
    prob = 0
    for i in range(6):
        for j in range(6):
            if i + j > 2:
                prob += poisson.pmf(i, lambda_home) * poisson.pmf(j, lambda_away)
    return prob

def buscar_jogos():
    hoje = datetime.now().strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?date={hoje}"
    response = requests.get(url, headers=HEADERS)
    return response.json()["response"]

def analisar_jogos():
    jogos = buscar_jogos()
    oportunidades = []

    for jogo in jogos:
        home = jogo["teams"]["home"]["name"]
        away = jogo["teams"]["away"]["name"]

        # ⚠️ Temporário (depois puxamos médias reais)
        lambda_home = 1.6
        lambda_away = 1.4

        prob = calcular_over25(lambda_home, lambda_away)

        if prob > 0.60:
            oportunidades.append({
                "jogo": f"{home} x {away}",
                "prob": round(prob*100, 2)
            })

    oportunidades.sort(key=lambda x: x["prob"], reverse=True)
    return oportunidades[:5]
