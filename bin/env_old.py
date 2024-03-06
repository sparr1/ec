import datetime
import os
import random

import binutil  # required to import from dreamcoder modules

from dreamcoder.ec import commandlineArguments, ecIterator
from dreamcoder.grammar import Grammar
from dreamcoder.program import Primitive
from dreamcoder.task import Task
from dreamcoder.type import arrow, tint, tpair, tbool, tlist, t0
from dreamcoder.utilities import numberOfCPUs

# Primitives
# def _zero(): return 0
# def _one(): return 1
def _incr(x): return x + 1
def _decr(x): return x - 1
def _modulo(x): return lambda n: x%n
def _eq(x): return lambda y: x==y
def _not(x): return not x
# def _if(x,y,z): return lambda x,y,z: y if x else z
def _ge(x): return lambda y: x>=y
def _if(c): return lambda t: lambda f: t if c else f
# def _concat(x,y): return lambda x,y: (x,y)
# def _left_separate(x,y): return lambda x,y: x
# def _right_separate(x,y): return lambda x,y: y
# def _empty(): return []
# def _append(l,a): return lambda l,a: l + a OLD

# def _index(l, i): return lambda l,i: l[i]
def _cons(x): return lambda y: [x] + y
# def _append(x): return lambda y: x + y
def _index(j): return lambda l: l[j]

def transitionN(d):
    x = random.choice(range(d))
    y = random.choice(range(d))
    a = random.choice(range(4))
    # up, down, left, right
    if a == 0:
        ox = x
        oy = (y+1) % d
    elif a == 1:
        ox = x
        oy = (y-1) % d
    elif a == 2:
        ox = (x-1) % d
        oy = y
    elif a == 3:
        ox = (x+1) % d
        oy = y
    return {"i": (x,y,a), "o": (ox,oy)}


def simple_transition_test(d):
    x = random.choice(range(d))
    a = random.choice(range(2))
    # up, down, left, right
    if a == 0:
        ox = (x+1) % d
    else:
        ox = (x-1) % d
    return {"i": [x,a], "o": [ox]}

def wall_transition_test(d):
    x = random.choice(range(d))
    a = random.choice(range(2))
    # up, down, left, right
    if a == 0:
        ox = (x+1) if x <= d - 1 else x
    else:
        ox = (x-1) if x > 0 else x

    return {"i": [x,a], "o": [ox]}

def simple_mod_test(d):
    x = random.choice(range(d))
    return {"i": [x], "o": [(x+1) % d]}

def simple_eq_test(d):
    x = random.choice(range(d))
    y = random.choice(range(d))
    return {"i": [x,y], "o": [x==y]}

def simple_if_test(d):
    c = random.choice([True,False])
    # w = random.choice(range(d))
    x = random.choice(range(d))
    y = random.choice(range(d))
    # z = random.choice(range(d))
    return {"i": (c,x,y), "o": x if c else y}

simple_test = wall_transition_test

def get_tint_task(item):
    return Task(
        item["name"],
        arrow(tlist(tint), tlist(tint)),
        [((ex["i"],), ex["o"]) for ex in item["examples"]],
    )
# def get_strans_task(item):
#     return Task(
#         item["name"],
#         arrow(tlist(tint), tlist(tint)),
#         [((ex["i"],), ex["o"]) for ex in item["examples"]],
#     )

def get_tbool_task(item):
    return Task(
        item["name"],
        arrow(tlist(tint), tlist(tbool)),
        [((ex["i"],), ex["o"]) for ex in item["examples"]],
    )

def get_if_task(item):
    return Task(
        item["name"],
        arrow(tbool, tint, tint, tint),
        [(ex["i"], ex["o"]) for ex in item["examples"]],
    )

# def get_if2_task(item):
#     return Task(
#         item["name"],
#         arrow(tlist(tint), tlist(tint)),
#         [((ex["i"],), ex["o"]) for ex in item["examples"]],
#     )

def get_transition_task(item):
    return Task(
        item["name"],
        arrow(tint, tint, tint, tint, tint),
        [(ex["i"], ex["o"]) for ex in item["examples"]],
    )

get_task = get_tint_task

