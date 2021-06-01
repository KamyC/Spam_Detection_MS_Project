import ml_algorithm.river_run
from flask import Flask, request, jsonify, render_template, json, session,redirect, url_for
from ml_algorithm import algorithm
import tools.util
import tools.database
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

class labelContainer:
    def __init__(self,label):
        self.label = label
    def is_spam(self):
        self.label = "spam"
    def is_benign(self):
        self.label = "benign"
    def reverse(self):
        if self.label == "spam":
            self.label = "benign"
        elif self.label == "benign":
            self.label = "spam"

label_container = labelContainer("neutral")

class tweetContainer:
    def __init__(self, content):
        self.content = content
    def updateContent(self,content):
        self.content = content

tweet_container = tweetContainer("nothing")

@app.route('/')
def home():
    username = session.get('username')
    if username:
        return render_template('index.html', userName="Welcome " + username)
    else:
        return render_template('index.html', signIn="Sign in", singUp="Sign up")

@app.route('/exit')
def logOut():
    print("remove user name")
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/detect',methods=['POST'])
def detect():
    confScore = 100
    username = session.get('username')
    str_input = request.form.get('content')
    tweet_container.updateContent(str_input)
    time = tools.util.get_date()
    label = "sus_benign"
    if 'detect' in request.form:
        if username:
            res = algorithm.detect_spam(str_input, username)
            if res:
                label = "sus_spam"
                label_container.is_spam()
                tools.database.init_tweet_table(username)
                tools.database.insert_into_sql(username, str_input, label, time, confScore)
                return render_template('index.html', isSpam='Spam Warning!!!',
                                       userName="Welcome " + username, res=res)
            else:
                label_container.is_benign()
                tools.database.init_tweet_table(username)
                tools.database.insert_into_sql(username, str_input, label, time, confScore)
                return render_template('index.html',
                                       notSpam='Safe! Not A Spam!',
                                       userName="Welcome " + username, res=res)
        else:
            res = algorithm.detect_spam_for_public(str_input)
            print("no user name")
            if res:
                label = "sus_spam"
                tools.database.write_to_public(str_input, label, time, confScore)
                return render_template('index.html', isSpam='Spam Warning!!!',
                                       res=res)
            else:
                return render_template('index.html',
                                       notSpam='Safe! Not A Spam!' , res=res)
    elif 'report' in request.form:
        if username:
            label_container.is_spam()
            tools.database.init_tweet_table(username)
            tools.database.insert_into_sql(username, str_input, "con_spam", time, confScore)
        else:
            tools.database.write_to_public(str_input, "con_spam", time, confScore)
        return render_template('index.html', getReport='Report Received! Thank you!', userName="Welcome " + username)

@app.route('/deny_tweet',methods=['POST'])
def denyTweet():
    username = session.get('username')
    tools.util.deny_tweet_sql(username)
    #update model
    content = tweet_container.content
    label_container.reverse()
    label = label_container.label
    num_label = 0
    if label == "spam":
        num_label = 1
    ml_algorithm.river_run.train_online(content, num_label, username)
    return "Deny Works"

@app.route('/confirm_tweet',methods=['POST'])
def confirmTweet():
    username = session.get('username')
    tools.util.confirm_tweet_sql(username)
    #update model
    content = tweet_container.content
    label = label_container.label
    num_label = 0
    if label == "spam":
        num_label = 1
    ml_algorithm.river_run.train_online(content,num_label,username)
    return "Confirm Works"

@app.route('/help_tweet',methods=['POST'])
def helpTweet():
    username = session.get('username')
    print(tools.util.send_help_database_admin(username))
    return "Help Works"


@app.route('/update_db',methods=['POST'])
def updateDB():
    username = session.get('username')
    tools.util.updateDB(username)
    return "Help Works"

# nav jump
@app.route('/why_page')
def toWhyPage():
    username = session.get('username')
    if username:
        return render_template('why_page.html', userName = "Welcome " + username)
    else:
        return render_template('why_page.html', signIn = "Sign in", singUp = "Sign up")

@app.route('/service_page')
def toServicePage():
    username = session.get('username')
    if username:
        return render_template('service_page.html', userName="Welcome " + username)
    else:
        return render_template('service_page.html', signIn="Sign in", singUp="Sign up")

@app.route('/support_page')
def toSupportPage():
    username = session.get('username')
    if username:
        return render_template('support_page.html', userName="Welcome " + username)
    else:
        return render_template('support_page.html', signIn="Sign in", singUp="Sign up")

