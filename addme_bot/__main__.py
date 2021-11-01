from uuid import uuid4
from typing import cast
from telegram import (
    Update,
    User,
    InlineQueryResultArticle,
    ParseMode,
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    CallbackContext,
    InlineQueryHandler,
    CallbackQueryHandler,
)
from telegram.utils.helpers import escape_markdown
from addme_bot import DISPATCHER, LOGGER, TOKEN, PORT, UPDATER, WEBHOOK, URL

from addme_bot.helpers import gen_message, in_or_out


def inlinequeryhandler(update: Update, _: CallbackContext) -> None:
    query = update.inline_query.query

    if query == "":
        return
    keyboard = [
        [
            InlineKeyboardButton(
                text="Add Me",
                callback_data={
                    "text": query,
                    "in": [],
                    "out": [],
                },
            ),
        ],
        [
            InlineKeyboardButton(
                text="Exclude Me",
                callback_data={
                    "text": query,
                    "in": [],
                    "out": [],
                },
            ),
        ],
    ]
    result = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Create New List",
            input_message_content=InputTextMessageContent(
                message_text=escape_markdown(query),
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN,
            ),
        )
    ]
    update.inline_query.answer(result)


def buttonhandler(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    data = cast(
        typ=tuple[str, list[tuple[int, str]], list[tuple[int, str]], str],
        val=update.callback_query.data,
    )
    if not isinstance(user, User):
        return
    in_list, out_list, response = in_or_out(data[3], user, data[1], data[2])
    context.bot.answer_callback_query(
        callback_query_id=update.callback_query.id,
        text=response,
        show_alert=False,
    )
    msg = gen_message(data[0], in_list, out_list)
    update.callback_query.edit_message_text(
        text=msg["text"],
        reply_markup=msg["reply_markup"],
        parse_mode=ParseMode.MARKDOWN,
    )


if __name__ == "__main__":
    LOGGER.info("Starting AddMe Bot")
    LOGGER.info("Adding Handlers...")
    DISPATCHER.add_handler(InlineQueryHandler(inlinequeryhandler))
    DISPATCHER.add_handler(CallbackQueryHandler(buttonhandler))
    if WEBHOOK:
        LOGGER.info("Starting Webhook...")
        UPDATER.start_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TOKEN,
            webhook_url=URL + TOKEN,
        )
    else:
        LOGGER.info("Using Long Polling...")
        UPDATER.start_polling()
    UPDATER.idle()
