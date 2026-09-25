# This code has been modified by @Looteredev
# Please do not remove this credit
from pyrogram import Client, filters, enums
from database.users_chats_db import db
from utils import temp
from info import ADMINS, GROUP_VERIFY_LOGS
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Script import get_random_message


@Client.on_callback_query(filters.regex(r"^verify_group_"))
async def verify_group_callback(client, query):
    data = query.data.split("_")
    chat_id = int(data[2])  
    group_info = await db.get_chat(chat_id)
    owner_id = group_info.get('owner_id', None)
    user = await client.get_users(owner_id)
    group_title = group_info.get('title', 'Unknown Group')
    total = await client.get_chat_members_count(chat_id)
    
    if not group_info:
        await query.answer(get_random_message("group_not_found"), show_alert=True)
        return
    if group_info.get('grp_link'):
        group_link = group_info['grp_link']
    else:
        chat = await client.get_chat(chat_id)
        if chat.username:
            group_link = f"https://t.me/{chat.username}"
        else:
            try:
                invite_link = await client.create_chat_invite_link(chat_id)
                group_link = invite_link.invite_link
            except Exception as e:
                group_link = "No link available"
    if await db.rejected_group(chat_id):
        await db.un_rejected(chat_id)
    await db.verify_group(chat_id) 
    await query.answer(get_random_message("group_verified"), show_alert=True)

    await query.message.edit_text(
        f"𝑩𝒐𝒕: {temp.U_NAME}\n𝑮𝒓𝒐𝒖𝒑: <a href='{group_link}'>{group_title}</a>\n𝑰𝑫: {chat_id}\n𝑴𝒆𝒎𝒃𝒆𝒓𝒔: {total}\n𝑼𝒔𝒆𝒓: {user.mention}\n\nGʀᴏᴜᴘ Is Vᴇʀɪғɪᴇᴅ. ✅",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Rᴇᴊᴇᴄᴛ ⛔", callback_data=f"rejected_group_{chat_id}")]]
        )
    )

    if owner_id:
        await client.send_message(chat_id=owner_id, text=f"#𝐕𝐞𝐫𝐢𝐟𝐲𝐞𝐝_𝐆𝐫𝐨𝐮𝐩\n\nGʀᴏᴜᴘ Nᴀᴍᴇ: {group_title}\nIᴅ: {chat_id}\n\nCᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs Gʀᴏᴜᴘ Is Vᴇʀɪғɪᴇᴅ. ✅.")

@Client.on_callback_query(filters.regex(r"^rejected_group_"))
async def rejected_group_callback(client, query):
    data = query.data.split("_")
    chat_id = int(data[2])
    group_info = await db.get_chat(chat_id)
    owner_id = group_info.get('owner_id', None)
    user = await client.get_users(owner_id)
    group_title = group_info.get('title', 'Unknown Group')
    total = await client.get_chat_members_count(chat_id)
    if not group_info:
        await query.answer(get_random_message("group_not_found"), show_alert=True)
        return
    if group_info.get('grp_link'):
        group_link = group_info['grp_link']
    else:
        chat = await client.get_chat(chat_id)
        if chat.username:
            group_link = f"https://t.me/{chat.username}"
        else:
            try:
                invite_link = await client.create_chat_invite_link(chat_id)
                group_link = invite_link.invite_link
            except Exception as e:
                group_link = "No link available"
    await db.reject_group(chat_id)
    await query.answer(get_random_message("group_rejected"), show_alert=True)

    await query.message.edit_text(f"𝑩𝒐𝒕: {temp.U_NAME}\n𝑮𝒓𝒐𝒖𝒑: <a href={group_link}>{group_title}</a>\n𝑰𝑫: {chat_id}\n𝑴𝒆𝒎𝒃𝒆𝒓𝒔: {total}\n𝑼𝒔𝒆𝒓: {user.mention}</b>\n\nRᴇᴊᴇᴄᴛᴇᴅ Gʀᴏᴜᴘ ❌", reply_markup=InlineKeyboardMarkup(
        [[InlineKeyboardButton("Tᴀᴘ Tᴏ Vᴇʀɪғʏ ✅", callback_data=f"verify_group_{chat_id}")]]
    ))
    if owner_id:
        await client.send_message(chat_id=owner_id, text=f"#𝐑𝐞𝐣𝐞𝐜𝐭_𝐆𝐫𝐨𝐮𝐩❌\n\nGʀᴏᴜᴘ Nᴀᴍᴇ: {group_title}\nIᴅ: {chat_id}\n\nʏᴏᴜʀ ɢʀᴏᴜᴘ ʜᴀs ʙᴇᴇɴ ʀᴇᴊᴇᴄᴛᴇᴅ\n\n ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴀᴅᴍɪɴ: @Looteredev.")