@app.route('/dash_board')
def toDashBoard():
    username = session.get('username')
    data = tools.util.find_user_information_database(username)
    tweets = tools.util.get_past_ten_database(username) #label date content
    if username:
        return render_template('dash_board.html', userName="Welcome " + username, total_number = data["total_num"], data = data, tweets = tweets)
    else:
        return redirect(url_for('toSignIn'))

@app.route('/get_date_frame',methods=['POST'])
def getDateFrameResponse():
    username = session.get('username')
    startDate = request.form.get("startDate")
    endDate = request.form.get("endDate")
    print(startDate)
    print(endDate)

    # get spam between number
    spam_cnt = tools.util.get_spam_cnt_between(username,startDate,endDate)
    # get benign between number
    benign_cnt = tools.util.get_benign_cnt_between(username,startDate,endDate)
    # get tweets in between
    tweets = tools.util.get_tweets_between(username,startDate,endDate)  #Label,Date,Content
    data = {
        "spam_cnt": spam_cnt,
        "benign_cnt": benign_cnt,
        "tweets" :tweets
    }
    return jsonify(data)

@app.route('/dash_history')
def toHistory():
    username = session.get('username')
    tweets = tools.util.get_past_fiften_database(username) #date content label
    if username:
        return render_template('dash_history.html', userName="Welcome " + username, tweets = tweets)
    else:
        return redirect(url_for('toSignIn'))

@app.route('/dash_history_checkbox',methods=['POST'])
def getCheckBoxRespoinse():
    tID = request.form.get("tID")
    label = request.form.get("label")
    username = session.get('username')
    print(username+": "+tID+": "+label)
    tools.util.checkbox_label_database(username,tID,label)
    return "SUCCESS"

class pageContainer:
    def __init__(self,covers):
        self.covers = covers
    def toNext(self,username):
        res = int(self.covers)
        totalCnt = tools.util.get_total_num(username)
        if res+15 < totalCnt:
            self.covers = str(int(self.covers)+15)
    def toPrev(self):
        res = int(self.covers) - 15
        if res<0:
            self.covers = "0"
        else:
            self.covers = str(res)

p = pageContainer("0")

@app.route('/get_next_fifteen_tweets')
def getNextFifteenTweets():
    username = session.get('username')
    p.toNext(username)
    tweets = tools.util.get_fiften_frame(username,p.covers) #id date content label
    print(tweets)
    if username:
        return render_template('dash_history.html', userName="Welcome " + username, tweets=tweets)
    else:
        return redirect(url_for('toSignIn'))

@app.route('/get_prev_fifteen_tweets')
def getPrevFifteenTweets():
    p.toPrev()
    username = session.get('username')
    tweets = tools.util.get_fiften_frame(username,p.covers)
    if username:
        return render_template('dash_history.html', userName="Welcome " + username, tweets=tweets)
    else:
        return redirect(url_for('toSignIn'))

@app.route('/dash_visualization')
def toVisualization():
    username = session.get('username')
    spam_path = username+"_sus_spam.png"
    benign_path = username+ "_sus_benign.png"
    algorithm.generate_wordCloud_csv(username)
    algorithm.visualize("sus_spam", "con_spam", username)
    algorithm.visualize("sus_benign", "con_benign", username)
    #pass the path var
    if username:
        return render_template('dash_visualization.html', userName="Welcome " + username, spamWordCloud = spam_path, benignWordCloud = benign_path)
    else:
        return redirect(url_for('toSignIn'))

@app.route('/sign_in')
def toSignIn():
    return render_template('sign_in.html')

@app.route('/sign_up')
def toSignUp():
    return render_template('sign_up.html')

#check username
@app.route('/check_username',methods=['POST'] )
def checkUsername():
    username = request.form.get("username")
    users = tools.database.check_username(username)
    if users == 0:
        return "valid"
    else:
        return "invalid"

#check email
@app.route('/check_email',methods=['POST'] )
def checkEmail():
    username = request.form.get("email")
    users = tools.database.check_email(username)
    if users == 0:
        return "valid"
    else:
        return "invalid"

