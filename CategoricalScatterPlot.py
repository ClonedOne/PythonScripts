import csv, sys, pprint
import random as rnd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from itertools import combinations
from matplotlib import cm



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


def acquire_stats (data_dict, categories):
    stat_dict = {}
    cat_list = categories.keys()
    for cat in cat_list:
        stat_dict[cat] = {}
    for cat in data_dict:
        if cat in cat_list:
            list_of_values = data_dict[cat]
            for value in list_of_values:
                if value in stat_dict[cat]:
                    stat_dict[cat][value] += 1
                else:
                    stat_dict[cat][value] = 1
    return stat_dict


def compute_points_dataframe (data_dict, categories, fuzzy=True):
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
            if fuzzy:
                points[category].append(categories[category].index(data_dict[category][i]) + rnd.uniform(-0.1, 0.1))
            else:
                points[category].append(categories[category].index(data_dict[category][i]))

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


def graph_points_bubble (df, cat1, cat2, categories):
    point_occurencies = count_point_occurrences(df, cat1, cat2)
    cmap = cm.get_cmap('winter')
    cat_length_1 = len(categories[cat1])
    cat_length_2 = len(categories[cat2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.xticks(np.arange(cat_length_1 + 1), categories[cat1], fontsize=14)
    plt.yticks(np.arange(cat_length_2 + 1), categories[cat2], fontsize=14)
    df.plot(cat1, cat2, kind='scatter', marker='o', ax=ax, s=point_occurencies, c=df[cat1], linewidth=0, cmap=cmap)
    for item in [ax.title, ax.xaxis.label, ax.yaxis.label]:
        item.set_fontsize(14)
    plt.show()



def graph_stats_bubble (stat_dict, categories):
    cmap = cm.get_cmap('brg')
    x = []
    lables_x = []
    y = []
    i = 0
    for cat in categories:
        x.append(i)
        lables_x.append(cat)
        i += 1
        if cat in stat_dict:
            y.append(stat_dict[cat])
        else:
            y.append(0)
    s = [30 * (elem**2) for elem in y]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.xticks(np.arange(len(lables_x)), lables_x, fontsize=14)
    for item in [ax.title, ax.xaxis.label, ax.yaxis.label]:
        item.set_fontsize(14)
    plt.scatter(x,y,s=s, c=s, cmap=cmap)
    plt.tight_layout()
    plt.show()



def count_point_occurrences (df, cat1, cat2):
    occurs = {}
    feature_1 = df[cat1]
    feature_2 = df[cat2]
    for i in range(len(feature_1)):
        point = feature_1[i], feature_2[i]
        if point in occurs:
            occurs[point] += 1
        else:
            occurs[point] = 1
    occurs_list = []
    for i in range(len(feature_1)):
        point = feature_1[i], feature_2[i]
        occurs_list.append((occurs[point]**2)*100)
    return occurs_list


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
    stat_dict = acquire_stats(data_dict, categories)
    df_not_fuzzy = compute_points_dataframe (data_dict, categories, fuzzy=False)
    if debug:
        print stat_dict
        print df
        print df_not_fuzzy

    '''
    for key in stat_dict.keys():
        graph_stats_bubble(stat_dict[key], categories[key])
    '''

    '''
    for comb in combinations(categories.keys(), 2):
        if len(label_list) > 0:
            graph_single_point(df, comb[0], comb[1], categories, label_list)
        else:
            graph_single_point(df, comb[0], comb[1], categories)
    '''


    for comb in combinations(categories.keys(), 2):
        graph_points_bubble(df_not_fuzzy, comb[0], comb[1], categories)






if __name__ == '__main__':
    main()
