import difflib

text1 = 'body(concat(header(concat(btn(x), btn(x))), concat(btn(x), btn(x))))'
text2 = 'body(concat(header(concat(btn(x), btn(x))), concat(btn(x), btn(x))))'
text3 = 'body(concat(body(concat(btn(x), btn(x))), concat(btn(x), btn(x))))'


def calc_similarity(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).ratio()


if __name__ == "__main__":
    print('Text 1 VS text 2: {}'.format(calc_similarity(text1, text2)))
    print('Text 1 VS text 3: {}'.format(calc_similarity(text1, text3)))
