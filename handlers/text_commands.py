from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import (ReplyKeyboardBuilder, InlineKeyboardBuilder,
                                    InlineKeyboardButton, KeyboardButton)
from aiogram.utils.deep_linking import decode_payload,create_start_link
from loader import bot,db
import phr
from handlers import keyboards as kb
router = Router()

@router.message(F.text)
async def text_cmd(message:Message):
    match message.text:

        case phr.create_referal:
            r = db.get_all_user_refferals(message.from_user.id)

            if len(r):

                markup = InlineKeyboardBuilder()
                for reff in r:
                    settings = db.get_refferal_setting(reff['reff_code'])
                    markup.add(InlineKeyboardButton(text=settings['name'],callback_data=kb.get_refferal_link(refferal_code=str(reff['code'])).pack()))
                await message.answer('Ваши реферальный ссылки',reply_markup=markup.as_markup())

            else:
                link = await create_start_link(bot, db.create_refferal(message.from_user.id, 'new_user'), encode=True)
                markup = InlineKeyboardBuilder()
                markup.add(InlineKeyboardButton('Поделиться',switch_inline_query='/refs new_user'))
                await message.answer('Ваша реферальная ссылка готова. Нажмите поделиться, чтобы её использовать.',reply_markup=markup.as_markup())

        case phr.my_profile:
            user = db.get_user(message.from_user.id)
            await message.answer(f'Ваша информация, {user["fullname"]}!\n\n'
                                 f'Ваше количество реферальных ссылок - {len(db.get_all_user_refferals(user["user_id"]))}\n\n'
                                 f'Количество приглашенных пользователей - {sum([len(i["activators"]) for i in db.get_all_user_refferals(user["user_id"])])}\n\n'
                                 f'У вас {user["bonuses"]} бонусов!!!')