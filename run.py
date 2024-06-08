from loader import dp,bot, set_default_commands, db
import asyncio
import logging
import sys
from handlers import start,refferal, text_commands, inline_mode





async def main():
    dp.include_router(start.router)
    dp.include_router(refferal.router)
    dp.include_router(text_commands.router)
    dp.include_router(inline_mode.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())