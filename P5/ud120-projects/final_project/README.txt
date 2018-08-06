1. The goal of this project is to try to predict, using the given features, whether a person is a POI or not. The learning process is achieved by
   using machine learning algorithms. The dataset contains email and financial data about every person documented and is of length 146. In terms of outliers,
   I didn't find any that's worthy of being removed in that the numerical data are all about income or payments and if the number is very large, that's because
   the employee did earn that amount of income or did pay that amount of money. So there is absolutely no need to remove them.

2. I manually selected the features ['poi','salary', 'total_payments', 'bonus', 'loan_advances', 'total_stock_value', 'from_poi_to_this_person', 'from_this_person_to_poi', 'shared_receipt_with_poi']. After achieving
   above 0.3 precision and recall, I took a look at the feature importances and removed

3. I tried the GaussianNB, SVM, and DecisionTree. GaussianNB has below 0.3 precision and recall, SVM reports an 'divide by zero' error, so
   I chose DecisionTree as the final algorithm.

4. To tune the parameters of an algorithm means to pick the parameter combination in the given set of combinations that has the best performance.
   If this step is not done well, the best effort is not achieved. I used GridSearchCV to tune min_samples_split, splitter, max_depth and found the
   optimal combination to be