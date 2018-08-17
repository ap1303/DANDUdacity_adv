#!/usr/bin/python

import pickle

from sklearn import grid_search
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data, test_classifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.pipeline import Pipeline

with open("final_project_dataset.pkl", "rb") as data_file:
    data_dict = pickle.load(data_file)

data_dict.pop('TOTAL', 0)

for person in data_dict:
    if data_dict[person]['from_poi_to_this_person'] != 'NaN' and data_dict[person]['to_messages'] != 'NaN':
        data_dict[person]['fraction_from_poi'] = int(data_dict[person]['from_poi_to_this_person']) / int(data_dict[person]['to_messages'])
    else: 
        data_dict[person]['fraction_from_poi'] = 0

    if data_dict[person]['from_this_person_to_poi'] != 'NaN' and data_dict[person]['from_messages'] != 'NaN':
        data_dict[person]['fraction_to_poi'] = int(data_dict[person]['from_this_person_to_poi']) / int(data_dict[person]['from_messages'])
    else: 
        data_dict[person]['fraction_to_poi'] = 0

features_list = ['poi', 'exercised_stock_options', 'fraction_to_poi', 'expenses', 'total_payments', 'shared_receipt_with_poi', 'bonus']

my_dataset = data_dict
data = featureFormat(my_dataset, features_list, sort_keys=True)
labels, features = targetFeatureSplit(data)

features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

"""
clf = GaussianNB()
#clf.fit(features_train, labels_train)
#pred = clf.predict(features_test)
#dump_classifier_and_data(clf, my_dataset, features_list)


clf = SVC(C=10)
clf.fit(features_train, labels_train)
pred = clf.predict(features_test)
dump_classifier_and_data(clf, my_dataset, features_list)
"""

parameters = {'min_samples_split': [2, 4, 6, 8, 10, 12, 14, 16, 18],
              'splitter': ('best','random'),
              'max_depth': [2, 4, 6, 8, 10, 12, 14, 16, 18]
             }
clf = DecisionTreeClassifier(min_samples_split=8, splitter='random', max_depth=10)
clf.fit(features_train, labels_train)
feature_importances = {}
importances = clf.feature_importances_
for i in range(len(importances)):
    feature_importances[features_list[i+1]] = importances[i]
print(feature_importances)
#clf = DecisionTreeClassifier()
#clf = grid_search.GridSearchCV(clf, parameters).fit(features_train, labels_train)
#print(clf.best_estimator_)

dump_classifier_and_data(clf, my_dataset, features_list)




