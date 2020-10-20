# -*- coding: utf-8 -*-
# fork from https://github.com/Giaola/python-greeklish with some modifications

class Generator(object):
    # The possible accents
    ACCENTS = {
        u'ά': u'α', u'Ά': u'Α',
        u'έ': u'ε', u'Έ': u'Ε',
        u'ή': u'η', u'Ή': u'Η',
        u'ί': u'ι', u'Ί': u'Ι',
        u'ύ': u'υ', u'Ύ': u'Υ',
        u'ό': u'ο', u'Ό': u'Ο',
        u'ώ': u'ω', u'Ώ': u'Ω'
    }

    # The possible digraph cases.
    DIGRAPH_CASES = [
        u"αι", u"Αι", u"ΑΙ",
        u"ει", u"Ει", u"ΕΙ",
        u"οι", u"Οι", u"ΟΙ",
        u"ου", u"Ου", u"ΟΥ",
        u"ευ", u"Ευ", u"ΕΥ",
        u"αυ", u"Αυ", u"ΑΥ",
        u"μπ", u"Μπ", u"ΜΠ",
        u"γγ", u"Γγ", u"ΓΓ",
        u"γκ", u"Γκ", u"ΓΚ",
        u"ντ", u"Ντ", u"ΝΤ"
    ]

    # The possible string conversions for each case.
    CONVERT_STRINGS = {
        u"αι": [u"ai"],
        u"Αι": [u"Ai"],
        u"ΑΙ": [u"AI"],
        u"ει": [u"ei"],
        u"Ει": [u"Ei"],
        u"ΕΙ": [u"EI"],
        u"οι": [u"oi"],
        u"Οι": [u"Oi"],
        u"ΟΙ": [u"OI"],
        u"ου": [u"ou"],
        u"Ου": [u"Ou"],
        u"ΟΥ": [u"OU"],
        u"ευ": [u"eu"],
        u"Ευ": [u"Eu"],
        u"ΕΥ": [u"EU"],
        u"αυ": [u"au"],
        u"Αυ": [u"Au"],
        u"ΑΥ": [u"AU"],
        u"μπ": [u"mp"],
        u"Μπ": [u"Mp"],
        u"ΜΠ": [u"MP"],
        u"γγ": [u"gg"],
        u"Γγ": [u"Gg"],
        u"ΓΓ": [u"GG"],
        u"γκ": [u"gk"],
        u"Γκ": [u"Gk"],
        u"ΓΚ": [u"GK"],
        u"ντ": [u"nt"],
        u"Ντ": [u"Nt"],
        u"ΝΤ": [u"NT"],
        u"α": [u"a"],
        u"Α": [u"A"],
        u"β": [u"v"],
        u"Β": [u"V"],
        u"γ": [u"g"],
        u"Γ": [u"G"],
        u"δ": [u"d"],
        u"Δ": [u"D"],
        u"ε": [u"e"],
        u"Ε": [u"E"],
        u"ζ": [u"z"],
        u"Ζ": [u"Z"],
        u"η": [u"i"],
        u"Η": [u"I"],
        u"θ": [u"th"],
        u"Θ": [u"TH"],
        u"ι": [u"i"],
        u"Ι": [u"I"],
        u"κ": [u"k"],
        u"Κ": [u"K"],
        u"λ": [u"l"],
        u"Λ": [u"L"],
        u"μ": [u"m"],
        u"Μ": [u"M"],
        u"ν": [u"n"],
        u"Ν": [u"N"],
        u"ξ": [u"ks"],
        u"Ξ": [u"KS"],
        u"ο": [u"o"],
        u"Ο": [u"O"],
        u"π": [u"p"],
        u"Π": [u"P"],
        u"ρ": [u"r"],
        u"Ρ": [u"R"],
        u"σ": [u"s"],
        u"Σ": [u"S"],
        u"ς": [u"s"],
        u"τ": [u"t"],
        u"Τ": [u"T"],
        u"υ": [u"y"],
        u"Υ": [u"Y"],
        u"φ": [u"f"],
        u"Φ": [u"F"],
        u"χ": [u"h"],
        u"Χ": [u"H"],
        u"ψ": [u"ps"],
        u"Ψ": [u"PS"],
        u"ω": [u"o"],
        u"Ω": [u"O"]
    }

    def __init__(self, max_expansions):
        self.max_expansions = max_expansions
        self.greeklish_list = []
        self.per_word_greeklish = []

    def generate_greeklish_words(self, greek_word):
        self.greeklish_list = []

        self.per_word_greeklish = []
        greek_word = self.remove_accent_chars(greek_word)
        greek_word = self.convert_to_dict(greek_word)

        for greek_char in greek_word:
            if greek_char in self.CONVERT_STRINGS:
                self.add_character(self.CONVERT_STRINGS[greek_char])
            else:
                self.add_character(greek_char)

        for word in self.per_word_greeklish:
            self.greeklish_list.append(word)

        return self.greeklish_list

    def remove_accent_chars(self, word):
        for accent_char in self.ACCENTS:
            word = word.replace(accent_char, self.ACCENTS[accent_char])
        return word

    def convert_to_dict(self, word):
        dictword = []
        skipchar = False
        maxL = len(word)
        for index, obj in enumerate(word):
            if skipchar:
                skipchar = False
                continue
            if index < (maxL - 1):
                if word[index] + word[index + 1] in self.DIGRAPH_CASES:
                    dictword.append(word[index] + word[index + 1])
                    skipchar = True
                else:
                    dictword.append(word[index])
            else:
                dictword.append(word[index])
        return dictword

    def add_character(self, convert_strings):
        # list is empty
        if not self.per_word_greeklish:
            for string in convert_strings:
                self.per_word_greeklish.append(string)
        else:
            new_tokens = []
            for convert_string in convert_strings:
                for token in self.per_word_greeklish:
                    if len(new_tokens) >= self.max_expansions:
                        break
                    new_tokens.append(token + convert_string)
            self.per_word_greeklish = new_tokens


class Converter(object):

    def __init__(self, max_expansions=4):
        self.generator = Generator(max_expansions)

    def convert(self, input_token):
        self.greek_words = input_token

        return self.generator.generate_greeklish_words(self.greek_words)
