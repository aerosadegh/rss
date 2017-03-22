import sys
import time
import telepot
from emoji import emojize
import telepot.helper
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import (
    per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)
from tele import RSSFLink
"""
$ python3.5 lover.py <token>

1. Send him a message
2. He will ask you to marry him
3. He will keep asking until you say "Yes"

If you are silent for 10 seconds, he will go away a little bit, but is still
there waiting for you. What a sweet bot!

It statically captures callback query according to the originating chat id.
This is the chat-centric approach.

Proposing is a private matter. This bot only works in a private chat.
"""

propose_records = telepot.helper.SafeDict()  # thread-safe dict
em = lambda x: bytes(emojize(x, use_aliases=True),'utf8').decode('utf8')

ke = [InlineKeyboardButton(text='{:}'.format(c[0][6:].replace('گروه','')), callback_data='{:}'.format(i)) for i,c in enumerate(RSSFLink)]
kE = [[ke[i],ke[i+1]] for i in range(0,len(ke)-1,2)]

class Lover(telepot.helper.ChatHandler):
    keyboard = InlineKeyboardMarkup(inline_keyboard=kE)

    def __init__(self, *args, **kwargs):
        super(Lover, self).__init__(*args, **kwargs)

        # Retrieve from database
        global propose_records
        if self.id in propose_records:
            self._count, self._edit_msg_ident = propose_records[self.id]
            self._editor = telepot.helper.Editor(self.bot, self._edit_msg_ident) if self._edit_msg_ident else None
        else:
            self._count = 0
            self._edit_msg_ident = None
            self._editor = None

    def _propose(self):
        self._count += 1
        sent = self.sender.sendMessage('%d. یک موضوع انتخاب کنید' % self._count, reply_markup=self.keyboard)
        self._editor = telepot.helper.Editor(self.bot, sent)
        self._edit_msg_ident = telepot.message_identifier(sent)

    def _cancel_last(self):
        if self._editor:
            self._editor.editMessageReplyMarkup(reply_markup=None)
            self._editor = None
            self._edit_msg_ident = None

    def on_chat_message(self, msg):
        self._propose()

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        from tele import Feeds
        if query_data is not '/more':
            self._cancel_last()
            self.sender.sendMessage(RSSFLink[int(query_data)][0]+em(Feeds[int(query_data)][0]))
            ff = Feeds[int(query_data)][1:6]
            for c in ff:
                self.sender.sendMessage(em(c), 
                                        disable_web_page_preview=True,
                                        parse_mode='Markdown')
            self.close()
            del ff, Feeds
        else:
            self.bot.answerCallbackQuery(query_id, text='Ok. But I am going to keep asking.')
            self._cancel_last()
            self._propose()

    def on__idle(self, event):
        self.sender.sendMessage('I know you may need a little time. I will always be here for you.')
        self.close()

    def on_close(self, ex):
        # Save to database
        global propose_records
        propose_records[self.id] = (self._count, self._edit_msg_ident)

try:
    TOKEN = sys.argv[1]
except:
    TOKEN = '351549984:AAH4rllQBQyeRKZyxxCtQkapria6y2L5R-w'


bot = telepot.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(
            per_chat_id(types=['private']), create_open, Lover, timeout=10),
])
bot.message_loop(run_forever='Listening ...')
