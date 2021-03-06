

from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot

from ...libs.redis import MessageInfo
from ...utils import send_github_message
from . import config, is_github_reply, KEY_GITHUB_REPLY

link = on_command("link",
                  is_github_reply,
                  priority=config.github_command_priority)
link.__doc__ = """
/link
回复机器人一条github信息，给出对应链接
"""


@link.handle()
async def handle_link(bot: Bot, state: T_State):
    message_info: MessageInfo = state[KEY_GITHUB_REPLY]
    url = f"https://github.com/{message_info.owner}/{message_info.repo}/issues/{message_info.number}"
    await send_github_message(link, message_info.owner, message_info.repo,
                              message_info.number, url)
