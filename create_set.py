"""Create training and testing data sets from a parent set of data given a 
percentage to use for grabbing observations, or with the option to include all
remaining observations for training sets.

Usage:
     create_set.py <input> <amount> <class> [options]

Options:
    -h --help  Show this screen.
    -v --verbose  Show details during processing.
    -k --keep-all  Keep remainders when sampling.
"""


from collections import namedtuple
from docopt import docopt
import pandas as pd
import random
import sys
import math


def do_splits(args):
    # namedtuple for readability
    group = namedtuple('group', 'name, df, count')

    # flags
    verbose = False
    keep = False
    if args['--verbose']:
        verbose = True
    if args['--keep-all']:
        keep = True

    # load
    df = pd.read_csv(args['<input>'])
    sample_size = float(args['<amount>'])
    class_attr = args['<class>']

    # check if class attribute is even real
    if class_attr not in df.columns:
        print('Class attribute ("{}") not present in data!'.format(class_attr))
        sys.exit(1)

    # check percentage
    if sample_size > 1.0 or sample_size <= 0:
        print('Sample size is not a proper percentage, 0 < x <= 1!')
        sys.exit(1)

    # split up by unique values
    all_groups = [group(n, g, len(g)) for n, g in df.groupby([class_attr])]

    # verbose detail
    if verbose:
        print '-- Preliminary'
        print '{} total groups'.format(len(all_groups))

    # build training and testing set from sample percentage size
    testing_groups = []
    training_groups_preprocess = []
    for g in all_groups:
        sample_count = int(math.ceil(sample_size * g.count))
        rows = random.sample(g.df.index, sample_count)
        t_df = g.df.ix[rows]
        r_df = g.df.drop(rows)
        testing_groups.append(group(g.name, t_df, len(t_df)))
        training_groups_preprocess.append(group(g.name, r_df, len(r_df)))
        if verbose:
            print 'Sampled {}/{} for group {name}' \
                    .format(len(t_df), g.count, name=g.name)

    # verbose detail
    if verbose:
        print '\n-- After sampling'
        print 'Collected a total of {} elems for testing' \
                .format(sum([x.count for x in testing_groups]))

    # deal with remainders
    training_groups = []
    if not keep:
        min_size = min(training_groups_preprocess, key=lambda x: x.count).count
        for g in training_groups_preprocess:
            rows = random.sample(g.df.index, min_size)
            t_df = g.df.ix[rows]
            training_groups.append(group(g.name, t_df, len(t_df)))
        if verbose:
            print '\n-- Remainders'
            print 'Max size a group can maintain {} elems'.format(min_size)
    else:
        training_groups = training_groups_preprocess

    # combine both sets
    testing_df = pd.concat([x.df for x in testing_groups])
    training_df = pd.concat([x.df for x in training_groups])

    # save sorted by index (but do not include it)
    testing_df.sort_index().to_csv('testing.csv', index=False)
    training_df.sort_index().to_csv('training.csv', index=False)


if __name__ == '__main__':
    args = docopt(__doc__)
    do_splits(args)
