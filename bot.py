import logging
from os.path import exists
from configparser import ConfigParser
from telegram import Update, InlineQueryResultCachedSticker
from telegram.error import InvalidToken
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, InlineQueryHandler
import mixer
import storage

def generate_config(config):
#   # I made a config generator to facilitate starting the bot up
    config['section_a'] = {'private_token': '', 'owner_id': 'yes', 'cache_id': ''}
#   # here we generate the required keys inside the config file
    while True:
        try:
            config['section_a']['private_token'] = str(input('Enter Bot API Token: '))
            validator = Updater(token=config.get('section_a','private_token'))
#           # Updater is called to verify the token
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
    text="Hi!👋 I'm Emoji Mixer. To use me, type @emomixbot followed by any two emoji in the input field, like this: 🤔🐢. You can also just send two emoji here. To see the list of available emoji, type /about.")

def about(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id,
    text="🤔 *What is this bot for?*\nThis bot mixes a pair of emoji into a new, combined one\.\n\n🪄 *How does it work?*\nIt uses Google's images from the Emoji Kitchen feature of their keyboard\.\n\n👨🏻‍💻 *Who created it?*\nThis bot was created by @gershik\. Its source code is available on [GitHub](https://github.com/gershik/emojimixer)\.\n\n🎯 *Which emoji are supported?*\nAccording to [Emojipedia](https://emojipedia.org/emoji-kitchen/), the following ones are supported:\n😀😃😄😁😆😅🤣😂🙃🫠😉😊😇🥰😍🤩😘😗☺️😚😙🥲😋😛😜🤪😝🤑🤗🤭🫢🫣🤫🤔🫡🤐🤨😐😑😶🫥😶‍🌫️😏😒🙄😬😮‍💨🤥😌😔😪🤤😴😷🤒🤕🤢🤮🤧🥵🥶🥴😵😵‍💫🤯🤠🥳🥸😎🤓🧐😕🫤😟🙁☹️😮😯😲😳🥺🥹😦😧😨😰😥😢😭😱😖😣😞😓😩😫🥱😤😡😠🤬😈👿💀☠️💩🤡👻👽🤖😺😸😹😻😼😽🙀😿😾🙈🙉🙊💋💌💘💝💖💗💞💕💟❣️💔❤️‍🔥❤️‍🩹❤️🧡💛💚💙💜🤎🖤🤍💯💫💦💨🕳️💣💬👁️‍🗨️🗯️💭💤👍🧠🫀🫁🦷🦴👀👁️👅🫦🤷🐵🐒🐶🐕🦮🐕‍🦺🐩🦝🐱🐈🦁🐯🐅🦄🦌🐷🐖🐽🐐🦙🐭🐁🐰🐇🦔🦇🐻🐨🐼🦥🐾🐦🐧🦉🪶🦩🐢🐟🐙🐚🪸🐌🦋🐝🪲🐞🦗🪳🕷️🦂🦠💐🌸💮🪷🏵️🌹🌺🌻🌼🌷🌱🪴🌲🌳🌴🌵🌿☘️🍀🍃🪹🍇🍈🍉🍊🍋🍌🍍🥭🍐🍒🍓🫐🥝🍅🫒🥥🥑🥔🥕🌽🌶️🫑🥒🥦🧄🧅🍄🥜🫘🌰🍞🥐🥖🫓🥨🥯🥞🧀🍖🥩🍔🍟🌭🥪🌮🌯🫔🥙🧆🍳🥘🍲🫕🥣🥗🍿🧂🥫🍘🍙🍚🍛🍜🍝🍠🍣🍤🍥🥠🦀🦞🍦🍧🍨🍩🍪🎂🍰🧁🍫🍬🍼☕🍵🍹🧋🧉🍽️🍴🥄🔪🌍🌎🌏🌐🗺️🌋🏕️🏖️🏜️🏝️🏟️🏛️🪨🪵🏘️🏠🏡🌃🏙️🌄🌅🌆🌇🎡🎢🎪🚂🚌🚍🚎🚒🚓🚔🚕🚖🚗🚘🏎️🛹🛼🚨🛑⚓🛟⛵🚤🛳️⛴️🛥️🚢✈️🛩️🛫🛬💺🚀🛸🌑🌒🌓🌔🌕🌖🌗🌘🌙🌚🌛🌜☀️🌝🌞🪐⭐🌟🌠☁️⛅🌧️🌨️🌩️🌪️🌫️🌬️🌀🌈🌂☂️☔⚡❄️☃️⛄☄️🔥💧🌊🎃🎄🧨✨🎈🎉🎊🎀🎁🎗️🎟️🎫🎖️🏆🏅🥇🥈🥉⚽⚾🥎🏀🏐🏈🏉🎾🎳🏏🏑🏒🥍🏓🏸🥊🥋🥅⛳⛸️🎣🤿🎽🎿🛷🥌🎯🪀🪁🎱🔮🪄🧿🎮🎰🎲🧩🧸🪩♠️♥️♟️🃏🀄🎴🎭🎨🧵🪡🧶👓🕶️🧦🩰👑🎩🪖💄💍💎🔈🔉🔊📣🎼🎵🎶🎙️🎤🎧🎷🪗🎸🎹🎺🎻🪕🥁🪘📱📲☎️📞🔋🪫💽💾💿📀🎥🎞️📽️🎬📺📷📸📹🔎💡📔📕📖📗📘📙📚📓📒📰💰🪙💴💵💶💷💸💳✉️📧📨📩📤📥📮✏️✒️🖋️🖊️🖌️🖍️📝📁📂🗂️🗃️🗄️🗑️🔒🔓🔏🔐🔑🗝️🪓🛠️🪃🏹⚖️⛓️🩸🩹🛏️🛁🧼🫧🧽🏧🚮⚠️☯️☮️♈♉♊♋♌♍♎♏♐♑♒♓⛎📴✖️➕➖➗♾️⁉️❓❔❕❗〰️💱💲♻️✅☑️✔️➰➿©️®️™️🅰️🆎🅱️🆑🆒🆓🆕🆗🆘🆙💠\nUnfortunately, some of these may not work in the bot yet\.\n\n*Why doesn't ❤️ work?*\nTry ♥️\.", parse_mode='MarkdownV2', disable_web_page_preview=True)


