#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#library
import numpy as np
from sklearn.externals import joblib
from sklearn.linear_model import LinearRegression


# In[ ]:


#dataset 
X= np.array([400,350,1000,200,560,430,1500,780,670,480]).reshape((-1, 1))
Y= np.array([1500,750,1760,500,800,900,890,1600,2000,1970])


# In[ ]:


#call model regression
model = LinearRegression().fit(X,Y)


# In[ ]:


#save model
filename = 'model.sav'
joblib.dump(model, filename)


# In[ ]:


#load model
loaded_model = joblib.load(filename)


# In[ ]:


#prediction model
loaded_model.predict(10)


# In[ ]:




