# dectree

`create_set.py` will create the training and testing sets of data (to CSV) for use with `create_tree.py`. I will likely need another script in the near future to do the prediction/testing of data.


## usage

#### `create_set.py`

```
Create training and testing data sets from a parent set of data given a 
percentage to use for grabbing observations, or with the option to include all
remaining observations for training sets.

Usage:
     create_set.py <input> <amount> <class> [options]

Options:
    -h --help  Show this screen.
    -v --verbose  Show details during processing.
    -k --keep-all  Keep remainders when sampling.
```

---

#### `create_tree.py`

```
Create a DecisionTree from a training set. Be sure to specify a Graphviz
output or else this will all be for naught.

Usage:
    create_tree.py <input> <class> [options]

Options:
    -h --help  Show this screen.
    -v --verbose  Verbose mode.
    -s SAMPLES --samples SAMPLES  Minimum samples for a grouping [default: 20].
    -e EXCEPT --except EXCEPT  Columns to exclude (comma delimited).
    -o OUT --output OUT  Filename for graphviz output (no extension).
```

## references

This [post][chris] by Chris Strelioff helped me greatly.

[chris]: http://chrisstrelioff.ws/sandbox/2015/06/08/decision_trees_in_python_with_scikit_learn_and_pandas.html
