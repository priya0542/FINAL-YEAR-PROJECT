from tkinter import *
import tkinter as tk
from tkinter import simpledialog
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import naive_bayes, svm
from sklearn.metrics import classification_report,accuracy_score
from PIL import ImageTk, Image
import re
from sklearn.feature_extraction.text import TfidfTransformer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

root = Tk()

#taking input from user
my_w = tk.Tk()

"""
#new addings

my_w.geometry("400x200")
my_w.configure(bg = 'pink')

#new addings
"""


my_w = simpledialog.askstring("input","enter an input", parent = my_w)


#Importing data set
data=pd.read_csv(r'C:\Users\HP\OneDrive\Desktop\MY FOLDER\FINAL YEAR PROJECT\test-sample_dataset.csv')
#remove repeated(duplicates) tweets
data.drop_duplicates(inplace = True)
print(data.head(5))
print(data.shape)
#drop table
data_1=data.drop(['annotation'], axis = 1)

#Corpus bag of words
corpus = []
for i in range (0,len(data)):  
    review = re.sub('[A-Z^a-z]',' ',data['content'][i]) 
    review = review.lower() 
    review = review.split() 
    review = ' '.join(review) 
    corpus.append(review)
 
#corpus
bow_transformer = CountVectorizer() 
bow_transformer = bow_transformer.fit(corpus)
print(len(bow_transformer.vocabulary_)) 
messages_bow = bow_transformer.transform(corpus) 
print(messages_bow.shape)
tfidf_transformer = TfidfTransformer().fit(messages_bow)

#sentiment analysis
analyzer = SentimentIntensityAnalyzer()
data_1['compound'] = [analyzer.polarity_scores(x)['compound'] for x in data_1['content']]
data_1['neg'] = [analyzer.polarity_scores(x)['neg'] for x in data_1['content']]
data_1['neu'] = [analyzer.polarity_scores(x)['neu'] for x in data_1['content']]
data_1['pos'] = [analyzer.polarity_scores(x)['pos'] for x in data_1['content']]

#Labelling
data_1['comp_score'] = data_1['compound'].apply(lambda c: 0 if c >=0 else 1)

#Splitting dataset into Train and Test set 
X_train, X_test, y_train, y_test = train_test_split(data_1['content'],data_1['comp_score'], 
random_state=40)

print('Number of rows in the total set: {}'.format(data.shape[0]))
print('Number of rows in the training set: {}'.format(X_train.shape[0]))
print('Number of rows in the test set: {}'.format(X_test.shape[0]))

#CountVectorizer method
vector = CountVectorizer(stop_words = 'english', lowercase = True)
#Fitting the training data 
training_data = vector.fit_transform(X_train)
#Transform testing data 
testing_data = vector.transform(X_test)


#Classification
#Naive Bayes
print()
print("----------------------")
print("Naive Bayes")
Naive = naive_bayes.MultinomialNB()
Naive.fit(training_data, y_train)
nb_pred = Naive.predict(testing_data)

#Analysis Report
print()
print("------Classification Report------")
print(classification_report(nb_pred,y_test))
print("------Accuracy------")
print(f"The Accuracy Score :{round(accuracy_score(nb_pred,y_test)*100)}")
print()
nb=round(accuracy_score(nb_pred,y_test)*100)

#Support vector Machine
print()
print("----------------------")
print()
print("Support vector Machine")
sv = svm.SVC(kernel='linear') # Linear Kernel
sv.fit(training_data, y_train)
sv_pred = sv.predict(testing_data)

#Analysis Report
print()
print("------Classification Report------")
print(classification_report(sv_pred,y_test))
print()
print("------Accuracy------")
print(f"The Accuracy Score :{round(accuracy_score(sv_pred,y_test)*100)}")
svm=round(accuracy_score(sv_pred,y_test)*100)


#data processing against the algorithms
def prediction():
    pred=vector.transform([my_w])
    svp=sv.predict(pred)
    nbp=Naive.predict(pred)
    print("Result for the user given input : ")
    print (svp,nbp)
    print()
    print("----------------------")
    print()
    print()
    
#Data Visualization

def graphs():
    
    # comparison Graph
    objects = ('Naive Bayes', 'SVM')
    y_pos = np.arange(len(objects))
    performance = [nb,svm]
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Accuracy')
    plt.title('Cyberbulling')
    plt.show()

    #pie graph
    plt.figure(figsize = (7,7))
    counts = data_1['comp_score'].value_counts()
    plt.pie(counts, labels = counts.index, startangle = 90, counterclock = False, wedgeprops = {'width' : 
    0.6},autopct='%1.1f%%', pctdistance = 0.55, textprops = {'color': 'black', 'fontsize' : 15}, shadow = 
    True,colors = sns.color_palette("Paired")[3:])
    plt.text(x = -0.35, y = 0, s = 'Total Tweets: {}'.format(data.shape[0]))
    plt.title('Distribution of Tweets', fontsize = 14);
    
    #print no.of positive and negative tweets
    print(counts)
    print()
    
    plt.show()
    print()
    print()

mybutton = Button(root, text = 'output', command = prediction)
mybutton.pack()
print("----------------------")
Mbutton = Button(root, text = 'graphs', command = graphs)
Mbutton.pack()

root.mainloop()
