from aiogram.utils import executor

from .bot import dp, startup, shutdown

executor.start_polling(dp, on_startup=startup, on_shutdown=shutdown)
