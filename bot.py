import os
import csv
import json
import logging
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

from telegram import (
    Update,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# -------------------------------
# LETTURA CALENDARIO 2026
# -------------------------------

def leggi_calendario():
    calendario = {}
    with open("calendario 2026 telegram.csv", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            calendario[row["data"].strip('"')] = row
    return calendario

calendario = leggi_calendario()

def contenuto_del_giorno():
    oggi = datetime.now().strftime("%Y-%m-%d")
    if oggi in calendario:
        return calendario[oggi]
    return None

# -------------------------------
# MENU PRINCIPALE
# -------------------------------

main_menu = ReplyKeyboardMarkup(
    [
        ["📖 Vangelo del giorno", "📜 Lettura del giorno"],
        ["🌅 Preghiera del mattino", "🌙 Preghiera della sera"],
        ["👼 Santo del giorno", "✨ Riflessione"],
        ["🌟 Rosario consigliato", "🙏 Novena del giorno"]
    ],
    resize_keyboard=True
)

# -------------------------------
# COMANDI
# -------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Benvenuto nel calendario spirituale 2026 🙏\nScegli una voce dal menu:",
        reply_markup=main_menu
    )

async def vangelo_del_giorno(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dati = contenuto_del_giorno()
    if dati:
        testo = f"📖 *Vangelo del giorno*\n\n{dati['vangelo']}"
    else:
        testo = "Non ho trovato il vangelo per oggi."
    await update.message.reply_text(testo, parse_mode="Markdown", reply_markup=main_menu)

async def lettura_del_giorno(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dati = contenuto_del_giorno()
    if dati:
        testo = f"📜 *Lettura del giorno*\n\n{dati['lettura']}"
    else:
        testo = "Non ho trovato la lettura per oggi."
    await update.message.reply_text(testo, parse_mode="Markdown", reply_markup=main_menu)

async def preghiera_mattino(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dati = contenuto_del_giorno()
    if dati:
        testo = f"🌅 *Preghiera del mattino*\n\n{dati['mattino']}"
    else:
        testo = "Non ho trovato la preghiera del mattino."
    await update.message.reply_text(testo, parse_mode="Markdown", reply_markup=main_menu)

async def preghiera_sera(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dati = contenuto_del_giorno()
    if dati:
        testo = f"🌙 *Preghiera della sera*\n\n{dati['sera']}"
    else:
        testo = "Non ho trovato la preghiera della sera."
    await update.message.reply_text(testo, parse_mode="Markdown", reply_markup=main_menu)

async def santo_del_giorno(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dati = contenuto_del_giorno()
    if dati:
        testo = f"👼 *Santo del giorno*\n\n{dati['santo']}"
    else:
        testo = "Non ho trovato il santo del giorno."
    await update.message.reply_text(testo, parse_mode="Markdown", reply_markup=main_menu)

async def riflessione(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dati = contenuto_del_giorno()
    if dati:
        testo = f"✨ *Riflessione*\n\n{dati['riflessione']}"
    else:
        testo = "Non ho trovato la riflessione per oggi."
    await update.message.reply_text(testo, parse_mode="Markdown", reply_markup=main_menu)

async def rosario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dati = contenuto_del_giorno()
    if dati:
        testo = f"🌟 *Rosario consigliato*\n\n{dati['rosario']}"
    else:
        testo = "Non ho trovato il rosario consigliato."
    await update.message.reply_text(testo, parse_mode="Markdown", reply_markup=main_menu)

async def novena_del_giorno(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dati = contenuto_del_giorno()
    if dati:
        testo = f"🙏 *Novena del giorno*\n\n{dati['novena']}"
    else:
        testo = "Non ho trovato la novena per oggi."
    await update.message.reply_text(testo, parse_mode="Markdown", reply_markup=main_menu)

# -------------------------------
# AVVIO BOT
# -------------------------------

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get("TELEGRAM_TOKEN")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Comandi
    app.add_handler(CommandHandler("start", start))

    # Pulsanti del menu
    app.add_handler(MessageHandler(filters.Text("📖 Vangelo del giorno"), vangelo_del_giorno))
    app.add_handler(MessageHandler(filters.Text("📜 Lettura del giorno"), lettura_del_giorno))
    app.add_handler(MessageHandler(filters.Text("🌅 Preghiera del mattino"), preghiera_mattino))
    app.add_handler(MessageHandler(filters.Text("🌙 Preghiera della sera"), preghiera_sera))
    app.add_handler(MessageHandler(filters.Text("👼 Santo del giorno"), santo_del_giorno))
    app.add_handler(MessageHandler(filters.Text("✨ Riflessione"), riflessione))
    app.add_handler(MessageHandler(filters.Text("🌟 Rosario consigliato"), rosario))
    app.add_handler(MessageHandler(filters.Text("🙏 Novena del giorno"), novena_del_giorno))

    app.run_polling()

if __name__ == "__main__":
    main()
