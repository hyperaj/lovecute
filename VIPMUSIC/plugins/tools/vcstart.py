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
    await app.send_message(f"🍷 𝑫𝒂𝒊 𝒂𝒅𝒎𝒊𝒏 𝒈𝒓𝒑 𝒍𝒂 𝒗𝒄 𝒌𝒂𝒏𝒏𝒐 𝒅𝒂 😻** {err_msg}")
    return False


@app.on_message(filters.command(["vcstart", "startvc"], ["/", "!"]))
async def start_group_call(c: Client, m: Message):
    chat_id = m.chat.id
    assistant = await get_assistant(chat_id)
    ass = await assistant.get_me()
    assid = ass.id
    if assistant is None:
        await app.send_message(chat_id, "🍷 𝑨𝒔𝒔𝒊𝒔𝒕𝒂𝒏𝒕 𝒌𝒐𝒍𝒂𝒓𝒖  𝑨𝒂𝒊𝒕𝒉𝒂𝒏 𝒅𝒂 𝒔𝒂𝒎𝒃𝒖 𝒎𝒂𝒗𝒂𝒏𝒆𝒂 😻")
        return
    msg = await app.send_message(chat_id, "🍷 𝑽𝒐𝒊𝒄𝒆 𝑪𝒉𝒂𝒕 𝑺𝒕𝒂𝒓𝒕 𝑷𝒂𝒏𝒏𝒊𝒕𝒉𝒂𝒏𝒈𝒂 𝑴𝒂𝒎𝒆𝒂𝒂 😻")
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
        await msg.edit_text("𝑽𝒐𝒊𝒄𝒆 𝑪𝒉𝒂𝒕 𝑺𝒖𝒄𝒄𝒆𝒔𝒔𝒇𝒖𝒍𝒍𝒚 𝑺𝒕𝒂𝒓𝒕 𝑩𝒂𝒃𝒚 💋🥹")
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
            await msg.edit_text("𝑽𝒐𝒊𝒄𝒆 𝑪𝒉𝒂𝒕 𝑺𝒖𝒄𝒄𝒆𝒔𝒔𝒇𝒖𝒍𝒍𝒚 𝑺𝒕𝒂𝒓𝒕 𝑩𝒂𝒃𝒚 💋🥹")
            await VIP.st_stream(chat_id)
            await set_loop(chat_id, 0)
        except:
            await msg.edit_text("🍷 𝐴𝑑𝑖𝑒 𝑎𝑑𝑚𝑖𝑛𝑠 𝑎𝑙𝑙 𝑝𝑒𝑟𝑚𝑖𝑠𝑠𝑖𝑜𝑛 𝑘𝑢𝑑𝑢𝑡ℎ𝑢 𝑡ℎ𝑜𝑙𝑎𝑖𝑔𝑎𝑑𝑎𝑎 😻")


@app.on_message(filters.command(["vcend", "endvc"], ["/", "!"]))
async def stop_group_call(c: Client, m: Message):
    chat_id = m.chat.id
    assistant = await get_assistant(chat_id)
    ass = await assistant.get_me()
    assid = ass.id
    if assistant is None:
        await app.send_message(chat_id, "🍷 𝑨𝒔𝒔𝒊𝒔𝒕𝒂𝒏𝒕 𝒌𝒐𝒍𝒂𝒓𝒖  𝑨𝒂𝒊𝒕𝒉𝒂𝒏 𝒅𝒂 𝒔𝒂𝒎𝒃𝒖 𝒎𝒂𝒗𝒂𝒏𝒆𝒂 😻")
        return
    msg = await app.send_message(chat_id, "𝑉𝑜𝑖𝑐𝑒 𝐶ℎ𝑎𝑡 𝐶𝑙𝑜𝑠𝑒 𝑃𝑎𝑛𝑛𝑖𝑡ℎ𝑎𝑛𝑔𝑎 𝐷𝑎 🥺😣")
    try:
        if not (
            group_call := (
                await get_group_call(
                    assistant, m, err_msg=", 𝐺𝑟𝑜𝑢𝑝 𝑙𝑎 𝑉𝑜𝑖𝑐𝑒 𝐶ℎ𝑎𝑡 𝐸𝑛𝑑 𝑃𝑎𝑛𝑛𝑖 𝑅𝑜𝑚𝑏𝑎 𝑁𝑒𝑎𝑟𝑎𝑚 𝐴𝑔𝑢𝑡ℎ𝑢 𝐷𝑎 𝑀𝑎𝑛𝑔𝑎 𝑀𝑎𝑛𝑑𝑎𝑖𝑦𝑎 🙄🙄😑"
                )
            )
        ):
            return
        await assistant.invoke(DiscardGroupCall(call=group_call))
        await msg.edit_text("𝑉𝑜𝑖𝑐𝑒 𝐶ℎ𝑎𝑡 𝐶𝑙𝑜𝑠𝑒 𝑃𝑎𝑛𝑛𝑖𝑡ℎ𝑎𝑛𝑔𝑎 𝐷𝑎 🥺😣")
    except Exception as e:
        if "GROUPCALL_FORBIDDEN" in str(e):
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
                            assistant, m, err_msg=", 𝐺𝑟𝑜𝑢𝑝 𝑙𝑎 𝑉𝑜𝑖𝑐𝑒 𝐶ℎ𝑎𝑡 𝐸𝑛𝑑 𝑃𝑎𝑛𝑛𝑖 𝑅𝑜𝑚𝑏𝑎 𝑁𝑒𝑎𝑟𝑎𝑚 𝐴𝑔𝑢𝑡ℎ𝑢 𝐷𝑎 𝑀𝑎𝑛𝑔𝑎 𝑀𝑎𝑛𝑑𝑎𝑖𝑦𝑎 🙄🙄😑"
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
                await msg.edit_text("𝑉𝑜𝑖𝑐𝑒 𝐶ℎ𝑎𝑡 𝐶𝑙𝑜𝑠𝑒 𝑃𝑎𝑛𝑛𝑖𝑡ℎ𝑎𝑛𝑔𝑎 𝐷𝑎 🥺😣")
                await VIP.st_stream(chat_id)
                await set_loop(chat_id, 0)
            except:
                await msg.edit_text("🍷 𝑫𝒂𝒊 𝒂𝒅𝒎𝒊𝒏 𝒗𝒄 𝒔𝒕𝒂𝒓𝒕 𝒑𝒂𝒏𝒏𝒊𝒕𝒉𝒂 𝒖𝒏𝒏𝒂 𝒎𝒂𝒂𝒓𝒊 𝒏𝒂𝒍𝒂 𝒗𝒂 𝒚𝒂𝒓𝒖 𝒊𝒍𝒍𝒂 𝒅𝒂 😻")
