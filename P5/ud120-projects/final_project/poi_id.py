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

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi','salary', 'total_payments', 'bonus', 'loan_advances', 'total_stock_value', 'from_poi_to_this_person', 'from_this_person_to_poi', 'shared_receipt_with_poi']

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "rb") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
"""
count = 0
while count < len(features_list):
    for name in data_dict:
        if data_dict[name][features_list[count]] == 'NaN':
            del data_dict[name]
"""

### Task 3: Create new feature(s)
for person in data_dict:
    if data_dict[person]['bonus'] != 'NaN':
        data_dict[person]['total_income'] = int(data_dict[person]['salary']) + int(data_dict[person]['bonus'])
    else:
        if data_dict[person]['salary'] != 'NaN':
             data_dict[person]['total_income'] = int(data_dict[person]['salary'])


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
parameters = {'min_samples_split': [x for x in range(2, 100)],
              'splitter': ('best','random'),
              'max_depth': [None, 2, 4, 6, 8, 10, 15, 20, 25]
              }
clf = DecisionTreeClassifier()
clf = grid_search.GridSearchCV(clf, parameters).fit(features, labels)
clf.fit(features_train, labels_train)
print(clf.best_estimator_)
#print(clf.feature_importances_)
dump_classifier_and_data(clf, my_dataset, features_list)




