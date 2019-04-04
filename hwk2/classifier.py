from sklearn.datasets import load_iris
from sklearn import tree
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
from pandas import datetime
from sklearn.datasets import load_iris
import graphviz
import os
os.environ["PATH"]+=os.pathsep+'C:/Program Files (x86)/Graphviz2.38/bin'

def main():
    ufo_df = pd.read_csv("national_ufo_reports.csv")
    ufo_df['date_time'] = pd.to_datetime(ufo_df['date_time'])
    ufo_df['posted'] = pd.to_datetime(ufo_df['posted'])

    ufo_df['hour'] = [d.hour for d in ufo_df['date_time']]
    
    # get training set from pandas
    pdtraining = ufo_df.loc[ufo_df.loc[:,'month']<7]
    # get test set from pandas
    pdtest = ufo_df.loc[ufo_df.loc[:,'month']>=7]
    # create the matrices
    mtraining = []
    mtraining_labels = []
    mtest = []
    mtest_labels = []
    for index, row in pdtraining.iterrows():
        
        region = map_state(row['state'])
        if not region == -1:
            time = map_time(row['hour'])
            mtraining.append([region, time])

            mtraining_labels.append(map_shape(row['shape']))
    
    for index, row in pdtest.iterrows():
        region = map_state(row['state'])
        if not region == -1:
            time = map_time(row['hour'])
            mtest.append([region, time])

            mtest_labels.append(map_shape(row['shape']))
    
    # tree time
    # default criterion is gini impurity, so we don't need to change anything
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(mtraining, mtraining_labels)
    predictions = clf.predict(mtest)
    # actual = mtest_labels

    acc_mx = [[0, 0], [0, 0]]
    # calculate accuracy:
    for i in range(0, len(predictions)):
        p = predictions[i]
        a = mtest_labels[i]
        acc_mx[p][a]+=1
    
    fp = acc_mx[0][1]
    fn = acc_mx[1][0]
    tp = acc_mx[1][1]
    tn = acc_mx[0][0]

    print("False Positives: " + str(fp))
    print("False Negatives: " + str(fn))
    print("True Positives: " + str(tp))
    print("True Negatives: " + str(tn))

    print("Accuracy: " + str(accuracy_score(mtest_labels, predictions)))

    # graphviz tree
    feature_names = ['US Region', 'Time of Day']
    target_names = ['Circle', 'Triangle']
    dot_data = tree.export_graphviz(clf, 
        out_file=None, 
        feature_names=feature_names,
        class_names=target_names)
    graph = graphviz.Source(dot_data)
    graph.render('dec_tree')
    # Note that the output pdf will have numbers and not nice labels
    # see below (line 94-96) for specific info on these
    


# date_time year month city state shape posted
# we want:
# Region of the country: 
# Time of day: Night (0000-0559) Morning(0600-1159) 
#              Afternoon(1200-1759) Evening(1800-2359)

# Training is between Jan1 and June 30
# Test is between July 1 and and Aug 31

# 0 is circle, 1 is triangle
# 0 is night, 1 is morning, 2 is afternoon, 3 is evening
# 0 is northeast, 1 is midwest, 2 is south, 3 is west

# Map the data

def map_state(abbrev):
    northeast = 0
    midwest = 1
    south = 2
    west = 3
    switch = {
        'ME':northeast,
        'VT':northeast,
        'NH':northeast,
        'MA':northeast,
        'CT':northeast,
        'RI':northeast,
        'NY':northeast,
        'PA':northeast,
        'NJ':northeast,
        'ND':midwest,
        'SD':midwest,
        'NE':midwest,
        'KS':midwest,
        'MO':midwest,
        'IA':midwest,
        'MN':midwest,
        'WI':midwest,
        'IL':midwest,
        'IN':midwest,
        'OH':midwest,
        'MI':midwest,
        'MD':south,
        'DE':south,
        'WV':south,
        'VA':south,
        'KY':south,
        'NC':south,
        'TN':south,
        'MS':south,
        'AL':south,
        'GA':south,
        'SC':south,
        'FL':south,
        'LA':south,
        'TX':south,
        'OK':south,
        'AR':south,
        'WA':west,
        'OR':west,
        'CA':west,
        'NV':west,
        'AZ':west,
        'NM':west,
        'CO':west,
        'UT':west,
        'WY':west,
        'ID':west,
        'MT':west,
        'AK':west,
        'HI':west,
    }
    return switch.get(abbrev,-1)

def map_shape(shape):
    switch = {
        "Circle":0,
        "Triangle":1,
    }
    return switch.get(shape,-1)

def rev_map_shape(num):
    switch = {
        0:"Circle",
        1:"Triangle",
    }
    return switch.get(num,-1)

def map_time(time_h):
    if time_h < 6:
        return 0
    elif time_h < 12:
        return 1
    elif time_h < 18:
        return 2
    elif time_h < 24:
        return 3
    else:
        return -1

if __name__=="__main__":
    main()