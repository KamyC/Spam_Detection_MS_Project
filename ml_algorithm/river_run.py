import pickle
# from river import metrics
# 1 = spam, 0 = non-spam

model =  ""

def is_spam(input_tweet,model_path):
    model = pickle.load(open(model_path, "rb"))
    return model.predict_one(input_tweet)

# input is raw tweet string, output is 1 or 0
# confirm and report to update model
def train_online(input_tweet, expected_output, username):
    path = "ml_algorithm/"+ username +".pickel"
    model = pickle.load(open(path,"rb"))
    print("updating model")
    print(expected_output)
    model.fit_one(input_tweet, expected_output)

    pickle.dump(model, open(path, 'wb'))
