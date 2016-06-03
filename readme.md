# Code repository for paper titled 'Near-Optimal Fingerprinting with Constraints'

## What is this for?
This repository serves the codebase of a scientific conference paper in [1]. The paper shows that limiting the availability of user attributes is not enough for mainting user privacy. In fact, this is shown in two "hot" areas the paper:

1. Apple iOS 9 introduced limitations on application detection. While this definitely limits what could be learnt from each user this way, this still leaves the possibility open for several attacks that aim to re-identify users or to link users in multiple databases.
2. Recently outdated versions (up to version 5.5) Tor Browser, used a similar protection mechanism to protect against fingerprinting based web tracking: by default a webpage was only allowed to load at most 10 fonts. (In version 5.5 developers started using another privacy protection mechanism due to implementation difficulties.)

As this method is still considered as a valid approach to protect user privacy, the paper shows that it is in fact a weak protection method and if possible, should be avoided.

The paper is available here: [Near-Optimal Fingerprinting with Constraints](https://arxiv.org/abs/1605.08664)

## How can I use this?

The code is consisting of three parts:

1. We cannot release our dataset publicly, so the a toy dataset needs to be set up. We use the [UCI Adult Data Set](https://archive.ics.uci.edu/ml/datasets/Adult) for this purpose. Although it is a regular tabular dataset, and has a Gausian distribution instead of a heavy tailed one over the attributes, it is fine for experimenting. Then you can work on your own.
2. Scripts generating and analysing _targeted fingerprints_ for individuals (please see the paper for more details).
3. Scripts generating and analysing _general fingerprints_ over the whole dataset (please see the paper for more details).

You can use `python` for the first step, then `pypy` to speed things up.

### (1) Data generation

Simply run the first file (`01_build_dataset.py`), it will download the dataset in question, and will also convert it to the necessary format.

Finally, it will create two files in the `./data/` folder:

* `attrs.csv` for storing list of users having a the same attribute (each line is an attribute).
* `users.csv` for storing list of attributes per user (each line is a user).

You can have multiple datasets, these should be differentiated with a postfix.

### (2) Evaluation of targeted fingerprinting

The operation is based on configuration files stored in `./config/`. These `json` files have a couple of entries, and could be used as:

* `type`: which individual fingerprinting algorithm shall be used. There are two algorithms that could be added here:
  * `paper`: the exact algorithm that you can find in the paper.
  * `faster`: we provide another algorithm for fast experimentation. We observed that while this algorithm is a bit less precise than the other one, it is faster when the attribute space is large; plus, results are just a bit behind compard to the other one.
* `data_pref`: dataset postfix; e.g., `users_movies.csv`, from where `movies` should be added here.
* `limit`: limit for attribute queryies. For example, in case of iOS 9 this is 50, and 10 for the Tor Browser.
* `user_limit`: for faster experimentation it can be nice if only a part of the dataset is used. Use -1 if you need the whole dataset.
* `first_col`: in some cases the CSV file can start with line numbering. With this variable, you can control how many columns need to be skipped from the beginning of each line. Use 0 if none.

Output in all cases is provided in `./results/`.

First you can run either the script file running algorithm `paper` (`02_individual_fingerprints.py`) or for algorithm `faster` (`03_individual_fingerprints_faster.py`). The basic config file wired into the following scripts assume that you run `paper` with limited to only 1000 users. These will calculate individual fingerprints and store them as a CSV in the `./results/` folder.

Each line in an individual fingerprint file is the list of attributes of the fingerprint, negative values are attributes that should not be set to the given user. (_Note_: for "historical" reasons, attributes are indexed from zero, and to preserve the sign, the zero index is stored as a float value.)

You can visualize properties of the fingerprints by using the following scripts. Script `04_lengths.py` plots the distribution of the length of the fingerprints (this is for the complete adult dataset):

![alt text](https://raw.githubusercontent.com/gaborgulyas/constrainted_fingerprinting/master/images/individual_lengths.png "Individual fingerprint lengths visualized.")

Next, you need to run `05_cache_anonsets.py`, which will calculate anonymity set sizes for each user, and will save  the result into a pickled file. This can be plotted with script `06_plot_anonsets.py`, which would give you something like this:

![alt text](https://raw.githubusercontent.com/gaborgulyas/constrainted_fingerprinting/master/images/individual_anonsetsizes.png "Individual fingerprint anonymity set sizes visualized.")

For the latter visualization, you need to get two more scripts:

* [`kmap.py`](https://raw.githubusercontent.com/gaborgulyas/kmap/master/kmap.py): this visualizes frequency of anonymity sets accordingly to their sizes. This is a useful visualization tool that helps understanding what is happening in your data, if you consider different attributes, apply anonymization or other countermeasures to decrease uniqueness.
* [`selectpoints.py`](https://raw.githubusercontent.com/gaborgulyas/SelectPoints/master/selectpoints.py): `kmap.py` uses this script to surround some points on the plot with a border.

### (3) Evaluation of general fingerprinting

The evaluation of general fingerprinting can be done similarly as before. The fingerprint generation is done with `07_group_fingerprinting.py`, which has a config file called `config_group.json`, where the output path and maximum fingerprint size (`max_sig_size`) can be set beside the other parameters. As `max_sig_size` suggests, this script calculates the group fingerprint for all `2 <= s <= max_sig_size`, saves the general fingerprint and the resulting equivalence classes into zipped pickle files.

When having the general fingerprint files ready, we can plot out the anonymity sets with `08_plot_anonsets.py`. This will result images like this:

![alt text](https://raw.githubusercontent.com/gaborgulyas/constrainted_fingerprinting/master/images/equivalence_classes_14.png "General fingerprint equvialence classes for `s=14` and only 1k users.")

<center>**General fingerprint equvialence classes for `s=14` and only 1k users**</center>


## Reference/attribution
If you find this work useful, especially if you use it whole or in part, please refer it to (similarly) as:

`[1] Gabor Gyorgy Gulyas, Gergely Acs, Claude Castelluccia: Near-Optimal Fingerprinting with Constraints. PET Symposium 2016.`

The paper is available here: [Near-Optimal Fingerprinting with Constraints](https://arxiv.org/abs/1605.08664)

Here is a short teaser:

> **Near-Optimal Fingerprinting with Constraints**
> 
> Several recent studies have demonstrated that people show large behavioural uniqueness. This has serious privacy implications as most individuals become increasingly re-identifiable in large datasets or can be tracked while they are browsing the web using only a couple of their attributes, called as their fingerprints. Often, the success of these  attacks depend on explicit constraints on the number of attributes learnable about individuals, i.e., the size of their fingerprints. These constraints can be budget as well as technical constraints imposed by the data holder. For instance, Apple restricts the number of applications that can be called by another application on iOS in order to mitigate the potential privacy threats of leaking the list of installed applications on a device. 
In this work, we address the problem of identifying the attributes (e.g., smartphone applications) that can serve as a fingerprint of users given constraints on the size of the fingerprint. We give the best fingerprinting algorithms in general, and evaluate their effectiveness on several real-world datasets. Our results show that current privacy guards limiting the number of attributes that can be queried about individuals is insufficient to mitigate their potential privacy risks in many practical cases.   
