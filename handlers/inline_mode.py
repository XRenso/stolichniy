import aiogram
from loader import db,dp,bot
from handlers import keyboards as kb
from aiogram import types
from aiogram.utils.deep_linking import decode_payload,create_start_link
from aiogram import Router
import hashlib
from aiogram.types import InlineKeyboardMarkup , InlineQueryResultArticle, InputTextMessageContent
from aiogram.utils.keyboard import (ReplyKeyboardBuilder, InlineKeyboardBuilder,
                                    InlineKeyboardButton, KeyboardButton)

router = Router()

@router.inline_query()
async def send_refferal(inline_query:types.InlineQuery):
    text = inline_query.query or '/refs'
    if '/refs' == text.split()[0]:
        if len(text.split()) == 1:
            reffs = db.get_all_user_refferals(inline_query.from_user.id)
            results = []
            if reffs != 0:
                results = []
                for i in reffs:
                    settings = db.get_refferal_setting(i['reff_code'])
                    link = await create_start_link(bot, i['code'], encode=True)
                    markup = InlineKeyboardBuilder().add(InlineKeyboardButton(text='Активировать реферальную ссылку', url=link))
                    caption = f'Примени мою реферальную ссылку столичного по кнопке ниже:'
                    item = InlineQueryResultArticle(
                        id=str(i['_id']),
                        title=settings['name'],
                        description=settings['description'],
                        reply_markup=markup.as_markup(),
                        input_message_content=InputTextMessageContent(message_text=caption)
                    )
                    results.append(item)

        else:
            results = []
            refferal = db.get_refferal_by_user_id(user_id=inline_query.from_user.id,settings_code=text.split()[1])

            if refferal:
                settings = db.get_refferal_setting(refferal['reff_code'])
                link = await create_start_link(bot, refferal['code'], encode=True)
                markup = InlineKeyboardBuilder().add(
                    InlineKeyboardButton(text='Активировать реферальную ссылку', url=link))
                caption = f'Примени мою реферальную ссылку столичного по кнопке ниже:'
                item = InlineQueryResultArticle(
                    id=str(refferal['_id']),
                    title=settings['name'],
                    description=settings['description'],
                    reply_markup=markup.as_markup(),
                    input_message_content=InputTextMessageContent(message_text=caption)
                )
                results.append(item)
    await bot.answer_inline_query(inline_query.id,results,cache_time=1)