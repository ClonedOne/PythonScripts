import csv, sys, pprint
import random as rnd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.ticker import *
from itertools import combinations
from matplotlib import cm
from matplotlib import colors


def acquire_data (file_name):
    data_dict = {}
    with open(file_name) as csvfile:
        reader = csv.DictReader(csvfile)
        for field in reader.fieldnames:
            data_dict[field] = []
        for row in reader:
            for field in reader.fieldnames:
                data_dict[field].append(row[field])
    return data_dict


def acquire_categories (file_name):
    categories = {}
    with open(file_name) as csvfile:
        reader = csv.DictReader(csvfile)
        for field in reader.fieldnames:
            categories[field] = []
        for row in reader:
            for field in reader.fieldnames:
                categories[field].append(row[field])
    return categories


def acquire_labels (file_name):
    label_list = []
    with open(file_name) as label_file:
        for line in label_file:
            label_list.append(line.strip())
    return label_list


def compute_points_dataframe (data_dict, categories):
    points = {}
    cat_list = categories.keys()
    for category in cat_list:
        points[category] = []
    data_headers = data_dict.keys()
    for header in data_headers:
        if header not in cat_list:
            identifier = header
    number_of_points = len(data_dict[data_headers[0]])
    for i in range(number_of_points):
        for category in cat_list:
            points[category].append(categories[category].index(data_dict[category][i]) + rnd.uniform(-0.1, 0.1))

    d = {}
    for category in cat_list:
        d[category] = pd.Series(points[category], index=data_dict[identifier])
    df = pd.DataFrame(d)
    return df


def graph_single_point (df, cat1, cat2, categories, label_list=None):
    cmap = cm.get_cmap('winter')
    cat_length_1 = len(categories[cat1])
    cat_length_2 = len(categories[cat2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    df.plot(cat1, cat2, kind='scatter', marker='o' , ax=ax, s=65, c=df[cat1] , linewidth=0, cmap=cmap)
    plt.xticks(np.arange(cat_length_1 + 1), categories[cat1], fontsize=14)
    plt.yticks(np.arange(cat_length_2 + 1), categories[cat2], fontsize=14)
    for item in [ax.title, ax.xaxis.label, ax.yaxis.label]:
        item.set_fontsize(14)
    if label_list != None:
        for k, v in df.iterrows():
            if k in label_list:
                ax.annotate(k, (v[cat1], v[cat2]), xytext=(rnd.randint(-50, 50), rnd.randint(-60, 60)), textcoords='offset points',
                        family='sans-serif', fontsize=16,  ha = 'center', va = 'bottom', color='darkslategrey',
                        arrowprops = dict(arrowstyle = '-|>', connectionstyle = 'arc3,rad=0'))

    #plt.tight_layout()
    plt.show()


def main ():
    debug = True
    if len(sys.argv) < 3:
        print "Please provide a valid file path for the data file and the category file [optional label file path]"
        return

    label_list = []
    data_dict = acquire_data(sys.argv[1])
    categories = acquire_categories(sys.argv[2])
    if len(sys.argv) == 4:
        label_list = acquire_labels(sys.argv[3]);

    if debug:
        pprint.pprint (data_dict)
        for key in data_dict:
            print len(data_dict[key])
        pprint.pprint (categories)
        for key in categories:
            print len(categories[key])

    df = compute_points_dataframe (data_dict, categories)
    if debug:
        print df
    for comb in combinations(categories.keys(), 2):
        if len(label_list) > 0:
            graph_single_point(df, comb[0], comb[1], categories, label_list)
        else:
            graph_single_point(df, comb[0], comb[1], categories)

if __name__ == '__main__':
    main()
