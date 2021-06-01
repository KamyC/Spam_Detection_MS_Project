import tools.util
import ml_algorithm.river_run
import os.path
from shutil import copyfile
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator


def detect_spam (inputStr,username):
    original_model = 'ml_algorithm/model.pickel'
    model_path = "ml_algorithm/"+username+".pickel"
    if os.path.exists(model_path):
        res = ml_algorithm.river_run.is_spam(inputStr,model_path)
    else:
        print("create new pickle model")
        des_path = "ml_algorithm/"+username+".pickel"
        copyfile(original_model, des_path)
        res = ml_algorithm.river_run.is_spam(inputStr,username)
    # detect spam result
    print(res)
    if res == 0:
        # not spam
        return False
    else:
        return True

def detect_spam_for_public (inputStr):
    original_model = 'ml_algorithm/model.pickel'
    res = ml_algorithm.river_run.is_spam(inputStr, original_model)
    if res == 0:
        return False
    else:
        return True
    
# https://www.datacamp.com/community/tutorials/wordcloud-python
def visualize(susLabel,conLabel,username):
    csv_path = 'wordClouds/'+username+".csv"
    mask_path = 'wordClouds/blue.png'
    if conLabel == "con_spam":
        mask_path = 'wordClouds/orange.png'
    mask = pd.np.array(Image.open(mask_path))
    df = pd.read_csv(csv_path, encoding='ISO-8859-1')
    words = ''
    for msg in df[df['Type'] == susLabel]['Tweet']:
        msg = msg.lower()
        words += msg + ' '
    for msg in df[df['Type'] == conLabel]['Tweet']:
        msg = msg.lower()
        words += msg + ' '
    if len(words)==0:
        return False
    wordcloud = WordCloud(width=600, height=400,background_color="white",mask = mask).generate(words)

    image_colors = ImageColorGenerator(mask)
    plt.figure(figsize=[7, 7])
    plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis('off')
    plt.savefig("static/img/"+username+"_"+susLabel,bbox_inches='tight', pad_inches=0)
    plt.show()

def generate_wordCloud_csv(username):
    tools.util.select_to_csv(username)


