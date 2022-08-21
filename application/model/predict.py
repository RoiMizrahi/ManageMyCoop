import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import classification_report, accuracy_score, f1_score

from pylab import rcParams
from plotly import tools
import math
from sklearn.decomposition import PCA
from sklearn.metrics import r2_score
import codecs
#import visuals as vs
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
import warnings
warnings.filterwarnings("ignore")
import joblib

df = pd.read_csv('mizrahiCoop.csv')
#print(df.head())

df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce') #date which computer could read and work with
#print(df.head())

df.replace(0, np.NaN,inplace=True) #replace '0' to something pandas can understand...
#print(df.isnull().sum())

df.dropna(subset = ['NumOfChickiens'], inplace = True) #drop each row without chickens
#print(df.isnull().sum())

#plotting the data (for studing it)
plt.figure(figsize=(20,15))
sns.heatmap(df.corr(),annot=True); #medium correlarion between food consumed and num of eggs

plt.rcParams['figure.figsize'] = (18, 8)

plt.subplot(1, 2, 1)
sns.set(style = 'whitegrid')
sns.distplot(df['Eggs'])
plt.title('Distribution of Eggs', fontsize = 20)
plt.xlabel('Range of Eggs')
plt.ylabel('Count')
#normal distribution without touching the data !
#the count means how many time the number appears relatively in the data

plt.figure(figsize=(9,6))
dfBoxPlot = df.boxplot(column='Eggs',grid=False, rot=45, fontsize=15)
#it seems we have to normalized the data..

pcadf = df.copy()
pcadf.replace(np.NaN, 0,inplace=True)
pca = PCA(n_components=9).fit(pcadf.drop(['date'], axis=1))
#pcs_res = vs.pca_results(pcadf.drop(['date'], axis=1), pca) #food is the most weighted feature

Q1 = df['Eggs'].quantile(q=0.25)
Q3 = df['Eggs'].quantile(q=0.75)

IQR = Q3 - Q1
print(IQR)
upper_limit= Q3 + (1.5*IQR)
lower_limit= Q1 - (1.5*IQR)
#df['Eggs'] = np.where(df['Eggs'] <lower_limit ,lower_limit,df['Eggs'])
#df['Eggs'] = np.where(df['Eggs'] > upper_limit,upper_limit,df['Eggs'])

plt.figure(figsize=(9,6))
boxplot = df.boxplot(column='Eggs',grid=False, rot=45, fontsize=15)  #much better :)


plt.rcParams['figure.figsize'] = (18, 8)

plt.subplot(1, 2, 1)
sns.set(style = 'whitegrid')
sns.distplot(df['Eggs'])
plt.title('Distribution of Eggs', fontsize = 20)
plt.xlabel('Range of Eggs')
plt.ylabel('Count')
# even better distribuition

df.replace(np.NaN, 0,inplace=True)
df.drop(['date'], axis=1, inplace=True) #the regressor doesn't know how to handle date time

#realized that dropping temp and humid made the algorithem even better
#food consumed is just like current food
df.drop(['Temp','Humidity','Food','Broken'], axis=1 , inplace=True)
print(df.head())

#preparing the data
X = df.drop(['Eggs'], axis=1)
y = df['Eggs']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=30)

#running the Decision Tree Regressor
reg = DecisionTreeRegressor(random_state=30, max_depth=10)
reg.fit(X_train,y_train)
y_pred = reg.predict(X_test)
score = r2_score(y_test,y_pred)
print ("Our R_2 is %.2f" %score)

#plotting the results
plt.figure(figsize=(15,12))
plt.scatter(y_pred, y_test, color = 'magenta')
plt.xlabel("PREDICTIONS", fontsize=20)
plt.ylabel("Actual Eggs", fontsize=20)
plt.title("Decision Tree Regressor", fontsize=20)
plt.show()

joblib.dump(reg, 'reg.pkl')