# sign up
@app.route('/sign_in',methods=['POST'] )
def hasSignedUp():
    # get form data
    userName = request.form.get('userName')
    emailInput = request.form.get('emailInput')
    pswInput = request.form.get('pswInput')
    pswConfirm = request.form.get('pswConfirm')
    print(userName, emailInput, pswInput,pswConfirm)
    if pswConfirm == pswInput:
        user_info_list = [userName,emailInput,pswInput]
        tools.database.write_user_to_database(user_info_list)
        # jump to sign in page
        return render_template('sign_in.html', allow ="Thank you for signing up. You can log in now")

# sign in
@app.route('/home',methods=['POST'] )
def hasSignedIn():
    emailInput = request.form.get('emailInput')
    pswInput = request.form.get('pswInput')
    userInfo = tools.database.find_user_in_database(emailInput, pswInput)
    if userInfo is None:
        return render_template('sign_in.html', warning ="User Not Found!" )
    session['username'] = userInfo[1]
    session.permanent = True
    return render_template('index.html', userName = "Welcome " +userInfo[1])

# extension sign in---------------------------------------------------
@app.route('/extension_sign',methods=['POST'])
def extensionSign():
    emailInput = request.form.get('emailInput')
    pswInput = request.form.get('pswInput')
    print(emailInput, pswInput)
    userInfo = tools.database.find_user_in_database(emailInput,pswInput)
    print(userInfo)
    if len(userInfo[1]) == 0:
        return {"result":False}
    else:
        return {"result":userInfo[1]}

# report spam using post
@app.route('/detect_api/post_report',methods=['POST'])
def api_post_report():
    data = request.data.decode('utf-8')
    print(data)
    data_json = json.loads(data)
    username = data_json.get('user')
    str_input = data_json['tweet']
    time = tools.util.get_date()
    label = "con_spam"
    # if we can get user
    if username:
        tools.database.insert_into_sql(username,str_input,label,time,100)
    #or
    else:
        tools.database.insert_into_public(str_input,label,time,100)
    return jsonify(data_json)

# detect spam using post
@app.route('/detect_api/post_detect',methods=['POST'])
def api_post_detect():
    data = request.data.decode('utf-8')
    print(data)
    data_json = json.loads(data)
    username = data_json.get('user')
    str_input = data_json['tweet']
    time = tools.util.get_date()
    label = "sus_benign"
    if algorithm.detect_spam(str_input,username):
        result ="This is a spam!!!"
        # print(result)
        label = "sus_spam"
    else:
        result = "Safe! Not a spam"
        # print(result)
    # if we can get user
    if username:
        tools.database.insert_into_sql(username,str_input,label,time,100)
    # or
    else:
        tools.database.insert_into_public(str_input,label,time,100)
    return {'result': result}

# ----------------------------API
# http://127.0.0.1:5000/api/detect/public?tweets=this is a test for APIs
@app.route('/api/detect/public')
def api_detect_public():
    tweets = request.args.get('tweets')
    res = algorithm.detect_spam_for_public(tweets)
    label = "benign"
    if res:
        label = "spam"
    data = {
        "tweets": tweets,
        "label": label
    }
    return jsonify(data)

# http://127.0.0.1:5000/api/detect/user?email=123@hotmail.com&psw=123&tweets=hello world
@app.route('/api/detect/user')
def api_detect_user():
    email = request.args.get('email')
    psw = request.args.get('psw')
    tweets = request.args.get('tweets')
    userInfo = tools.database.find_user_in_database(email, psw)
    find_user = True
    label = "sus_benign"
    if len(userInfo[1]) == 0:
       find_user = False
    if find_user:
        res = algorithm.detect_spam(tweets,userInfo[1])
        if res:
            label = "sus_spam"
    data = {
        "user": userInfo[1],
        "tweets": tweets,
        "label": label
    }
    time = tools.util.get_date()
    tools.database.insert_into_sql(userInfo[1], tweets, label, time, 100)
    return jsonify(data)

# http://127.0.0.1:5000/api/report/user?email=123@hotmail.com&psw=123&tweets=hello%20world
@app.route('/api/report/user')
def api_report_user():
    email = request.args.get('email')
    psw = request.args.get('psw')
    tweets = request.args.get('tweets')
    userInfo = tools.database.find_user_in_database(email, psw)
    find_user = True
    label = "con_spam"
    if len(userInfo[1]) == 0:
        find_user = False
    if find_user:
        data = {
            "user": userInfo[1],
            "tweets": tweets,
            "label": label
        }
    time = tools.util.get_date()
    tools.database.insert_into_sql(userInfo[1], tweets, label, time, 100)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
