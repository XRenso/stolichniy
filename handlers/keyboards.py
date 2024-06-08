from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import (ReplyKeyboardBuilder, InlineKeyboardBuilder,
                                    InlineKeyboardButton, KeyboardButton)
from aiogram.filters.callback_data import CallbackData
import phr

class refferal_activate_callback(CallbackData,prefix='rfA'):
    refferal_code:str


class get_refferal_link(CallbackData,prefix='gRf'):
    refferal_code:str

#Главное меню
main_kb_builder = ReplyKeyboardBuilder()
my_profile = KeyboardButton(text=phr.my_profile)
about_me = KeyboardButton(text=phr.create_referal)
main_kb_builder.add(about_me).add(my_profile)

go_to_tg_channel_btn = InlineKeyboardButton(text=phr.stolichniy_channel_url,url='https://t.me/stolichi')
def get_refferal_kb(reff_code):
    markup = InlineKeyboardBuilder()
    i_subscribed_button = InlineKeyboardButton(text=phr.i_subscribed,callback_data=refferal_activate_callback(refferal_code=reff_code).pack())
    return markup.add(go_to_tg_channel_btn).add(i_subscribed_button).as_markup()


channel_url_kb = InlineKeyboardBuilder().add(go_to_tg_channel_btn).as_markup()


