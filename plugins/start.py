# Powered By @BikashHalder @AdityaHalder
# ÂŠī¸ Copy Right By Bikash Halder Or Aditya Halder
# Any Problem To Report @Bgt_Chat or @AdityaDiscus
# Bot Owner @BikashHalder Or @AdityaHalder

import asyncio

from pyrogram import filters
from pyrogram.types import (InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)
from youtubesearchpython.__future__ import VideosSearch
from Bikash import app
from Bikash import config
from Bikash.config import BANNED_USERS
from Bikash.config.config import OWNER_ID
from Bikash.strings import get_command, get_string
from Bikash import Telegram, YouTube, app
from Bikash.misc import SUDOERS
from plugins.playlist import del_plist_msg
from plugins.sudoers import sudoers_list
from Bikash.utils.database import (add_served_chat,
                                       add_served_user,
                                       blacklisted_chats,
                                       get_assistant, get_lang,
                                       get_userss, is_on_off,
                                       is_served_private_chat)
from Bikash.utils.decorators.language import LanguageStart
from Bikash.utils.inline import (help_pannel, private_panel,
                                     start_pannel)

loop = asyncio.get_running_loop()


@app.on_message(
    filters.command(["start"])
    & filters.private
    & ~filters.edited
    & ~BANNED_USERS
)
@LanguageStart
async def start_comm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            return await message.reply_text(
                _["help_1"], reply_markup=keyboard
            )
        if name[0:4] == "song":
            return await message.reply_text(_["song_2"])
        if name[0:3] == "sta":
            m = await message.reply_text(
                "đ đđđ­đđĄđĸđ§đ  đđ¨đŽđĢ đđđĢđŦđ¨đ§đđĨ đđ­đđ­đŦ đ.!"
            )
            stats = await get_userss(message.from_user.id)
            tot = len(stats)
            if not stats:
                await asyncio.sleep(1)
                return await m.edit(_["ustats_1"])

            def get_stats():
                msg = ""
                limit = 0
                results = {}
                for i in stats:
                    top_list = stats[i]["spot"]
                    results[str(i)] = top_list
                    list_arranged = dict(
                        sorted(
                            results.items(),
                            key=lambda item: item[1],
                            reverse=True,
                        )
                    )
                if not results:
                    return m.edit(_["ustats_1"])
                tota = 0
                videoid = None
                for vidid, count in list_arranged.items():
                    tota += count
                    if limit == 10:
                        continue
                    if limit == 0:
                        videoid = vidid
                    limit += 1
                    details = stats.get(vidid)
                    title = (details["title"][:35]).title()
                    if vidid == "telegram":
                        msg += f"đĄī¸[đđđĨđđ đĢđđĻ đđđđĸđ đ](https://t.me/telegram) **đ đđĨđđ˛đđ {count} âąī¸ đđĸđĻđđŦ**\n\n"
                    else:
                        msg += f"đĄī¸ [{title}](https://www.youtube.com/watch?v={vidid}) **đ đđĨđđ˛đđ {count} âąī¸ đđĸđĻđđŦ**\n\n"
                msg = _["ustats_2"].format(tot, tota, limit) + msg
                return videoid, msg

            try:
                videoid, msg = await loop.run_in_executor(
                    None, get_stats
                )
            except Exception as e:
                print(e)
                return
            thumbnail = await YouTube.thumbnail(videoid, True)
            await m.delete()
            await message.reply_photo(photo=thumbnail, caption=msg)
            return
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(config.LOG):
                sender_id = message.from_user.id
                sender_name = message.from_user.first_name
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"{message.from_user.mention} đđđŦ đđŽđŦđ­ đđ­đđĢđ­đđ đđĸđ¤đđŦđĄ đđŽđŦđĸđ đđ¨đ­ đđ¨ đđĄđđđ¤ <code>SUDOLIST</code>\n\n**đ đđŦđđĢ đđ:** {sender_id}\n**đ đđŦđđĢ đđđĻđ:** {sender_name}",
                )
            return
        if name[0:3] == "lyr":
            query = (str(name)).replace("lyrics_", "", 1)
            lyrical = config.lyrical
            lyrics = lyrical.get(query)
            if lyrics:
                return await Telegram.send_split_text(message, lyrics)
            else:
                return await message.reply_text(
                    "âī¸ đđđĸđĨđđ đđ¨ đđđ­ đđ˛đĢđĸđđŦ â."
                )
        if name[0:3] == "del":
            await del_plist_msg(client=client, message=message, _=_)
        if name[0:3] == "inf":
            m = await message.reply_text("đ đđđ­đđĄđĸđ§đ  Info!")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[
                    0
                ]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = f"""
__**đˇ đđĸđ¤đđŦđĄ đđĸđđđ¨ đđĢđđđ¤ đđ§đđ¨đĢđĻđđ­đĸđ¨đ§ đˇ**__
                        
                â° đđĸđ¤đđŦđĄ âī¸ đđĨđđ˛đđĢ âą
                        
đ**đđĸđ­đĨđ:** {title}

âąī¸**đđŽđĢđđ­đĸđ¨đ§:** {duration} Mins
đ**đđĸđđ°đŦ:** `{views}`
â°**đđŽđđĨđĸđŦđĄđđ đđĸđĻđ:** {published}
đĄ**đđĄđđ§đ§đđĨ đđđĻđ:** {channel}
đĄ **đđĄđđ§đ§đđĨ đđĸđ§đ¤:** [đ đđĸđđ° đđĄđđ§đ§đđĨ đĄ]({channellink})
đĄī¸ **đđĸđđđ¨ đđĸđ§đ¤:** [đ đđĸđ§đ¤ đ]({link})

đī¸ đđđđĢđđĄđđ đđ¨đ°đđĢđđ đđ˛ đˇ {Bikash.config.MUSIC_BOT_NAME}__"""
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="đˇ đđđ­đđĄ đē", url=f"{link}"
                        ),
                        InlineKeyboardButton(
                            text="â đđĨđ¨đŦđ â", callback_data="close"
                        ),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=key,
            )
            if await is_on_off(Bikash.config.LOG):
                sender_id = message.from_user.id
                sender_name = message.from_user.first_name
                return await app.send_message(
                    Bikash.config.LOG_GROUP_ID,
                    f"{message.from_user.mention} đđđŦ đđŽđŦđ­ đđ­đđĢđ­đđ đđĸđ¤đđŦđĄ đđŽđŦđĸđ đđ¨đ­ đĩ  đđ¨ đđĄđđđ¤ <code>đĨ đđĸđđđ¨ đđ§đđ¨đĢđĻđđ­đĸđ¨đ§</code>\n\n**đ đđŦđđĢ đđ:** {sender_id}\n**đ đđŦđđĢ đđđĻđ:** {sender_name}",
                )
    else:
        try:
            await app.resolve_peer(OWNER_ID[0])
            OWNER = OWNER_ID[0]
        except:
            OWNER = None
        out = private_panel(_, app.username, OWNER)
        if config.START_IMG_URL:
            try:
                await message.reply_photo(
        photo=f"https://te.legra.ph/file/99d0261f0aa5512ad6753.png",
        caption=f"""**ââââââââââââââââââââââââ
đĨ đđđĨđĨđ¨, đ đđĻ đđŽđŠđđĢđđđŦđ­ đđĸđ đĄ đđŽđđĨđĸđ­đ˛
đđ¨ đđđ  đđ đđŽđŦđĸđ đđĨđđ˛đđĢ đđ¨đ­.

âââââââââââââââââââ
âŖâ đđ°đ§đđĢ'đąđ : [đđĸđ¤đđŦđĄ đđđĨđđđĢ](https://t.me/BikashHalder)
âŖâ đđ°đ§đđĢ'đąđ : [đđđĸđ­đ˛đ đđđĨđđđĢ](https://t.me/AdityaHalder)
âŖâ đđŠđđđ­đđŦ Âģ : [đđ đ­ đđđđĸđđĸđđĨ](https://t.me/BikashGadgetsTech)
âŖâ đđŽđŠđŠđ¨đĢđ­ Âģ : [đđ đ­ đđĄđđ­](https://t.me/Bgt_Chat)
âŖâ đđĄđđ­đ¸ Âģ : [đđđĸđ­đ˛đ đđĸđŦđđŽđŦ](https://t.me/AdityaDiscus)
âââââââââââââââââââ

đ đđŽđŦđ­ đđđ đđ Âģ đđ¨ đđ¨đŽđĢ đđĢđ¨đŽđŠ đđ§đ
đđ§đŖđ¨đ˛ đđŽđŠđđĢ đđŽđđĨđĸđ­đ˛ âĨī¸đđŽđŦđĸđ.
ââââââââââââââââââââââââ**""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "â â° đđđ đđ đđ¨ đđ¨đŽđĢ đđĢđ¨đŽđŠ âą â", url=f"https://t.me/{app.username}?startgroup=true"),
                ],
                [
                    InlineKeyboardButton(
                        "đē â° đđĢđ¨đĻđ¨đ­đĸđ¨đ§ âą đē", url=f"https://youtube.com/channel/UCUkj6FFzdsOO5acUXVOEECg"),
                ],
                [
                    InlineKeyboardButton(
                        text="âī¸ â° đđŠđđ§ đđ¨đĻđĻđđ§đđŦ đđđ§đŽ âą âī¸", callback_data="settings_back_helper")
                ]
           ]
        ),
                  )
            except:
                await message.reply_photo(
        photo=f"https://te.legra.ph/file/99d0261f0aa5512ad6753.png",
        caption=f"""**ââââââââââââââââââââââââ
đĨ đđđĨđĨđ¨, đ đđĻ đđŽđŠđđĢđđđŦđ­ đđĸđ đĄ đđŽđđĨđĸđ­đ˛
đđ¨ đđđ  đđ đđŽđŦđĸđ đđĨđđ˛đđĢ đđ¨đ­.

âââââââââââââââââââ
âŖâ đđ°đ§đđĢ'đąđ : [đđĸđ¤đđŦđĄ đđđĨđđđĢ](https://t.me/BikashHalder)
âŖâ đđ°đ§đđĢ'đąđ : [đđđĸđ­đ˛đ đđđĨđđđĢ](https://t.me/AdityaHalder)
âŖâ đđŠđđđ­đđŦ Âģ : [đđ đ­ đđđđĸđđĸđđĨ](https://t.me/BikashGadgetsTech)
âŖâ đđŽđŠđŠđ¨đĢđ­ Âģ : [đđ đ­ đđĄđđ­](https://t.me/Bgt_Chat)
âŖâ đđĄđđ­đ¸ Âģ : [đđđĸđ­đ˛đ đđĸđŦđđŽđŦ](https://t.me/AdityaDiscus)
âââââââââââââââââââ

đ đđŽđŦđ­ đđđ đđ Âģ đđ¨ đđ¨đŽđĢ đđĢđ¨đŽđŠ đđ§đ
đđ§đŖđ¨đ˛ đđŽđŠđđĢ đđŽđđĨđĸđ­đ˛ âĨī¸đđŽđŦđĸđ.
ââââââââââââââââââââââââ**""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "â â° đđđ đđ đđ¨ đđ¨đŽđĢ đđĢđ¨đŽđŠ âą â", url=f"https://t.me/{app.username}?startgroup=true"),
                ],
                [
                    InlineKeyboardButton(
                        "đē â° đđĢđ¨đĻđ¨đ­đĸđ¨đ§ âą đē", url=f"https://youtube.com/channel/UCUkj6FFzdsOO5acUXVOEECg"),
                ],
                [
                    InlineKeyboardButton(
                        text="â â° đđŠđđ§ đđ¨đĻđĻđđ§đđŦ đđđ§đŽ âą â", callback_data="settings_back_helper")
                ]
           ]
        ),
              )
        else:
            await message.reply_photo(
        photo=f"https://te.legra.ph/file/99d0261f0aa5512ad6753.png",
        caption=f"""**ââââââââââââââââââââââââ
đĨ đđđĨđĨđ¨, đ đđĻ đđŽđŠđđĢđđđŦđ­ đđĸđ đĄ đđŽđđĨđĸđ­đ˛
đđ¨ đđđ  đđ đđŽđŦđĸđ đđĨđđ˛đđĢ đđ¨đ­.

âââââââââââââââââââ
âŖâ đđ°đ§đđĢ'đąđ : [đđĸđ¤đđŦđĄ đđđĨđđđĢ](https://t.me/BikashHalder)
âŖâ đđ°đ§đđĢ'đąđ : [đđđĸđ­đ˛đ đđđĨđđđĢ](https://t.me/AdityaHalder)
âŖâ đđŠđđđ­đđŦ Âģ : [đđ đ­ đđđđĸđđĸđđĨ](https://t.me/BikashGadgetsTech)
âŖâ đđŽđŠđŠđ¨đĢđ­ Âģ : [đđ đ­ đđĄđđ­](https://t.me/Bgt_Chat)
âŖâ đđĄđđ­đ¸ Âģ : [đđđĸđ­đ˛đ đđĸđŦđđŽđŦ](https://t.me/AdityaDiscus)
âââââââââââââââââââ

đ đđŽđŦđ­ đđđ đđ Âģ đđ¨ đđ¨đŽđĢ đđĢđ¨đŽđŠ đđ§đ
đđ§đŖđ¨đ˛ đđŽđŠđđĢ đđŽđđĨđĸđ­đ˛ âĨī¸đđŽđŦđĸđ.
ââââââââââââââââââââââââ**""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "â â° đđđ đđ đđ¨ đđ¨đŽđĢ đđĢđ¨đŽđŠ âą â", url=f"https://t.me/{app.username}?startgroup=true"),
                ],
                [
                    InlineKeyboardButton(
                        "đē â° đđĢđ¨đĻđ¨đ­đĸđ¨đ§ âą đē", url=f"https://youtube.com/channel/UCUkj6FFzdsOO5acUXVOEECg"),
                ],
                [
                    InlineKeyboardButton(
                        text="â â° đđŠđđ§ đđ¨đĻđĻđđ§đđŦ đđđ§đŽ âą â", callback_data="settings_back_helper")
                ]
           ]
        ),
           )
        if await is_on_off(config.LOG):
            sender_id = message.from_user.id
            sender_name = message.from_user.first_name
            return await app.send_message(
                config.LOG_GROUP_ID,
                f"{message.from_user.mention} đđđŦ đđŽđŦđ­ đđ­đđĢđ­đđ đđĸđ¤đđŦđĄ đđŽđŦđĸđ đđ¨đ­ đˇ.\n\n**đ đđŦđđĢ đđ:** {sender_id}\n**đ đđŦđđĢ đđđĻđ:** {sender_name}",
            )


@app.on_message(
    filters.command(get_command("START_COMMAND"))
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@LanguageStart
async def testbot(client, message: Message, _):
    out = start_pannel(_)
    return await message.reply_text(
        "**â đđĄđđ§đ¤ đđ¨đŽ đđ¨đĢ đđŦđĸđ§đ  đđ đđ§\nđđĄđđ­ Âģ  {0}\n\nđĨ đđ đđ¨đŽ đđđ¯đ đ đđ§đ˛ đđŽđđĢđĸđđŦ\nđđĄđđ§ đđąđŠđĨđđĸđ§ đŦ đđ¨ đđ˛ đđ°đ§đđĢ đ.\n\nđ đđ¨đĸđ§ đđŽđĢ đđŠđđđ­đđŦ â đđŽđŠđŠđ¨đĢđ­ đˇ\nđˇ đđ¨đĢ đđđ­đ­đĸđ§đ  đđđ° đđŠđđđ­đđŦ đ...**".format(
            message.chat.title, Bikash.config.MUSIC_BOT_NAME
        ),
        reply_markup=InlineKeyboardMarkup(out),
    )


welcome_group = 2


@app.on_message(filters.new_chat_members, group=welcome_group)
async def welcome(client, message: Message):
    chat_id = message.chat.id
    if config.PRIVATE_BOT_MODE == str(True):
        if not await is_served_private_chat(message.chat.id):
            await message.reply_text(
                "**đ đđĢđĸđ¯đđ­đ đđŽđŦđĸđ đđ¨đ­ đĩ**\n\nđ°đđ§đĨđ˛ đđ¨đĢ đđŽđ­đĄđ¨đĢđĸđŗđđ đđĄđđ­đŦ đđĢđ¨đĻ đđĄđ đđ°đ§đđĢ đ. đđŦđ¤ đđ˛ đđ°đ§đđĢ đ đđ¨ đđĨđĨđ¨đ° âđđ¨đŽđĢ đđĄđđ­ đđĸđĢđŦđ­ đˇ."
            )
            return await app.leave_chat(message.chat.id)
    else:
        await add_served_chat(chat_id)
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if member.id == app.id:
                chat_type = message.chat.type
                if chat_type != "supergroup":
                    await message.reply_text(_["start_6"])
                    return await app.leave_chat(message.chat.id)
                if chat_id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_7"].format(
                            f"https://t.me/{app.username}?start=sudolist"
                        )
                    )
                    return await app.leave_chat(chat_id)
                userbot = await get_assistant(message.chat.id)
                out = start_pannel(_)
                await message.reply_text(
                    _["start_3"].format(
                        config.MUSIC_BOT_NAME,
                        userbot.username,
                        userbot.id,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
            if member.id in Bikash.config.OWNER_ID:
                return await message.reply_text(
                    _["start_4"].format(
                        config.MUSIC_BOT_NAME, member.mention
                    )
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    _["start_5"].format(
                        config.MUSIC_BOT_NAME, member.mention
                    )
                )
            return
        except:
            return
