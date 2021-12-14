import io
import requests
from PIL import Image
import emojilist
PREFIX = 'https://www.gstatic.com/android/keyboard/emojikitchen/'

def make_mix(emoji):
    url_variants = []
    codes = ['', '']
    num = 0
    for i in emoji:
        #print(i)
        j = i.encode('unicode-escape').decode('ASCII')
        if 'ufe0f' in j: 
            continue
        elif 'u' in j:
            codes[num] += j[2:]
           # print(j, 'u')
        else: 
            codes[num] += j[5:]
            #print(j, 'no u')
        num += 1
    #print(codes)
    try:
        url_variants = [
            f'{PREFIX}{emojilist.available_emoji[codes[1]]}/u{codes[1]}/u{codes[1]}_u{codes[0]}.png',
            f'{PREFIX}{emojilist.available_emoji[codes[0]]}/u{codes[0]}/u{codes[0]}_u{codes[1]}.png',
        ]
    except KeyError:
        for date in emojilist.dates:
            url_variants += [
                f'{PREFIX}{date}/u{codes[1]}/u{codes[1]}_u{codes[0]}.png',
                f'{PREFIX}{date}/u{codes[0]}/u{codes[0]}_u{codes[1]}.png',
                ]
    for url in url_variants: 
        print(url)
        response = requests.get(url, stream=True)
        if response.status_code != 404: 
            break
    if response.status_code == 404: 
        return 404, 404
    
    image = Image.open(io.BytesIO(response.content))
    image = image.convert('RGBA')
    img = io.BytesIO()
    image.save(img, format='webp')
    #image.save(open ('img.webp', 'wb'), format='webp')
    sticker=img.getvalue()
    
    if len(url_variants) > 2: 
        return 'bruted'
    else: return response.status_code, sticker

#make_mix(list('☃️🌇'))
