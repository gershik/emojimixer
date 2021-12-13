import io
import requests
from PIL import Image
import emojilist

def make_mix(emoji):
    url_variants = []
    codes = [i.encode('unicode-escape').decode('ASCII')[5:] for i in emoji]

    try:
        url_variants = [
            f'https://www.gstatic.com/android/keyboard/emojikitchen/{emojilist.available_emoji[codes[1]]}/u{codes[1]}/u{codes[1]}_u{codes[0]}.png',
            f'https://www.gstatic.com/android/keyboard/emojikitchen/{emojilist.available_emoji[codes[0]]}/u{codes[0]}/u{codes[0]}_u{codes[1]}.png',
        ]
    except KeyError:
        for date in emojilist.dates:
            url_variants += [
                f'https://www.gstatic.com/android/keyboard/emojikitchen/{date}/u{codes[1]}/u{codes[1]}_u{codes[0]}.png',
                f'https://www.gstatic.com/android/keyboard/emojikitchen/{date}/u{codes[0]}/u{codes[0]}_u{codes[1]}.png',
                ]
    for url in url_variants: 
        response = requests.get(url, stream=True)
        if response.status_code != 404: 
            break
    if response.status_code == 404: 
        return 404, 404
    
    image = Image.open(io.BytesIO(response.content))
    image = image.convert('RGBA')
    img = io.BytesIO()
    image.save(img, format='webp')
    sticker=img.getvalue()
    
    if len(url_variants) > 2: 
        return 'bruted'
    else: return response.status_code, sticker

#make_mix(list('🐱🎁'))
