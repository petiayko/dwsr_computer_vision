from typing import Optional

from bot.constants import *
from bot.logs import log_init
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, filters

logger = log_init()


async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(
        f'Starting /start by {update.effective_user.first_name} {update.effective_user.last_name} '
        f'({update.effective_user.id})')

    reply_keyboard = [['Распознать картинку', 'Помощь']]
    user = update.effective_user
    await update.message.reply_html(
        text=rf'Здравствуйте, {user.mention_html()}',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, is_persistent=True, resize_keyboard=True
        ),
    )


async def help_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(
        f'Starting /help by {update.effective_user.first_name} {update.effective_user.last_name} '
        f'({update.effective_user.id})')
    await update.message.reply_text('Мне бы кто помог...')

    return ConversationHandler.END


async def recognize_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(
        f'Starting /recognize by {update.effective_user.first_name} {update.effective_user.last_name} '
        f'({update.effective_user.id})')
    await update.message.reply_text('Пришлите изображение. Бот определит, на нем кошка или собака')

    return SENDING_PHOTO


async def unknown_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(
        f'Unknown command by {update.effective_user.first_name} {update.effective_user.last_name} '
        f'({update.effective_user.id})')
    await update.message.reply_text('Неизвестная команда!')


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Optional[int]:
    logger.info(
        f'Echo by {update.effective_user.first_name} {update.effective_user.last_name} ({update.effective_user.id})')
    if update.message.text == 'Помощь':
        return await help_command_handler(update, context)
    if update.message.text == 'Распознать картинку':
        return await recognize_command_handler(update, context)
    else:
        await update.message.reply_text('Не пишите сюда больше.')


async def picture_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(
        f'Picture to recognize by {update.effective_user.first_name} {update.effective_user.last_name} '
        f'({update.effective_user.id})')
    await update.message.reply_text('Вы прислали фото!')

    return ConversationHandler.END


async def other_content_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(
        f'Some content by {update.effective_user.first_name} {update.effective_user.last_name} '
        f'({update.effective_user.id})')
    await update.message.reply_text('Не присылайте такое больше.')


def start():
    application = Application.builder().token(os.environ['TOKEN']).build()

    start_hlr = CommandHandler('start', start_command_handler)
    help_hlr = CommandHandler('help', help_command_handler)
    recognize_hlr = CommandHandler('recognize', recognize_command_handler)
    unknown_hlr = MessageHandler(filters.COMMAND, unknown_command_handler)
    text_hlr = MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler)
    picture_hlr = MessageHandler(filters.PHOTO, picture_handler)
    other_hlr = MessageHandler(filters.ALL, other_content_handler)
    conv_hlr = ConversationHandler(
        entry_points=[recognize_hlr, text_hlr],
        states={SENDING_PHOTO: [picture_hlr], },
        fallbacks=[start_hlr, help_hlr, recognize_hlr, unknown_hlr, text_hlr, other_hlr, ],
    )

    application.add_handler(start_hlr)
    application.add_handler(help_hlr)
    application.add_handler(conv_hlr)
    application.add_handler(unknown_hlr)
    application.add_handler(text_hlr)
    application.add_handler(other_hlr)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
