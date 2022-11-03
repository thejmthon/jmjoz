import sys

from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from telethon.sessions import StringSession

from ..Config import Config
from .client import JmthonClient

__version__ = "2.10.6"

loop = None

if Config.STRING_SESSION:
    session = StringSession(str(Config.STRING_SESSION))
else:
    session = "jmthon"

try:
    sbb_b = JmthonClient(
        session=session,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        loop=loop,
        app_version=__version__,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )
except Exception as e:
    print(f"STRING_SESSION WRONG PLZ MAKE A NEW SESSION - {e}\n كود سيشن تيليثون الذي وضعته غير صالح")
    sys.exit()


sbb_b.tgbot = tgbot = JmthonClient(
    session="jmthonTgbot",
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    loop=loop,
    app_version=__version__,
    connection=ConnectionTcpAbridged,
    auto_reconnect=True,
    connection_retries=None,
).start(bot_token=Config.TG_BOT_TOKEN)

except Exception as e:
    print(f"توكن البوت الخاص بك غير صحيح او وضعته بشكل خاطئ يرجى صنع بوت جديد واضافه قيمته")
    sys.exit()
