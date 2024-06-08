from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import (ReplyKeyboardBuilder, InlineKeyboardBuilder,
                                    InlineKeyboardButton, KeyboardButton)
from aiogram.utils.deep_linking import decode_payload,create_start_link
from loader import bot,db
from aiogram import types
import phr
from aiogram.exceptions import TelegramBadRequest
from handlers import keyboards as kb
router = Router()





@router.callback_query(kb.get_refferal_link.filter())
async def get_refferal_link(call:types.CallbackQuery, callback_data: kb.get_refferal_link):
    reff_code = callback_data.refferal_code

    refferal = db.get_refferal_by_code(int(reff_code))
    settings = db.get_refferal_setting(refferal['reff_code'])
    markup = InlineKeyboardBuilder()
    reward_type = 'За каждого приглашенного'
    level = ''
    if not settings['per_user']:
        reward_type = 'За определенное количество приглашенных'
        if len(refferal["activators"]) < sorted(list(map(int,settings['levels'])))[-1]:
            for i in sorted(list(map(int,settings['levels']))):
                if i > len(refferal["activators"]):
                    level = f'До следующего уровня осталось - {i -len(refferal["activators"]) }'
        else:
            level = 'Вы достигли максимального уровня'
    markup.add(InlineKeyboardButton(text='Поделиться', switch_inline_query=f'/refs {settings["code"]}'))
    await call.message.edit_text(text=f'Информация про реферальную ссылку\nНазвание - {settings["name"]}\n\n'
                                      f'Описание - {settings["description"]}\n\n'
                                      f'Сколько активировало - {len(refferal["activators"])}\n\n'
                                      f'За что выдают - {reward_type}\n\n'
                                      f'{level}',reply_markup=markup.as_markup())

@router.callback_query(kb.refferal_activate_callback.filter())
async def activate_refferal(call:types.CallbackQuery, callback_data: kb.refferal_activate_callback):
    reff_code = callback_data.refferal_code
    try:
        is_subscribed = await bot.get_chat_member(chat_id=phr.tg_channel_id,
                                                  user_id=call.message.chat.id)
        if is_subscribed.status !='left':
            refferal = db.get_refferal_by_code(int(reff_code))
            sender = db.get_user(refferal['creator'])
            activator = db.get_user(call.message.chat.id)
            db.activate_refferal(int(reff_code),activator['user_id'])
            await call.message.edit_text(f'Вы успешно активировали реферальную ссылку {sender["fullname"]}!\nПоздравляем')
            reff_settings = db.get_refferal_setting(refferal['reff_code'])
            refferal = db.get_refferal_by_code(int(reff_code))
            info = ''
            if not reff_settings['per_user']:
                levels = sorted(list(map(int,list(reff_settings['levels']))))
                if len(refferal['activators']) <= levels[-1]:
                    for lvl in levels:
                        if int(lvl) == len(refferal['activators']):
                            db.add_bonuses(sender['user_id'],int(reff_settings['levels'][str(lvl)]))
                            info = f'Вам засчислили {reff_settings["levels"][str(lvl)]} бонусов!!!!'
                            if levels.index(lvl) != len(levels)-1:
                                info+=f'\nДо следующего уровня нужно {int(levels[levels.index(lvl)+1])-len(refferal["activators"])}'
                                break
                            else:
                                info+=f'\nВы достигли максимального уровня своей реферальной ссылки. Поздравляем!!'

                            break
                        else:
                            info+=f'\nДо следующего уровня нужно {int(levels[levels.index(lvl)])-len(refferal["activators"])}'

            else:
                db.add_bonuses(sender['user_id'],int(reff_settings['per_user_bonus']))
                info = f'Вы получили {reff_settings["per_user_bonus"]} бонусов!!'
            await bot.send_message(chat_id=sender['user_id'],text=f'Вашу реферальную ссылку только что активировал {db.get_user(call.message.chat.id)["fullname"]}!\n{info}')
        else:
            await call.answer(text='Вы не подписались на каунал, проверьте ещё раз свою подписку!')

    except TelegramBadRequest:

        await call.answer(text='Вы не подписались на канал, проверьте ещё раз свою подписку!')