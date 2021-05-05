# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# You can find misc modules, which dont fit in anything xD
""" Userbot module for other small commands. """

from random import randint
from time import sleep
from os import execl
import sys
import io
import sys
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot, GIT_REPO_NAME, ALIVE_NAME
from userbot.events import register
from userbot.utils import time_formatter


# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


@register(outgoing=True, pattern="^.random")
async def randomise(items):
    """ For .random command, get a random item from the list of items. """
    itemo = (items.text[8:]).split()
    if len(itemo) < 2:
        await items.edit(
            "`2 or more items are required! Check .help random for more info.`"
        )
        return
    index = randint(1, len(itemo) - 1)
    await items.edit(
        "**Query: **\n`" + items.text[8:] + "`\n**Output: **\n`" + itemo[index] + "`"
    )


@register(outgoing=True, pattern="^.sleep ([0-9]+)$")
async def sleepybot(time):
    """ For .sleep command, let the userbot snooze for a few second. """
    counter = int(time.pattern_match.group(1))
    await time.edit("`I am sulking and snoozing...`")
    if BOTLOG:
        str_counter = time_formatter(counter)
        await time.client.send_message(
            BOTLOG_CHATID, f"You put the bot to sleep for {str_counter}.",
        )
    sleep(counter)
    await time.edit("`OK, I'm awake now.`")


@register(outgoing=True, pattern="^.shutdown$")
async def killdabot(event):
    """ For .shutdown command, shut the bot down."""
    await event.edit("`Shutting down..`")
    if event.is_channel and not event.is_group:
        await event.edit("`shutdown commad isn't permitted on channels`")
        return

    await event.edit("`Goodbye *Windows XP shutdown sound*....`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n" "Bot shut down")
    await bot.disconnect()


@register(outgoing=True, pattern="^.restart$")
async def killdabot(event):
    await event.edit(f"`Restarting` **⬢ {DEFAULTUSER}**..")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART \n" "Bot Restarted")
    await bot.disconnect()
    # Spin a new instance of bot
    execl(sys.executable, sys.executable, *sys.argv)
    # Shut the existing one down
    exit()


# Copyright (c) Gegham Zakaryan | 2019
@register(outgoing=True, pattern="^.repeat (.*)")
async def repeat(rep):
    cnt, txt = rep.pattern_match.group(1).split(" ", 1)
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + "\n"

    for _ in range(replyCount - 1):
        replyText += toBeRepeated + "\n"

    await rep.edit(replyText)


@register(outgoing=True, pattern="^.raw$")
async def raw(event):
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = event.reply_to_msg_id
    else:
        the_real_message = event.stringify()
        reply_to_id = event.message.id
    with io.BytesIO(str.encode(the_real_message)) as out_file:
        out_file.name = "raw_message_data.txt"
        await event.edit("`Check the userbot log for the decoded message data !!`")
        await event.client.send_file(
            BOTLOG_CHATID,
            out_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            caption="`Here's the decoded message data !!`",
        )


CMD_HELP.update(
    {
        "random": ".random <item1> <item2> ... <itemN>\
\nUsage: Get a random item from the list of items."
    }
)

CMD_HELP.update(
    {
        "sleep": ".sleep <seconds>\
\nUsage: Userbots get tired too. Let yours snooze for a few seconds."
    }
)

CMD_HELP.update(
    {
        "shutdown": ".shutdown\
\nUsage: Sometimes you need to shut down your bot. Sometimes you just hope to\
hear Windows XP shutdown sound... but you don't."
    }
)

CMD_HELP.update(
    {
        "support": ".support\
\nUsage: If you need help, use this command."
    }
)
CMD_HELP.update(
    {
        "creator": ".contributor\
\nUsage: See who contribute to this program"
    }
)

CMD_HELP.update(
    {
        "creator": ".maintain\
\nUsage: Know who maintain this awesome userbot !!"
    }
)

CMD_HELP.update(
    {
        "repeat": ".repeat <no.> <text>\
\nUsage: Repeats the text for a number of times. Don't confuse this with spam tho."
    }
)

CMD_HELP.update(
    {
        "restart": ".restart\
\nUsage: Restarts the bot !!"
    }
)

CMD_HELP.update(
    {
        "raw": ".raw\
\nUsage: Get detailed JSON-like formatted data about replied message."
    }
)
