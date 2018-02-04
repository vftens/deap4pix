import asttokens, ast

from collections import Counter


def extract_duplicate_subtrees(expr):
    atok = asttokens.ASTTokens(expr, parse=True)

    tree_code = atok.get_text(atok.tree)

    tokens = [atok.get_text(n) for n in ast.walk(atok.tree)]
    cntr = Counter(tokens)

    replaces = []

    for node_code, count in cntr.items():
        if node_code.count('(') > 1 and count > 1 and node_code != tree_code:
            replaces.append(node_code)
    return replaces


if __name__ == '__main__':
    expr = "body(header(concat(row(btn('text')), row(btn('text')))))"
    to_replace_subtrees = extract_duplicate_subtrees(expr)
    for st in to_replace_subtrees:
        print(st)
