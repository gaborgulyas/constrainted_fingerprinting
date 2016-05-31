#!/usr/bin/python
#from tables import *
import cPickle as pickle
import sys
from operator import itemgetter
import gzip
import os
from ProgressBar import *
from collections import Counter
from common import *

#===============================================================================
if __name__ == "__main__":
    config, outpath = load_config("config_group.json")

    # Max sig. length
    K = config["max_sig_size"]
    OUTPUT_DATA_DIR = config["output_path"]

    print "Max signature size:", K

    itemUser = load_attr_csv(config["user_limit"], first_col = config["first_col"], data_prefix = config["data_pref"])
    userItem = load_user_csv(config["user_limit"], first_col = config["first_col"], data_prefix = config["data_pref"])

    i_t = []
    for k in sorted(itemUser.keys()): 
        i_t.append(set(itemUser[k]))
    itemUser = i_t

    i_t = []
    for k in sorted(userItem.keys()): 
        i_t.append(set(userItem[k]))
    userItem = i_t

    # For test:
    # itemUser = itemUser[:1000]

    user_num = len(userItem)
    item_num = len(itemUser)

    K = min(K, item_num)

    print "Users:", user_num
    print "Items:", item_num
    print "K:", K

    scores = map(lambda x: -abs(user_num/2 - len(x)), itemUser) 

    best_item = max(enumerate(scores), key=itemgetter(1))[0]

    class1 = set(itemUser[best_item])

    e_classes = [class1, set(range(user_num)) - class1]

    signature = [best_item]
    sig_set = set(signature)

    while len(signature) < K and len(e_classes) < user_num:
        # separation metric: number of pairs that the item separates
        sep_metric = Counter()

        pbar = MyProgressBar('Searching for best separator (sig.len: %d)' % (len(signature) + 1), len(e_classes))
        for i, e_class in enumerate(e_classes):
            if len(e_class) == 1:
                continue

            items = set()
            for user in e_class:
                items |= userItem[user] 

            for item in items:
                if item in sig_set:
                    continue

                occurence = reduce(lambda x,y: x + (item in userItem[y]), e_class, 0)

                sep_metric[item] += occurence * (len(e_class) - occurence)

            pbar.update(i)

        (best_item, best_metric) = sep_metric.most_common(1)[0]

        if best_metric == 0:
            print "No further separation is possible. Terminating!"
            break

        new_classes = []

        # Division into subpartitions
        for e_class in e_classes:
            user_set = set(itemUser[best_item])

            new_set1 = e_class - user_set
            new_set2 = e_class - new_set1

            if len(new_set1) > 0 and len(new_set2) > 0:
                new_classes.extend([new_set1, new_set2]) 
            else:
                new_classes.append(e_class)

        e_classes = new_classes
        signature.append(best_item)
        sig_set.add(best_item)
        pbar.finish()

        pickle.dump([signature, e_classes],
                gzip.open(OUTPUT_DATA_DIR + "equivalence_classes_%d.p.gz" % len(signature), 'w'))

        print "Best separation metric:", best_metric
        print "Group fingerprint:", signature

        print "Equivalence classes (partitions):", len(e_classes), " (max: %d)" % user_num




