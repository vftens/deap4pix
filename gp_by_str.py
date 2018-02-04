mapping = {
    "opening-tag": "{",
    "closing-tag": "}",
    "body": "<html>\n  <header>\n    <meta charset=\"utf-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n    <link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\" integrity=\"sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u\" crossorigin=\"anonymous\">\n<link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css\" integrity=\"sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp\" crossorigin=\"anonymous\">\n<style>\n.header{margin:20px 0}nav ul.nav-pills li{background-color:#333;border-radius:4px;margin-right:10px}.col-lg-3{width:24%;margin-right:1.333333%}.col-lg-6{width:49%;margin-right:2%}.col-lg-12,.col-lg-3,.col-lg-6{margin-bottom:20px;border-radius:6px;background-color:#f5f5f5;padding:20px}.row .col-lg-3:last-child,.row .col-lg-6:last-child{margin-right:0}footer{padding:20px 0;text-align:center;border-top:1px solid #bbb}\n</style>\n    <title>Scaffold</title>\n  </header>\n  <body>\n    <main class=\"container\">\n      {}\n      <footer class=\"footer\">\n        <p>&copy; Tony Beltramelli 2017</p>\n      </footer>\n    </main>\n    <script src=\"js/jquery.min.js\"></script>\n    <script src=\"js/bootstrap.min.js\"></script>\n  </body>\n</html>\n",
    "header": "<div class=\"header clearfix\">\n  <nav>\n    <ul class=\"nav nav-pills pull-left\">\n      {}\n    </ul>\n  </nav>\n</div>\n",
    "btn-active": "<li class=\"active\"><a href=\"#\">[]</a></li>\n",
    "btn-inactive": "<li><a href=\"#\">[]</a></li>\n",
    "row": "<div class=\"row\">{}</div>\n",
    "single": "<div class=\"col-lg-12\">\n{}\n</div>\n",
    "double": "<div class=\"col-lg-6\">\n{}\n</div>\n",
    "quadruple": "<div class=\"col-lg-3\">\n{}\n</div>\n",
    "btn-green": "<a class=\"btn btn-success\" href=\"#\" role=\"button\">[]</a>\n",
    "btn-orange": "<a class=\"btn btn-warning\" href=\"#\" role=\"button\">[]</a>\n",
    "btn-red": "<a class=\"btn btn-danger\" href=\"#\" role=\"button\">[]</a>",
    "big-title": "<h2>[]</h2>",
    "small-title": "<h4>[]</h4>",
    "text": "<p>[]</p>\n"
}

import operator
import math
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

import multiprocessing

from calc_similarity import calc_similarity


def header(data):
    return mapping['header'].replace('{}', data)


def body(data):
    return mapping['body'].replace('{}', data)


def row(data):
    return mapping['row'].replace('{}', data)


def btn(data):
    return mapping['btn-green'].replace('[]', 'text')


def btn_green(data):
    return mapping['btn-green'].replace('[]', data)


def btn_orange(data):
    return mapping['btn-orange'].replace('[]', data)


def double(data):
    return mapping['double'].replace('{}', data)


# def block_row_btn(data):
#     return row(btn(data))


def concat(a, b):
    return a + b


RESULT_HTML = body(row(concat(
        double(btn_green('text')),
        double(btn_orange('text')),
    )))

pset = gp.PrimitiveSet("MAIN", 1)
pset.addPrimitive(body, 1)
# pset.addPrimitive(header, 1)
pset.addPrimitive(row, 1)
pset.addPrimitive(double, 1)
pset.addPrimitive(btn_green, 1)
pset.addPrimitive(btn_orange, 1)
# pset.addPrimitive(block_row_btn, 1)
# pset.addPrimitive(btn, 1)
pset.addPrimitive(concat, 2)
pset.renameArguments(ARG0='x')

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register("expr", gp.genFull, pset=pset, min_=1, max_=6)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)


def evalSymbReg(individual):
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)
    markup = func(x='text')
    code = str(gp.PrimitiveTree(individual))
    # result_code = 'body(concat(header(concat(btn(x), btn(x))), concat(btn(x), btn(x))))'
    # result_code = 'body(header(concat(btn(x), btn(x))))'
    # code = str(gp.PrimitiveTree(individual))
    # return -len(set(result_code) & set(code)) - (10 if result_code == code else 0),
    return -calc_similarity(RESULT_HTML, markup),


pool = multiprocessing.Pool(processes=4)
# toolbox.register("map", pool.map)

toolbox.register("evaluate", evalSymbReg)
toolbox.register("select", tools.selTournament, tournsize=4)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=3)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)


# toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
# toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))


def main():
    random.seed(318)

    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("max", numpy.mean)

    pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 20, stats=mstats,
                                   halloffame=hof, verbose=True)
    expr = hof[0]
    tree = gp.PrimitiveTree(expr)

    print('SCORE: \n')
    print(evalSymbReg(expr))
    print()

    print('CODE: \n')
    print(tree)
    print()

    func = toolbox.compile(expr=expr)
    markup = func(x='text')
    # print('HTML: \n')
    # print(markup)
    # print()

    # print('RESULT HTML: \n')
    # print(RESULT_HTML)
    return pop, log, hof


if __name__ == "__main__":
    main()
