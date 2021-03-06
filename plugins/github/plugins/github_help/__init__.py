

import inspect
from functools import reduce

from nonebot import on_command
from nonebot.adapters.cqhttp import Bot

from ... import _sub_plugins, github_config as config

help = on_command("git_help", priority=config.github_command_priority)
help.__doc__ = """
/git_help
获取帮助
"""


@help.handle()
async def handle(bot: Bot):
    matchers = reduce(lambda x, y: x.union(y.matcher), _sub_plugins, set())
    docs = "命令列表：\n\n"
    docs += "\n\n".join(
        map(lambda x: inspect.cleandoc(x.__doc__),
            filter(lambda x: x.__doc__, matchers)))
    await help.finish(docs)
