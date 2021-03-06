import logging
from os.path import exists
from configparser import ConfigParser
from telegram import Update, InlineQueryResultCachedSticker
from telegram.error import InvalidToken
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, InlineQueryHandler
import mixer
import storage

def generate_config(config):
    config['section_a'] = {'private_token': '', 'owner_id': 'yes', 'cache_id': ''}
    while True:
        try:
            config['section_a']['private_token'] = str(input('Enter Bot API Token: '))
            validator = Updater(token=config.get('section_a','private_token'))
            validator.stop()
        except InvalidToken:
            print('Invalid token provided. Please, try again')
            continue
        break
    config['section_a']['owner_id'] = str(input('Enter your user ID: '))
    config['section_a']['cache_id'] = str(input('Enter ID of the channel that will be used as a cache: '))
    with open('settings.ini', 'w', encoding='UTF-8') as configfile: 
        config.write(configfile)
    return config

s = storage.Storage('file.pcl')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id,
    text="Hi!š I'm Emoji Mixer. To use me, type @emomixbot followed by any two emoji in the input field, like this: š¤š¢. You can also just send two emoji here. To see the list of available emoji, type /about.")

def about(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id,
    text="š¤ *What is this bot for?*\nThis bot mixes a pair of emoji into a new, combined one\n\nšŖ *How does it work?*\nIt uses Google's images from the Emoji Kitchen feature of their keyboard\n\nšØš»āš» *Who created it?*\nThis bot was created by @gershik\. Its source code will soon be available on GitHub\n\nšÆ *Which emoji are supported?*\nAccording to [Emojipedia](https://emojipedia.org/emoji-kitchen/), the following ones are supported:\nšššššššš¤£š­ššššš„°šš„³š¤ššš„²š„¹āŗļøššššš«¢š¤­š¶šššššššš¤Ŗš«”š¤š¤Øš§ššš¤š š”š¤¬ā¹ļøšš«¤ššš„ŗš³š¬š¤š¤«š°šØš§š¦š®šÆš²š«£š±š¤Æš¢š„ššš®āšØšš£š©š«š¤¤š„±š“šŖšššš¤¢š¤®š¤§š¤š¤š„“š« š¶āš«ļøšµāš«š«„šµš„µš„¶š·šš¤ š¤šš¤š„øš¤„š¤”š»š©š½š¤šššæā ļøš„š«ā­šāØšÆšØš¦š¤š³ļøšššŗšøš¹š»š¼š½ššæš¾ā¤ļøš§”ššššš¤š¤š¤ā„ļøšššššššššā£ļøā¤ļøāš©¹šā¤ļøāš„šš¦ ššļøšš¹š·šøš¼šµš²šŖµš«ļøšŖļøāļøāāļøš„āļøāļøšš šššššššµš¦š±š¶š»šØš¼š­š°š¦š·š½š¦š¢šššš©šš¦®šāš¦ŗššš¦š¦š¦„šš¦š¦šŖ¶š¦š¦š§ššš¦š·ļøšššššššš¶ļøš„šš„š§š­šš§ā š“š½ļøš ššļøšššššššļøš„š„š„ššļøšš£šŖš¼šµš¶š§š§øššš¶ļøšŖš©¹š°š®\nUnfortunately, some of these don't work in the bot yet\.", parse_mode='MarkdownV2')


def mix(update: Update, context: CallbackContext) -> None:
    pair = update.message.text
    if pair[::-1] in s.dict:
        pair = pair[::-1]
    if pair in s.dict:
        file_id=s.dict[pair]
        context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=file_id)
    else:
        mixed = []
        try: 
            mixed += mixer.make_mix(list(pair))
            #print(mixed)
        except IndexError: 
            context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter exactly 2 emoji")
        if mixed[0] == 200 or mixed[0] == 'bruted': 
            file_id = (context.bot.send_sticker(chat_id=config.get('section_a', 'cache_id'), sticker=mixed[1]))['sticker']['file_id']
            context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=file_id)
            s.dict[pair] = file_id
            s.sync()
            if mixed[0] == 'bruted': 
                context.bot.send_message(
                    chat_id=config.get('section_a','owner_id'), 
                    text=pair + pair.encode('unicode-escape').decode('ASCII'))
        elif  mixed[0] == 404:
            context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text="Unfortunately, these emoji don't mix.")
        else: context.bot.send_message(chat_id=update.effective_chat.id, text=f"Weird error. Please report it to @gershik with the emoji that you tried. Code: {mixed[0]}_{pair}")

def inline_mix(update: Update, context: CallbackContext):
    pair = update.inline_query.query
    if not pair:
        return
    results = []
    if pair[::-1] in s.dict:
        pair = pair[::-1]
    if pair in s.dict:
        file_id=s.dict[pair]
        results.append(InlineQueryResultCachedSticker(id=pair, sticker_file_id=file_id,))
    else:
        mixed = []
        try: 
            mixed += mixer.make_mix(list(pair))
        except IndexError: 
            context.bot.answer_inline_query(
            update.inline_query.id, results='',
            switch_pm_text = "Please enter exactly 2 emoji", switch_pm_parameter = '0')
            return
        if mixed[0] == 200 or mixed[0] == 'bruted':
            file_id = (context.bot.send_sticker(
                chat_id=config.get('section_a','cache_id'), sticker=mixed[1]))['sticker']['file_id']
            results.append(InlineQueryResultCachedSticker(id=pair, sticker_file_id=file_id,))
            s.dict[pair] = file_id
            s.sync()
            if mixed == 'bruted':
                context.bot.send_message(
                    chat_id=config.get('section_a','owner_id'),
                    text=pair + pair.encode('unicode-escape').decode('ASCII'))
        elif mixed[0] == 404:
            context.bot.answer_inline_query(
                update.inline_query.id, results,
                switch_pm_text = "Unfortunately, these emoji don't mix.",
                switch_pm_parameter = '0')
        else:
            context.bot.answer_inline_query(
            update.inline_query.id, results,
            switch_pm_text = f"Weird error. Please report it to @gershik with the emoji that you tried. Code: {mixed[0]}_{pair}",
            switch_pm_parameter = '0')
    context.bot.answer_inline_query(update.inline_query.id, results)


config = ConfigParser()
if not exists('settings.ini'):
    generate_config(config)
config.read('settings.ini')


def main() -> None:
    updater = Updater(token=config.get('section_a','private_token'))

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("about", about))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, mix))
    dispatcher.add_handler(InlineQueryHandler(inline_mix))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
