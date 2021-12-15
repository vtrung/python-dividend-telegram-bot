#!/usr/bin/env python3

import logging
import telegram
import re
import configparser

from telegram.error import NetworkError, Unauthorized
from cachetools import cached, TTLCache

from time import sleep
from pardiv import stock

update_id = None

def main():
    #read config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    token_id = config['ID']['telegram']

    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot(token_id)

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        sleep(5)
        try:
            request(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def request(bot):
    """ read user request """
    global update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        print(update)
        if update.message:
          words = update.message.text.split()
          for word in words:
            word = re.sub(r'\W+', '', word)
            newstock = getstock(word.upper())
            info = newstock.getinfo()
            update.message.reply_text(info)

# cache stock data for no longer than a day
@cached(cache=TTLCache(maxsize=1024, ttl=86400))       
def getstock(sym):
    newstock = stock(sym)
    newstock.get()
    return newstock

if __name__ == '__main__':
    main()
