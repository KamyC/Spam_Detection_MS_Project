# from creme import compose
# from creme import feature_extraction
# from creme import naive_bayes
# from river import metrics
#
# from sklearn.model_selection import train_test_split
#
# import numpy as np
# import pandas as pd
# import pickle
#
# '''
# NOTE!
# You only need to run this file once
# '''
#
# # load training data from csv
# df = pd.read_csv('utkmls2/train.csv', encoding='ISO-8859-1')
#
# # set Y result label
# df['b_labels'] = df['Type'].map({'Quality': 0, 'Spam': 1})
# Y = df['b_labels'].values
# df_train, df_test, Ytrain, Ytest = train_test_split(df['Tweet'], Y, test_size=0.33)
#
# # initialize river model
# model = compose.Pipeline(
#     ('tokenize', feature_extraction.BagOfWords()),
#     ('nb', naive_bayes.MultinomialNB(alpha=1))
# )
#
# for tweet, label in zip(df_train, Ytrain):
#     model = model.fit_one(tweet, label)
#
# pickle.dump(model, open("model.pickel", "wb"))
#
# model = pickle.load(open("model.pickel", "rb"))
#
# # test accuracy metric
# metric = metrics.Accuracy()
# for tweet, label in zip(df_test, Ytest):
#     label_pred = model.predict_one(tweet)
#     metric = metric.update(label, label_pred)
#
# print(metric)
# print("Training completes")