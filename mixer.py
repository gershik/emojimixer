import io
import requests
from PIL import Image
import emojilist
PREFIX = 'https://www.gstatic.com/android/keyboard/emojikitchen/'
def generate_urls(emoji):
        url_variants = []

        codes = emoji
        for j in range(0,2):
            for num, current in enumerate(codes):
                if current == '200d':
#               # exception for a special symbol
                    for i in range(0,2):
                        codes[num-1] += f'-u{codes[num]}'
                        codes.pop(num)
                if current == 'fe0f':
#               # exception for a special symbol
                    codes[num-1] += f'-u{codes[num]}'
                    codes.pop(num)
        #print(codes)
#       # here, we convert the given emoji into their Unicode numbers
#       # a few characters break the way they are encoded in Google's database, so we fix them         
        for date in emojilist.dates:
            url_variants += [
                            f'{PREFIX}{date}/u{codes[1]}/u{codes[1]}_u{codes[0]}.png',
                            f'{PREFIX}{date}/u{codes[0]}/u{codes[0]}_u{codes[1]}.png',
                        ]
        return(url_variants)
#       # we generate two URLs for each stored date to find the combined image
#       # we have to make two, since Google randomly decides the order emoji are ordered in a pair

def make_mix(emoji):
    #print(emoji)
    for bundle in emojilist.redirects:
        for index, current_given in enumerate(emoji):
            if current_given == '\ufe0f' or current_given == '\u200d' or emoji[index-1] == '\u200d':
                continue
            if current_given in bundle[0]:
                emoji[index] = bundle[0][0]
                    
    #print(emoji)
    codes = ['', '']
    num = 0
    for i in emoji:
        j = i.encode('unicode-escape').decode('ASCII')
        if 'ufe0f' in j: 
            codes += ['']
            codes[num] += j[2:]
        elif 'u200d' in j:
            codes += ['', '']
            codes[num] += j[2:]
        elif '1f573' in j or '1f577' in j:
            codes[num] += j[5:] + '-ufe0f'
            #print(j)
        elif 'u' in j:
            codes[num] += j[2:]
        else: 
            codes[num] += j[5:]
        num += 1

    url_variants = generate_urls(codes)
    print(url_variants)

    for url in url_variants: 
        response = requests.get(url, stream=True)
        if response.status_code != 404: 
            break
    if response.status_code == 404: 
        # if '\u2665' in emoji or '\u2764' in emoji:
        #     make_mix([i.replace('\u2764','\u2665') for i in emoji])
        #     #make_mix([i.replace('\u2665','\u2764') for i in emoji])
        #     # print([i.encode('unicode-escape').decode('ASCII') for i in a])
        #     # make_mix([i.replace('\u2665','\u2764') for i in emoji])
        #     # make_mix([i.replace('\u2764','\u2665') for i in emoji])
        return 404, 404
#   # convert the result into a webp with Pillow and return it
    
    image = Image.open(io.BytesIO(response.content))
    image = image.convert('RGBA')
    img = io.BytesIO()
    image.save(img, format='webp')
    #image.save(open ('img.webp', 'wb'), format='webp')
    sticker=img.getvalue()
#   # convert the result into a webp with Pillow and return it
    
    if len(url_variants) > 2: 
        return 'bruted', sticker
#   # if the emoji hadn't been stored before, we return a 'bruted' status to add it to the database

    return response.status_code, sticker

#make_mix(list('🐯🐱'))
