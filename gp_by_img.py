import operator
import random

import numpy as np

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from utils import draw_logbook, draw_graph

from PIL import Image

from calc_similarity import calc_similarity
from skimage.measure import compare_ssim as ssim
from skimage.measure import compare_mse

from html_renderer import html2img, HTMLRenderer
from calc_color_proportion import get_color_proportion, get_mse_by_pixels, get_diff_by_pixels

from dsl_funcs import *

renderer = HTMLRenderer()

RESULT_IMAGE = Image.open('target.png')
RESULT_IMAGE_ARR = np.array(RESULT_IMAGE)

color_proportion = get_color_proportion(RESULT_IMAGE)
WEIGHTS_MASK = np.array([color_proportion[x] for x in RESULT_IMAGE.getdata()])

pset = gp.PrimitiveSet("MAIN", 1)

# pset.addPrimitive(body, 1)
# pset.addPrimitive(header, 1)
pset.addPrimitive(row, 1)
# pset.addPrimitive(single, 1)
pset.addPrimitive(double, 1)
# pset.addPrimitive(btn_active, 1)
# pset.addPrimitive(btn_inactive, 1)
pset.addPrimitive(btn_green, 1)
pset.addPrimitive(btn_orange, 1)
# pset.addPrimitive(small_title, 1)
# pset.addPrimitive(text, 1)
pset.addPrimitive(concat, 2)

pset.renameArguments(ARG0='x')

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register("expr", gp.genFull, pset=pset, min_=1, max_=6)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)


def evalByColorProportion(ind):
    func = toolbox.compile(expr=ind)
    markup = body(func(x='text'))
    ind_img = renderer.render_html(markup)
    ind_arr = np.array(ind_img)
    if ind_arr.shape != (640, 1024, 4):
        return 10000.0,  #
    dist = get_diff_by_pixels(RESULT_IMAGE, ind_img, weights_mask=WEIGHTS_MASK)
    return dist,


def evalMSE(individual):
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)
    markup = body(func(x='text'))
    ind_img = np.array(html2img(markup))
    if ind_img.shape != (640, 1024, 4):
        return 100.0,
    # dist = distance.braycurtis(RESULT_IMAGE.flatten(), ind_img.flatten())
    # dist = -ssim(RESULT_IMAGE, ind_img, multichannel=True)
    dist = compare_mse(RESULT_IMAGE, ind_img)
    return dist,


toolbox.register("evaluate", evalByColorProportion)
toolbox.register("select", tools.selTournament, tournsize=5)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=3)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))


def main():
    random.seed(318)

    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("min", np.min)
    mstats.register("avg", np.mean)

    pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.2, 20, stats=mstats,
                                   halloffame=hof, verbose=True)
    expr = hof[0]
    tree = gp.PrimitiveTree(expr)

    print('LOSS: {}'.format(evalByColorProportion(expr)))
    print()

    print('CODE: {}'.format(tree))
    print()

    func = toolbox.compile(expr=expr)
    markup = func(x='text')
    print('HTML: \n')
    print(markup)
    print()

    draw_graph(expr)
    draw_logbook(log)

    func = toolbox.compile(expr=expr)
    markup = body(func(x='text'))
    result_img = renderer.render_html(markup)
    result_img.save('output/result_html.png')

    return pop, log, hof


if __name__ == "__main__":
    # main()
    content = row(concat(
        double(btn_green('text')),
        double(btn_orange('text')),
    ))
    print(content)
    markup = body(content)
    open('test.html', 'w').write(markup)
    # img = html2img(markup)
    # img.save('target.png')
