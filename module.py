import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import linear_model
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.datasets import fetch_openml
import seaborn as sn
from sklearn.preprocessing import StandardScaler

from scipy.stats import norm, skew #Import Norm and skew for some statistics
from scipy import stats #Import stats
import statsmodels.api as sm #for decomposing the trends, seasonality etc.

from statsmodels.tsa.statespace.sarimax import SARIMAX #for the Seasonal Forecast


#Lets check the ditribution of the target variable (Order_Demand)
from matplotlib import rcParams

df=pd.read_csv('Historical Product Demand.csv')
print(df.dtypes)
df.dropna(axis=0, inplace=True)
df.reset_index(drop=True)

def ordinalEncode_category(df,str):
    ordinalEncoder = preprocessing.OrdinalEncoder()
    X = pd.DataFrame(df[str])
    ordinalEncoder.fit(X)
    df[str] = pd.DataFrame(ordinalEncoder.transform(X))

def labelEncode_category(df,str):
    labelEncoder = preprocessing.LabelEncoder()
    labelEncoder.fit(df[str])
    df[str] = labelEncoder.transform(df[str])

def oneHotEncode_category(df,str):
    enc = preprocessing.OneHotEncoder()
    encodedData = enc.fit_transform(df[[str]])
    encodedDataRecovery = np.argmax(encodedData, axis=1).reshape(-1, 1)
    df[str] = encodedDataRecovery


df_ordinal = df.copy()
df_oneHot = df.copy()
df_label = df.copy()

labelEncode_category(df_label,"Product_Code")
labelEncode_category(df_label,"Warehouse")
labelEncode_category(df_label,"Product_Category")
labelEncode_category(df_label,"Date")


oneHotEncode_category(df_oneHot,"Product_Code")
oneHotEncode_category(df_oneHot,"Warehouse")
oneHotEncode_category(df_oneHot,"Product_Category")
oneHotEncode_category(df_oneHot,"Date")


ordinalEncode_category(df_ordinal,"Product_Code")
ordinalEncode_category(df_ordinal,"Warehouse")
ordinalEncode_category(df_ordinal,"Product_Category")
ordinalEncode_category(df_ordinal,"Date")


print(df_ordinal.head(5))
print(df_oneHot.head(5))
print(df_label.head(5))

#Since the "()" has been removed , Now i Will change the data type.
df['Order_Demand']=df['Order_Demand'].str.replace('(',"", regex=True)
df['Order_Demand']=df['Order_Demand'].str.replace(')',"", regex=True)
df['Order_Demand'] = df['Order_Demand'].astype('int64')


def scale_module(df, targetName):
    y=df[targetName]
    X=df.drop([targetName],1)
    X_train, X_test,y_train,y_test = train_test_split(X,y,random_state=0)

    # Normalization with 4 Scaling methods
    maxAbsScaler = preprocessing.MaxAbsScaler()
    minmaxScaler = preprocessing.MinMaxScaler()
    robustScaler = preprocessing.RobustScaler()
    standardScaler = preprocessing.StandardScaler()

    df_maxAbs_scaled_train = maxAbsScaler.fit_transform(X_train)
    df_maxAbs_scaled_train = pd.DataFrame(df_maxAbs_scaled_train, columns=X_train.columns)
    df_maxAbs_scaled_test = maxAbsScaler.fit_transform(X_test)
    df_maxAbs_scaled_test = pd.DataFrame(df_maxAbs_scaled_test, columns=X_test.columns)

    df_minMax_scaled_train = minmaxScaler.fit_transform(X_train)
    df_minMax_scaled_train = pd.DataFrame(df_minMax_scaled_train, columns=X_train.columns)
    df_minMax_scaled_test = minmaxScaler.fit_transform(X_test)
    df_minMax_scaled_test = pd.DataFrame(df_minMax_scaled_test, columns=X_test.columns)

    df_robust_scaled_train = robustScaler.fit_transform(X_train)
    df_robust_scaled_train = pd.DataFrame(df_robust_scaled_train, columns=X_train.columns)
    df_robust_scaled_test = robustScaler.fit_transform(X_test)
    df_robust_scaled_test = pd.DataFrame(df_robust_scaled_test, columns=X_test.columns)

    df_standard_scaled_train = standardScaler.fit_transform(X_train)
    df_standard_scaled_train = pd.DataFrame(df_standard_scaled_train, columns=X_train.columns)
    df_standard_scaled_test = standardScaler.fit_transform(X_test)
    df_standard_scaled_test = pd.DataFrame(df_standard_scaled_test, columns=X_test.columns)


    
scale_module(df_ordinal, 'Order_Demand')
scale_module(df_oneHot,'Order_Demand')
scale_module(df_label,'Order_Demand')
