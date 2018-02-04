from tag_map import mapping


def header(data):
    return mapping['header'].replace('{}', data)


def body(data):
    return mapping['body'].replace('{}', data)


def row(data):
    return mapping['row'].replace('{}', data)


def text(data):
    return mapping['text'].replace('[]', data)


def small_title(data):
    return mapping['small-title'].replace('[]', data)


def double(data):
    return mapping['double'].replace('{}', data)


def single(data):
    return mapping['single'].replace('{}', data)


def btn_active(data):
    return mapping['btn-active'].replace('[]', data)


def btn_inactive(data):
    return mapping['btn-inactive'].replace('[]', data)


def btn_green(data):
    return mapping['btn-green'].replace('[]', data)


def btn_orange(data):
    return mapping['btn-orange'].replace('[]', data)


def concat(a, b):
    return a + b