if __name__ == "__main__":

    # Options more or less copied from list.py

    args = commandlineArguments(
        enumerationTimeout=10, activation='tanh',
        iterations=10, recognitionTimeout=7200,
        a=3, maximumFrontier=10, topK=2, pseudoCounts=30.0,
        helmholtzRatio=0.5, structurePenalty=1.,
        CPUs=numberOfCPUs())

    timestamp = datetime.datetime.now().isoformat()
    outdir = 'experimentOutputs/demo/'
    os.makedirs(outdir, exist_ok=True)
    outprefix = outdir + timestamp
    args.update({"outputPrefix": outprefix})

    # Create list of primitives

    primitives = [
        Primitive("0", tint, 0),
        Primitive("1", tint, 1),
        # Primitive("2", tint, 2),
        # Primitive("3", tint, 3),
        # Primitive("4", tint, 4),
        # Primitive("5", tint, 5),
        # Primitive("6", tint, 6),
        # Primitive("7", tint, 7),
        # Primitive("8", tint, 8),
        # Primitive("9", tint, 9),
        # Primitive("10", tint, 10),
        Primitive("true", tbool, True),
        Primitive("not", arrow(tbool, tbool), _not),
        Primitive("incr", arrow(tint, tint), _incr),
        Primitive("decr", arrow(tint, tint), _decr),
        # Primitive("mod", arrow(tint, tint, tint), _modulo),
        Primitive("eq?", arrow(tint, tint, tbool), _eq),
        Primitive("if", arrow(tbool, t0, t0, t0), _if),
        Primitive("gt?", arrow(tint, tint, tbool), _ge),

        # Primitive("concat", arrow(tint, tint, tpair(tint, tint)), _concat),
        # # Primitive("concat", arrow(tint, tint, tlist(tint)), _concat),
        # Primitive("left_separate", arrow(tpair(tint, tint), tint), _left_separate),
        # Primitive("right_separate", arrow(tpair(tint, tint), tint), _right_separate),

        # Primitive("empty", tlist, _empty),
        # Primitive("append", arrow(tint, tlist(tint), tlist(tint)), _append),
        # Primitive("index", arrow(tint, tlist(tint), tint), _index),

        Primitive("empty", tlist(t0), []),
        Primitive("cons", arrow(t0, tlist(t0), tlist(t0)), _cons),
        Primitive("index", arrow(tint, tlist(t0), t0), _index),
    ]


    # Create grammar

    grammar = Grammar.uniform(primitives)

    def transition2(): return transitionN(2)
    def transition3(): return transitionN(3)
    def transition4(): return transitionN(4)

    def simple_test2(): return simple_test(2)
    def simple_test3(): return simple_test(3)
    def simple_test4(): return simple_test(4)
    # def simple_test2(): return simple_test(2)
    # def simple_test3(): return simple_test(3)
    # def simple_test4(): return simple_test(4)
    # Training data
    training_examples = []
    # training_examples = [
    #     {"name": "simple_test2", "examples": [simple_test2() for _ in range(10000)]},
    #     {"name": "simple_test3", "examples": [simple_test3() for _ in range(10000)]},
    #     {"name": "simple_test4", "examples": [simple_test4() for _ in range(10000)]},
    # ]
    test_name = "simple_test"
    num_tests = 10
    for i in range(2, num_tests):
        def simple_testr(): return simple_test(i)
        training_examples.append({"name": test_name+str(i), "examples": [simple_testr() for _ in range(10000)]})
    training = [get_task(item) for item in training_examples]

    # Testing data

    def transition5(): return transitionN(5)

    testing_examples = [
        # {"name": "transition3", "examples": [transition3() for _ in range(5000)]},
        # {"name": "transition5", "examples": [transition5() for _ in range(500)]},
    ]
    def simple_testr3(): return simple_test(i+1)
    def simple_testr4(): return simple_test(i+2)
    testing_examples.append({"name": test_name+str(i+1), "examples": [simple_testr3() for _ in range(10000)]})
    testing_examples.append({"name": test_name+str(i+2), "examples": [simple_testr4() for _ in range(10000)]})

    testing = [get_task(item) for item in testing_examples]

    # EC iterate

    generator = ecIterator(grammar,
                           training,
                           testingTasks=testing,
                           **args)
    for i, _ in enumerate(generator):
        print('ecIterator count {}'.format(i))
