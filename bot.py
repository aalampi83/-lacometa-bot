import os
import json
import logging
import feedparser

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN")

RSS_VANGELO = "https://www.vaticannews.va/it/evangelii.xml"
RSS_LETTURA = "https://www.vaticannews.va/it/rss.xml"

NEGOZIO_URL = "https://www.lacometaarticolireligiosi.it/"
BLOG_URL = "https://www.lacometaarticolireligiosi.it/blog-e-news"


def get_first_entry_text(url: str) -> str | None:
    feed = feedparser.parse(url)
    if not feed.entries:
        return None
    entry = feed.entries[0]
    titolo = entry.title
    testo = getattr(entry, "summary", getattr(entry, "description", ""))
    return f"📖 *{titolo}*\n\n{testo}"


def load_subscribers():
    try:
        with open("subscribers.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_subscribers(subs):
    with open("subscribers.json", "w", encoding="utf-8") as f:
        json.dump(subs, f)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
    [InlineKeyboardButton("📖 Vangelo del giorno", callback_data="vangelo")],
    [InlineKeyboardButton("📚 Lettura del giorno", callback_data="lettura")],
    [InlineKeyboardButton("🙏 Preghiera del mattino", callback_data="mattino")],
    [InlineKeyboardButton("🌙 Preghiera della sera", callback_data="sera")],
    [InlineKeyboardButton("✝️ Santo del giorno", callback_data="santo")],
    [InlineKeyboardButton("💭 Riflessione", callback_data="riflessione")],
    [InlineKeyboardButton("📿 Rosario", callback_data="rosario")],
    [InlineKeyboardButton("🕊️ Novena del giorno", callback_data="novena")],
    [InlineKeyboardButton("📬 Iscriviti al Vangelo quotidiano", callback_data="iscriviti")],
    [InlineKeyboardButton("❌ Disiscriviti", callback_data="disiscriviti")],
    [InlineKeyboardButton("🛍️ Visita il negozio", url=NEGOZIO_URL)],
    [InlineKeyboardButton("📘 Visita il blog", url=BLOG_URL)],
]

      
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "🌟 Benvenuto in *La Cometa Articoli Religiosi*!\n\n"
        "Ogni giorno trovi qui il Vangelo, le letture e le preghiere.\n"
        "Scegli cosa vuoi leggere oggi 👇"
    )

    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    chat_id = query.message.chat_id

    if data == "vangelo":
        text = get_first_entry_text(RSS_VANGELO)
        if text:
            await query.edit_message_text(text, parse_mode="Markdown")
        else:
            await query.edit_message_text("Non è stato possibile caricare il Vangelo. Riprova più tardi.")

    elif data == "lettura":
        text = get_first_entry_text(RSS_LETTURA)
        if text:
            await query.edit_message_text(text, parse_mode="Markdown")
        else:
            await query.edit_message_text("Non è stato possibile caricare la lettura. Riprova più tardi.")

    elif data == "iscriviti":
        subs = load_subscribers()
        if chat_id not in subs:
            subs.append(chat_id)
            save_subscribers(subs)
            await query.edit_message_text("📬 Ti sei iscritto al Vangelo quotidiano delle 7.")
        else:
            await query.edit_message_text("Sei già iscritto al Vangelo quotidiano.")

    elif data == "disiscriviti":
        subs = load_subscribers()
        if chat_id in subs:
            subs.remove(chat_id)
            save_subscribers(subs)
            await query.edit_message_text("❌ Hai disattivato il Vangelo quotidiano.")
        else:
            await query.edit_message_text("Non risulti iscritto al Vangelo quotidiano.")
elif data == "mattino":
    await query.edit_message_text("🙏 *Preghiera del mattino*\n\nSignore, ti offro questo nuovo giorno...", parse_mode="Markdown")

elif data == "sera":
    await query.edit_message_text("🌙 *Preghiera della sera*\n\nSignore, ti ringrazio per questa giornata...", parse_mode="Markdown")

elif data == "santo":
    await query.edit_message_text("✝️ *Santo del giorno*\n\n(qui inseriremo il santo del giorno)", parse_mode="Markdown")

elif data == "riflessione":
    await query.edit_message_text("💭 *Riflessione*\n\n(qui inseriremo una riflessione quotidiana)", parse_mode="Markdown")

elif data == "rosario":
    await query.edit_message_text("📿 *Rosario*\n\n(qui inseriremo il testo del Rosario)", parse_mode="Markdown")

elif data == "novena":
    await query.edit_message_text("🕊️ *Novena del giorno*\n\n(qui inseriremo la novena)", parse_mode="Markdown")


def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN non impostato nelle variabili d'ambiente")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    # 🔔 Scheduler delle 7 lo aggiungeremo quando il bot sarà su PythonAnywhere

    app.run_polling()


if __name__ == "__main__":
    main()
