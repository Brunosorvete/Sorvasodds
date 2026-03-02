from telegram import Bot
from analysis import analisar_jogos
from datetime import datetime
import schedule
import time
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

def enviar_relatorio():
    oportunidades = analisar_jogos()

    if not oportunidades:
        mensagem = "📊 Nenhuma oportunidade acima de 60% hoje."
    else:
        mensagem = f"📊 RELATÓRIO DIÁRIO - {datetime.now().strftime('%d/%m/%Y')}\n\n"
        for op in oportunidades:
            mensagem += f"⚽ {op['jogo']}\n📈 Over 2.5: {op['prob']}%\n\n"

    bot.send_message(chat_id=CHAT_ID, text=mensagem)

schedule.every().day.at("09:00").do(enviar_relatorio)

while True:
    schedule.run_pending()
    time.sleep(60)