# Verify command to initiate the group verification
@Client.on_message(filters.group & filters.command("verify"))
async def grpp_verify(bot, message):
    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
    total=await bot.get_chat_members_count(message.chat.id)
    owner_id = message.from_user.id
    group_link = message.chat.invite_link
    is_verified = await db.check_group_verification(message.chat.id)
    is_rejected = await db.rejected_group(message.chat.id)
    owner=user.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] or str(message.from_user.id) in ADMINS
    if message.chat.username:
        group_link = f"https://t.me/{message.chat.username}"
    else:
        try:
            invite_link = await bot.create_chat_invite_link(message.chat.id)
            group_link = invite_link.invite_link
        except Exception as e:
            group_link = "No link available"
    if not is_rejected:
        if owner:
            if not is_verified:
                if not await db.get_chat(message.chat.id):
                    await db.add_chat(message.chat.id, message.chat.title, owner_id)
                await bot.send_message(
                    chat_id=GROUP_VERIFY_LOGS,
                    text=f"<b>#𝐕𝐞𝐫𝐢𝐟𝐲_𝐆𝐫𝐨𝐮𝐩\n\n𝑩𝒐𝒕: {temp.U_NAME}\n𝑮𝒓𝒐𝒖𝒑:- <a href={group_link}>{message.chat.title}</a>\n𝑰𝑫: {message.chat.id}\n𝑴𝒆𝒎𝒃𝒆𝒓𝒔:- {total}\n𝑼𝒔𝒆𝒓: {message.from_user.mention}</b>",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Tᴀᴘ Tᴏ Vᴇʀɪғʏ ✅", callback_data=f"verify_group_{message.chat.id}")],
                        [InlineKeyboardButton("Rᴇᴊᴇᴄᴛ ⭕", callback_data=f"rejected_group_{message.chat.id}")]]
                    )
                )
                await message.reply("ᴠᴇʀɪғʏ ʀᴇǫᴜᴇsᴛ sᴇɴᴛ ᴛᴏ ᴍʏ ᴀᴅᴍɪɴ, ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ғᴏʀ ᴛʜᴇ ᴄᴏɴғɪʀᴍᴀᴛɪᴏɴ.")
            else:
                await message.reply("Gʀᴏᴜᴘ Aʟʀᴇᴀᴅʏ Vᴇʀɪғɪᴇᴅ ✅")
        else:
            await message.reply_text(
                text=f"<b>ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs</b>",
            )
    else:
        if owner:
            await message.reply_text(text=f" ʏᴏᴜʀ ɢʀᴏᴜᴘ ʜᴀs ʙᴇᴇɴ ʀᴇᴊᴇᴄᴛᴇᴅ ʙʏ ᴍʏ ᴀᴅᴍɪɴ.\n\nɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ɢᴇᴛ ᴛʜᴇ ɢʀᴏᴜᴘ ᴠᴇʀɪғɪᴇᴅ ᴛʜᴇɴ contact ᴛʜᴇ ᴀᴅᴍɪɴ. @Looteredev.")
        else:
            await message.reply("ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs")


# Command to delete all saved groups and leave them
@Client.on_message(filters.command("grp_delete") & filters.user(ADMINS))
async def delete_all_groups_command(bot, message):
    all_groups = await db.get_all_groups()
    for group in all_groups:
        try:
            await bot.send_message(group['id'], "The bot is now leaving this group as per the admin's command.")
            await bot.leave_chat(group['id'])
        except Exception as e:
            print(f"Failed to leave chat {group['id']}: {e}")
    await db.delete_all_groups()
    await message.reply_text("All saved groups have been deleted and bot has left all groups.") 
