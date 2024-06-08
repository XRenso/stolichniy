from aiogram.methods.get_chat_member import GetChatMember, ChatMemberLeft
from aiogram import Router
from aiogram.filters import Command
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.deep_linking import decode_payload,create_start_link
from aiogram.exceptions import TelegramBadRequest
import phr
from loader import bot,db
from handlers import keyboards as kb
router = Router()

@router.message(Command("start"))
async def start(message:Message,command: CommandObject):
    #Переход по рефералке
    if command.args:
        reff_code = decode_payload(command.args)

        refferal = db.get_refferal_by_code(int(reff_code))

        reff_settings = db.get_refferal_setting(refferal['reff_code'])
        if message.from_user.id != refferal['creator']:
            if message.from_user.id not in refferal['activators']:
                if reff_settings['only_new_user']:
                    if not db.get_user(message.from_user.id):
                        try:
                            is_subscribed = await bot.get_chat_member(chat_id=phr.tg_channel_id,
                                                                      user_id=message.from_user.id)
                            if is_subscribed.status != 'left':
                                db.activate_refferal(refferal['code'],message.from_user.id)
                                await message.answer('Вы активировали реферальный код. Поздравляем.')
                                db.create_user(fullname=message.from_user.full_name,user_id=message.from_user.id)
                                refferal = db.get_refferal_by_code(int(reff_code))
                                sender = db.get_user(refferal['creator'])
                                info = ''
                                if not reff_settings['per_user']:
                                    levels = sorted(list(map(int, list(reff_settings['levels']))))
                                    if len(refferal['activators']) <= levels[-1]:
                                        for lvl in levels:
                                            if int(lvl) == len(refferal['activators']):
                                                db.add_bonuses(sender['user_id'],
                                                               int(reff_settings['levels'][str(lvl)]))
                                                info = f'Вам засчислили {reff_settings["levels"][str(lvl)]} бонусов!!!!'
                                                if levels.index(lvl) != len(levels) - 1:
                                                    info += f'\nДо следующего уровня нужно {int(levels[levels.index(lvl) + 1]) - len(refferal["activators"])}'
                                                    break
                                                else:
                                                    info += f'\nВы достигли максимального уровня своей реферальной ссылки. Поздравляем!!'

                                                break
                                            else:
                                                info += f'\nДо следующего уровня нужно {int(levels[levels.index(lvl)]) - len(refferal["activators"])}'

                                else:
                                    db.add_bonuses(sender['user_id'], int(reff_settings['per_user_bonus']))
                                    info = f'Вы получили {reff_settings["per_user_bonus"]} бонусов!!'






                            else:
                                db.create_user(fullname=message.from_user.full_name, user_id=message.from_user.id)
                                await message.answer(
                                    text='Вы совсем скоро сможете использовать реферальный код. Осталось только подписаться',
                                    reply_markup=kb.get_refferal_kb(reff_code))

                        except TelegramBadRequest:
                            db.create_user(fullname=message.from_user.full_name,user_id=message.from_user.id)
                            await message.answer(text='Вы совсем скоро сможете использовать реферальный код. Осталось только подписаться', reply_markup=kb.get_refferal_kb(reff_code))
                    else:
                        await message.answer('Данный реферальный код работает только для новых пользователей')
                else:
                    pass

            else:
                await message.answer('Вы уже использовали реферальную ссылку')
        else:
            await message.answer(f'Вы не можете использовать собственную рефферальную ссылку')
        # await message.answer(f'Вы прошли по реферальной ссылке пользователя - {reff_id}', reply_markup=kb.main_kb_builder.as_markup(resize_keyboard=True))
    #Просто старт
    else:
        await message.answer(f'Здравствуй, {message.from_user.full_name}! 🎁\n️Любишь скидки - жми Пригласить друга 🔝\n❓Сколько у тебя накопилось - жми Узнать скидку 👍🏻 ',reply_markup=kb.main_kb_builder.as_markup(resize_keyboard=True))
        db.create_user(fullname=message.from_user.full_name,user_id=message.from_user.id)
        try:
            is_subscribed = await bot.get_chat_member(chat_id=phr.tg_channel_id,user_id=message.from_user.id)
            if is_subscribed.status == 'left':
                await message.answer(text=phr.please_subscribe, reply_markup=kb.channel_url_kb)


        except TelegramBadRequest:
            await message.answer(text=phr.please_subscribe,reply_markup=kb.channel_url_kb)
