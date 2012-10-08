#
# (c) Noprianto <nop@tedut.com>, 2008-2009, GPL
#

import locale

def string_sep_rebuild(str, separator=',', remove_space=True, 
    unique=True, replace_underscore_with_space=True):
    str = str.strip()
    splitted = str.split(separator)
    splitted2 = [x.strip() for x in splitted]
    if remove_space:
        splitted3 = [x.replace(' ', '') for x in splitted2]
    else:
        splitted3 = splitted2
    
    if unique:
        splitted4 = []
        for i in splitted3:
            if i not in splitted4:
                splitted4.append(i)
    else:
        splitte4 = splitted3

    if replace_underscore_with_space:
        splitted5 = [x.replace('_', ' ') for x in splitted4]
    else:
        splitted5 = splitted4
        
    newlist = []
    for part in splitted5:
        if part:
            newlist.append(part)
    ret = separator.join(newlist)
    return ret

def number_format(number, places=0, lang='en_US'):
    locale.setlocale(locale.LC_ALL, lang)
    formatted = locale.format('%.*f', (places, number), True, True)
    return formatted
