# Powered By BikashHalder Or Aditya Halder IF You Fresh Any Problem To Contact The BgtRobot Owner
# Powered By @BikashHalder @AdityaHalder
# Ā©ļø Copy Right By Bikash Halder Or Aditya Halder
# Any Problem To Report @Bgt_Chat or @AdityaDiscus
# Bot Owner @BikashHalder Or @AdityaHalder

from pyrogram import filters
from pyrogram.types import Message

from Bikash.strings import get_command
from Bikash import app
from Bikash.misc import SUDOERS
from Bikash.utils.database.memorydatabase import (
    get_active_chats, get_active_video_chats)

# Commands
ACTIVEVC_COMMAND = get_command("ACTIVEVC_COMMAND")
ACTIVEVIDEO_COMMAND = get_command("ACTIVEVIDEO_COMMAND")


@app.on_message(filters.command(ACTIVEVC_COMMAND) & SUDOERS)
async def activevc(_, message: Message):
    mystic = await message.reply_text(
        "š„ ššš­š­š¢š§š  ššš­š¢šÆš ššØš¢šš šš”šš­š¬ š“āāļø\n\nš· šš„ššš¬š ššš¢š­ ššš° ššš..š„"
    )
    served_chats = await get_active_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except Exception:
            title = "š šš«š¢šÆšš­š šš”šš­ š„"
        if (await app.get_chat(x)).username:
            user = (await app.get_chat(x)).username
            text += f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n"
        else:
            text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
        j += 1
    if not text:
        await mystic.edit_text("š ššØ ššš­š¢šÆš  šš šš§ šš š­ šš®š¬š¢š ššØš­ ā")
    else:
        await mystic.edit_text(
            f"š šš š­ šš®š¬š¢š šš®š«š«šš§š­ šššÆš¢š­š ššØš¢šš šš”šš­š¬ šš¢š¬š­ š° :-**\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(ACTIVEVIDEO_COMMAND) & SUDOERS)
async def activevi_(_, message: Message):
    mystic = await message.reply_text(
        "š„ ššš­š­š¢š§š  ššš­š¢šÆš ššØš¢šš šš”šš­š¬ š“āāļø\n\nš· šš„ššš¬š ššš¢š­ ššš° ššš..š„"
    )
    served_chats = await get_active_video_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except Exception:
            title = "š„ šš«š¢šÆšš­š šš”šš­ š„"
        if (await app.get_chat(x)).username:
            user = (await app.get_chat(x)).username
            text += f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n"
        else:
            text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
        j += 1
    if not text:
        await mystic.edit_text("š ššØ ššš­š¢šÆš  šš šš§ šš š­ šš®š¬š¢š ššØš­ ā")
    else:
        await mystic.edit_text(
            f"š šš š­ šš®š¬š¢š šš®š«š«šš§š­ šššÆš¢š­š ššØš¢šš šš”šš­š¬ šš¢š¬š­ š° :-**\n\n{text}",
            disable_web_page_preview=True,
        )
