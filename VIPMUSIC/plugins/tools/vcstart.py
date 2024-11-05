from typing import List, Optional, Union

from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import ChatPrivileges, Message

from VIPMUSIC import app
from VIPMUSIC.core.call import VIP
from VIPMUSIC.utils.database import *
from VIPMUSIC.utils.database import set_loop

other_filters = filters.group & ~filters.via_bot & ~filters.forwarded
other_filters2 = filters.private & ~filters.via_bot & ~filters.forwarded


def command(commands: Union[str, List[str]]):
    return filters.command(commands, "")


@app.on_message(filters.video_chat_started & filters.group)
async def brah(_, msg):
    chat_id = msg.chat.id
    try:
        await msg.reply("**🍷 𝑽𝒄 𝒔𝒕𝒂𝒓𝒕 𝒑𝒂𝒏𝒏𝒊𝒕𝒉𝒂𝒏𝒈𝒂 𝒅𝒂 𝒑𝒂𝒏𝒈𝒖 😻**")
        await VIP.st_stream(chat_id)
        await set_loop(chat_id, 0)
    except Exception as e:
        return await msg.reply(f"**Error {e}**")


################################################
async def get_group_call(
    client: Client, message: Message, err_msg: str = ""
) -> Optional[InputGroupCall]:
    assistant = await get_assistant(message.chat.id)
    chat_peer = await assistant.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (
                await assistant.invoke(GetFullChannel(channel=chat_peer))
            ).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await assistant.invoke(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await app.send_message(f"**🍷 𝑫𝒂𝒊 𝒂𝒅𝒎𝒊𝒏 𝒈𝒓𝒑 𝒍𝒂 𝒗𝒄 𝒌𝒂𝒏𝒏𝒐 𝒅𝒂 😻** {err_msg}")
    return False


@app.on_message(filters.command(["vcstart", "startvc"], ["/", "!"]))
async def start_group_call(c: Client, m: Message):
    chat_id = m.chat.id
    assistant = await get_assistant(chat_id)
    ass = await assistant.get_me()
    assid = ass.id
    if assistant is None:
        await app.send_message(chat_id, "🍷 𝑨𝒔𝒔𝒊𝒔𝒕𝒂𝒏𝒕 𝒌𝒐𝒍𝒂𝒓𝒖  𝑨𝒂𝒊𝒕𝒉𝒂𝒏 𝒅𝒂 𝒔𝒂𝒎𝒃𝒖 𝒎𝒂𝒗𝒂𝒏𝒆𝒂 😻")
        return
    msg = await app.send_message(chat_id, "ꜱᴛᴀʀᴛɪɴɢ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ..")
    try:
        peer = await assistant.resolve_peer(chat_id)
        await assistant.invoke(
            CreateGroupCall(
                peer=InputPeerChannel(
                    channel_id=peer.channel_id,
                    access_hash=peer.access_hash,
                ),
                random_id=assistant.rnd_id() // 9000000000,
            )
        )
        await msg.edit_text("𝑉𝑎𝑛𝑡ℎ𝑢 𝐾𝑎𝑑ℎ𝑎𝑙 𝑃𝑎𝑛𝑛𝑢𝑛𝑔𝑎 𝑉𝑐 𝐿𝑎 𝐷𝑜𝑙𝑖 & 𝐷𝑜𝑙𝑎𝑛𝑠 🫶🏻🫴🏻🤍")
    except ChatAdminRequired:
        try:
            await app.promote_chat_member(
                chat_id,
                assid,
                privileges=ChatPrivileges(
                    can_manage_chat=False,
                    can_delete_messages=False,
                    can_manage_video_chats=True,
                    can_restrict_members=False,
                    can_change_info=False,
                    can_invite_users=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                ),
            )
            peer = await assistant.resolve_peer(chat_id)
            await assistant.invoke(
                CreateGroupCall(
                    peer=InputPeerChannel(
                        channel_id=peer.channel_id,
                        access_hash=peer.access_hash,
                    ),
                    random_id=assistant.rnd_id() // 9000000000,
                )
            )
            await app.promote_chat_member(
                chat_id,
                assid,
                privileges=ChatPrivileges(
                    can_manage_chat=False,
                    can_delete_messages=False,
                    can_manage_video_chats=False,
                    can_restrict_members=False,
                    can_change_info=False,
                    can_invite_users=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                ),
            )
            await msg.edit_text("🍷 𝑫𝒂𝒊 𝒂𝒅𝒎𝒊𝒏 𝒗𝒄 𝒔𝒕𝒂𝒓𝒕 𝒑𝒂𝒏𝒏𝒊𝒕𝒉𝒂 𝒖𝒏𝒏𝒂 𝒎𝒂𝒂𝒓𝒊 𝒏𝒂𝒍𝒂 𝒗𝒂 𝒚𝒂𝒓𝒖 𝒊𝒍𝒍𝒂 𝒅𝒂 😻")
            await VIP.st_stream(chat_id)
            await set_loop(chat_id, 0)
        except:
            await msg.edit_text("𝑘𝑢𝑑𝑢𝑡𝑎")


@app.on_message(filters.command(["vcend", "endvc"], ["/", "!"]))
async def stop_group_call(c: Client, m: Message):
    chat_id = m.chat.id
    assistant = await get_assistant(chat_id)
    ass = await assistant.get_me()
    assid = ass.id
    if assistant is None:
        await app.send_message(chat_id, "🍷 𝑨𝒔𝒔𝒊𝒔𝒕𝒂𝒏𝒕 𝒌𝒐𝒍𝒂𝒓𝒖  𝑨𝒂𝒊𝒕𝒉𝒂𝒏 𝒅𝒂 𝒔𝒂𝒎𝒃𝒖 𝒎𝒂𝒗𝒂𝒏𝒆𝒂 😻")
        return
    msg = await app.send_message(chat_id, "🤧💫 𝑉𝑐 𝐸𝑣𝑎𝑛𝑑𝑎 𝐸𝑛𝑑 𝑃𝑎𝑛𝑛𝑢𝑛𝑎𝑡ℎ𝑢 🥹🤌🏻")
    try:
        if not (
            group_call := (
                await get_group_call(
                    assistant, m, err_msg=", 🍷 𝑉𝑐 𝑒𝑛𝑑 𝑝𝑎𝑛𝑛𝑎 𝑟𝑜𝑚𝑏𝑎 𝑛𝑒𝑟𝑎𝑚 𝑎𝑐ℎ𝑢 😻"
                )
            )
        ):
          
            try:
                await app.promote_chat_member(
                    chat_id,
                    assid,
                    privileges=ChatPrivileges(
                        can_manage_chat=False,
                        can_delete_messages=False,
                        can_manage_video_chats=True,
                        can_restrict_members=False,
                        can_change_info=False,
                        can_invite_users=False,
                        can_pin_messages=False,
                        can_promote_members=False,
                    ),
                )
                if not (
                    group_call := (
                        await get_group_call(
                            assistant, m, err_msg=", 🍷 𝑉𝑐 𝑒𝑛𝑑 𝑝𝑎𝑛𝑛𝑎 𝑟𝑜𝑚𝑏𝑎 𝑛𝑒𝑟𝑎𝑚 𝑎𝑐ℎ𝑢 😻"
                        )
                    )
                ):
                    return
                await assistant.invoke(DiscardGroupCall(call=group_call))
                await app.promote_chat_member(
                    chat_id,
                    assid,
                    privileges=ChatPrivileges(
                        can_manage_chat=False,
                        can_delete_messages=False,
                        can_manage_video_chats=False,
                        can_restrict_members=False,
                        can_change_info=False,
                        can_invite_users=False,
                        can_pin_messages=False,
                        can_promote_members=False,
                    ),
                )
                await VIP.st_stream(chat_id)
                await set_loop(chat_id, 0)  
            except:
                await msg.edit_text("🍷 𝑫𝒂𝒊 𝒂𝒅𝒎𝒊𝒏 𝒗𝒄 𝒔𝒕𝒂𝒓𝒕 𝒑𝒂𝒏𝒏𝒊𝒕𝒉𝒂 𝒖𝒏𝒏𝒂 𝒎𝒂𝒂𝒓𝒊 𝒏𝒂𝒍𝒂 𝒗𝒂 𝒚𝒂𝒓𝒖 𝒊𝒍𝒍𝒂 𝒅𝒂 😻")
