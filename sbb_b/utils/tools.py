from telethon.tl.functions.channels import (
    CreateChannelRequest,
    EditPhotoRequest,
    InviteToChannelRequest,
)
from telethon.tl.functions.messages import ExportChatInviteRequest


async def create_supergroup(group_name, client, botusername, descript, photo):
    try:
        result = await client(
            CreateChannelRequest(
                title=group_name,
                about=descript,
                megagroup=True,
            )
        )
        created_chat_id = result.chats[0].id
        result = await client(
            ExportChatInviteRequest(
                peer=created_chat_id,
            )
        )
        await client(
            InviteToChannelRequest(
                channel=created_chat_id,
                users=[botusername],
            )
        )
        if photo:
            await client(
                EditPhotoRequest(
                    channel=created_chat_id,
                    photo=photo,
                )
            )
    except Exception as e:
        return "error", str(e)
    if not str(created_chat_id).startswith("-100"):
        created_chat_id = int("-100" + str(created_chat_id))
    return result, created_chat_id
