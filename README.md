# Emoji Mixer 

## What?

Google's Gboard on Android has an interesting feature called Emoji Kitchen. Using images that were designed in advance and are stored on Google's servers, it lets users 'mix' two emoji into one, using the combination as a sticker. This bot was designed to emulate this feature for iOS users and those, who like to use to use Telegram on a computer.

## How?

Google stores the combinations on their servers. They can be accessed by links that look like `https://www.gstatic.com/android/keyboard/emojikitchen/{date}/{emoji1}/{emoji2}.png`, where `{date}` means the day the update adding the combination was released, and the actual emoji are referred to as their Unicode numbers. The bot's job is to generate such a link, get the PNG file, convert it to WEBP, which is the format Telegram uses for stickers, and send it.

## How do I run it?
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 bot.py
```
The built-in config generator will help you do the rest.

## The code
has some comments. You should look at them to see how it works.

## TODO
- [x] Process [multi-character emoji](https://emojipedia.org/variation-selector-16/)
- [ ] Refactor the code to make it more efficient
- [ ] Show recent combinations in inline mode
- [ ] Get the bot to update the list of dates by itself
- [ ] Think of a way to make it work in groups