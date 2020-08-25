import tweepy,re
from textblob import TextBlob
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd


st.text('@author: koshal ')
html = """
<div style='background-color:tomato;padding:10px'>
<h2 style='color:white;text-align:center;'><b>VISUALIZING TWEETS SENTIMENTS</b> </h2>
</div>
"""
st.markdown(html, unsafe_allow_html=True)
st.subheader('    ')    
        
def cleanTweet(tweet): 
         return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

def percentage(part, whole):
            temp = 100 * float(part) / float(whole)         
            return format(temp, '.2f')

tweets = []
tweetText = []
sent = []

# authenticating
consumerKey ='XXXXXXXXXXXXXXXXX'   
consumerSecret ='XXXXXXXXXXXXXXXXXXXXXXXXX'  
accessToken ='XXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
accessTokenSecret ='XXXXXXXXXXXXXXXXXXXXXXX'

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

st.markdown("""<h4 style='color:green;'><i>Enter Keyword/Tag to search about</i></h4>""", unsafe_allow_html=True)
searchTerm = st.text_input('', 'economy')     

st.markdown("""<h4 style='color:green;'><i>Enter Number Of Tweets to be Analyzed</i></h4>""", unsafe_allow_html=True)
NoOfTerms = st.number_input('', min_value=30, max_value=1000)       

# searching for tweets
tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)

# creating some variables to store info
polarity = 0
positive = 0
wpositive = 0
spositive = 0
negative = 0
wnegative = 0
snegative = 0
neutral = 0

for tweet in tweets:
    
    tweetText.append(cleanTweet(tweet.text).encode('utf-8'))
    analysis = TextBlob(tweet.text)
    sent.append(analysis.sentiment)             # print tweet's polarity
    polarity += analysis.sentiment.polarity     # adding up polarities to find the average later

    if (analysis.sentiment.polarity == 0.00):   # adding reaction of how people are reacting to find average later
        neutral += 1
    elif (analysis.sentiment.polarity > 0.00 and analysis.sentiment.polarity <= 0.30):
        wpositive += 1
    elif (analysis.sentiment.polarity > 0.30 and analysis.sentiment.polarity <= 0.60):
        positive += 1
    elif (analysis.sentiment.polarity > 0.60 and analysis.sentiment.polarity <= 1.00):
        spositive += 1
    elif (analysis.sentiment.polarity > -0.30 and analysis.sentiment.polarity <= 0.00):
        wnegative += 1
    elif (analysis.sentiment.polarity > -0.60 and analysis.sentiment.polarity <= -0.30):
       negative += 1
    elif (analysis.sentiment.polarity > -1.00 and analysis.sentiment.polarity <= -0.60):
        snegative += 1

# finding average of how people are reacting
positive = percentage(positive, NoOfTerms)
wpositive = percentage(wpositive, NoOfTerms)
spositive = percentage(spositive, NoOfTerms)
negative = percentage(negative, NoOfTerms)
wnegative = percentage(wnegative, NoOfTerms)
snegative = percentage(snegative, NoOfTerms)
neutral = percentage(neutral, NoOfTerms)

# finding average reaction
polarity = polarity / NoOfTerms
  
labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
          'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
colors = ['yellow','#7CFC00','#FF4500','#4d75f3','#FF8C00','#DD7F50','#2CBD35']
explode=[0.05,0.05,0.05,0.05,0.05,0.05,0.05]
col=[positive, wpositive, spositive, neutral,negative, wnegative, snegative]
plt.figure(figsize=(10,7))

st.subheader(' ')
button = st.button('Visualize Sentiments')

if button:
    st.subheader('  ')
    st.subheader('    ')
    plt.pie(col,colors=colors,labels=labels,explode=explode,labeldistance=1.0,autopct='%1.1f%%',pctdistance=0.9,shadow=True,radius=1.1,startangle=0)
    plt.suptitle('How people are reacting on ' + searchTerm + ' by analyzing ' + str(NoOfTerms) + ' Tweets.', color='green', size=20, y=1.0)
    plt.axis('equal')
    st.pyplot()
    
def data():
    
    df = pd.concat([pd.DataFrame(tweetText, columns=['Tweets']), pd.DataFrame(sent)['polarity']], axis=1)
    return df
st.markdown("""<h4 style='color:green;'><i>Want's to Display each Tweet and its Polarity ??</i></h4>""", unsafe_allow_html=True)
st.subheader('   ')
but1 = st.button('Display')
if but1:
   st.table(data())


