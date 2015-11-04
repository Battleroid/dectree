"""Create a DecisionTree from a training set. Be sure to specify a Graphviz
output or else this will all be for naught.

Usage:
    create_tree.py <input> <class> [options]

Options:
    -h --help  Show this screen.
    -v --verbose  Verbose mode.
    -s SAMPLES --samples SAMPLES  Minimum samples for a grouping [default: 20].
    -e EXCEPT --except EXCEPT  Columns to exclude (comma delimited).
    -o OUT --output OUT  Filename for graphviz output (no extension).
"""


from docopt import docopt
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import pandas as pd
import sys


def create_tree(args):
    # load
    df = pd.read_csv(args['<input>'])
    class_attr = args['<class>']

    # check
    if class_attr not in df.columns:
        print('Class attribute "{}" not in dataset!'.format(class_attr))
        sys.exit(1)

    # flags & options
    verbose = False
    if args['--verbose']:
        verbose = True
    exceptions = None
    output = None
    if args['--output']:
        output = args['--output']
    if args['--except']:
        exceptions = args['--except'].split(',')
    samples = int(args['--samples'])
    
    # get numeric columns and drop class and exceptions (our features)
    features = df._get_numeric_data().columns.difference([class_attr])
    if exceptions:
        features = features.difference(exceptions)

    # create tree
    dt = DecisionTreeClassifier(
            min_samples_split=samples, 
            criterion='entropy',
            splitter='best',
            random_state=99)
    y = df[class_attr]
    X = df[features]
    dt.fit(X, y)

    # export graph of tree if graph output specified
    if output:
        import subprocess

        # save dot
        with open(output + '.dot', 'w') as f:
            export_graphviz(dt, out_file=f, feature_names=features)

        command = 'dot -Tpng {0}.dot -o {0}.png'.format(output).split()
        try:
            subprocess.check_call(command)
        except:
            print('Problem creating graphviz image, is graphviz installed?')
            sys.exit(1)



if __name__ == '__main__':
    args = docopt(__doc__)
    create_tree(args)