def mix(update: Update, context: CallbackContext) -> None:
    pair = update.message.text
    if pair[::-1] in s.dict:
        pair = pair[::-1]
#       # if a reverse of the pair is stored, we swap the requested emoji
    if pair in s.dict:
        file_id=s.dict[pair]
        context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=file_id)
#       # if we have the file saved, just return it, no need to ask Google again
    else:
        mixed = []
        try: 
            mixed += mixer.make_mix(list(pair))
            #print(mixed)
        except IndexError: 
            context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter exactly 2 emoji")
#           # Google mixes them in pairs, so we check the amount
        if mixed[0] == 200 or mixed[0] == 'bruted': 
            file_id = (context.bot.send_sticker(chat_id=config.get('section_a', 'cache_id'), sticker=mixed[1]))['sticker']['file_id']
#           # we can't send files directly from inline mode, so we have to store it in a 'cache' channel
            context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=file_id)
#           # now we can use the posted file's id to send it, either normally or through inline mode
            s.dict[pair] = file_id
            s.sync()
            # if mixed[0] == 'bruted': 
            #     context.bot.send_message(
            #         chat_id=config.get('section_a','owner_id'), 
            #         text=pair + pair.encode('unicode-escape').decode('ASCII'))
        elif mixed[0] == 404:
            context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text="Unfortunately, these emoji don't mix. See /about for the list of available emoji.")
        else: context.bot.send_message(chat_id=update.effective_chat.id, text=f"Weird error. Please report it to @gershik with the emoji that you tried. Code: {mixed[0]}_{pair}")

def inline_mix(update: Update, context: CallbackContext):
    pair = update.inline_query.query
    if not pair:
        return
#       # we check if the inline message field actually contains an request
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
                switch_pm_text = "Unfortunately, these emoji don't mix. See /about for the list of available emoji.",
                switch_pm_parameter = '0')
#           # error messages have to be shown above the message field now
        else:
            context.bot.answer_inline_query(
            update.inline_query.id, results,
            switch_pm_text = f"Weird error. Please report it to @gershik with the emoji that you tried. Code: {mixed[0]}_{pair}",
            switch_pm_parameter = '0')
    context.bot.answer_inline_query(update.inline_query.id, results)
#   # the response is shown above the message field

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
