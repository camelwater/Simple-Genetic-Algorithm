# -*- coding: utf-8 -*-
"""
Created on Sat Jun 5 15:30:03 2021

@author: ryanz
"""

def chunks(l, n):
    """
    split list into smaller lists

    Parameters
    ----------
    l : list to split
    n : number of elements per sublist

    Yields
    ------
    smaller lists of l with len(n) each

    """
    for i in range(0, len(l), n):
        yield l[i:i+n]


def is_CJK(char):
    return any([start <= ord(char) <= end for start, end in 
                [(4352, 4607), (11904, 42191), (43072, 43135), (44032, 55215), 
                 (63744, 64255), (65072, 65103), (65381, 65500), 
                 (131072, 196607)]
                ])

from unidecode import unidecode

def sanitize_uni(string, for_search = False):
    '''
    convert known/common un-unidecodable and unicode strings to ASCII and clean string for tag-matching

    '''
  
    ret= []
    for i in string:
        if i in MULT_CHAR_MAP:
            for char in MULT_CHAR_MAP[i]:
                ret.append(char)
            continue
        i = CHAR_MAP.get(i, i)
        if i in VALID_CHARS:
            ret.append(i)
            continue
        
        ret.append(" ")
        # n = unidecode(i)
        # if n=="":
        #     ret.append(" ")
        # elif n in VALID_CHARS:
        #     ret.append(n)
            
    if for_search:
        return ''.join(ret)

    while len(ret)>0:
        if ret[0] in PRE_REMOVE:
            ret.pop(0)
        elif ret[-1] in POST_REMOVE:
            ret.pop(-1)
        else:
            break

    return ''.join(ret)


def sanitize_tag_uni(string):
    '''
    get rid of non-unicode characters that cannot be converted, but keep convertable characters in original form
    '''
    string = [i for i in string if CHAR_MAP.get(i, i) in VALID_CHARS or i in MULT_CHAR_MAP or (unidecode(i)!="" and unidecode(i) in VALID_CHARS)]
    while len(string)>0:
        if string[0] in PRE_REMOVE:
            string.pop(0)
        elif string[-1] in POST_REMOVE:
            string.pop(-1)
        else:
            break

    return ''.join(string)


### constants + maps

VALID_CHARS = "/\*^+-_.!?@%&()\u03A9\u038F" + "abcdefghijklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz0123456789 ".upper()
PRE_REMOVE = "/\*^+-_.!?#%() "
POST_REMOVE = "/\*^+-.!?# "

CHAR_MAP = {
    "Λ": 'A', "λ": 'A', "@": 'A', "Δ": "A", "Ά": "A", "Ã": "A", "À": "A", "Á": "A", "Â": "A", "Ä": "A", "Å": "A", "ά": "a", "à": "a", "á": "a", "â": "a", "ä": "a", "å": "a", "ã": "a", "α": "a", "ª": "a",
    
    "♭": "b", "ß": "B", "β": "B",
    
    "¢": "c", "ς": "c", "ç": "c", "©": "c", "Ç": "C",
    
    "è": "e", "é": "e", "ê": "e", "ë": "e", "ε": "e", "ᵉ": "e", "έ": "E", "€": "E", "Ξ": "E", "ξ": "E", "Σ": "E", "£": "E", "Έ": "E", "È": "E", "É": "E", "Ê": "E", "Ë": "E",
    
    "Ή": "H",

    "ì": "i", "í": "i", "î": "i", "ï": "i", "ι": "i", "ΐ": "i", "ί": "i", "ϊ": "i", "Ϊ": "I", "Ì": "I", "Í": "I", "Î": "I", "Ί": "I", "Ï": "I",
    
    "κ": "k", 

    "ñ": "n", "η": "n", "ή": "n", "Ñ": "N", "Π": "N",

    "σ": "o", "○": "o", "º": "o", "ο": "o", "ò": "o", "ó": "o", "ό": "o", "ô": "o", "ö": "o", "ø": "o", "δ": "o", "õ": "o", "Ό": "O", "Ò": "O", "Ó": "O", "Ô": "O", "Ö": "O", "Ø": "O", "Õ": "O", "θ": "O", "φ": "O", "Θ": "O", "Φ": "O", "Ω": "O", "Ώ": "O", "◎": "O",
    
    "や": "P", "ρ": "p",
    
    "π": "r", "Г": "r", "®": "R",
    
    "$": "S", "§": "S",
    
    "τ": "t",
    
    "μ": "u", "ù": "u", "ú": "u", "û": "u", "ü": "u", "ϋ": "u", "ύ": "u", "Ù": "U", "Ú": "U", "Û": "U", "Ü": "U", "ΰ": "U", "υ": "u",
    
    "ν": "v",

    "ώ": "w", "Ψ": "w", "ω": "w", "ψ": "W",
    
    "χ": "X",
    
    "ý": "y", "ÿ": "y", "γ": "y", "¥": "Y", "Ύ": "Y", "Ϋ": "Y", "Ý": "Y", "Ÿ": "Y",
    
    "ζ": "Z"
}

MULT_CHAR_MAP = {
    "Æ": 'AE',
    "æ": "ae",

    "œ": "oe",
    "Œ": "OE",

    "™": "TM"
}

if __name__ == "__main__":
    import time
    i = "Player"
    sans = []
    t = time.time()
    for _ in range(100):
        sans.append(sanitize_uni(i))
    print(time.time()-t)
    print(sans[0])
    
