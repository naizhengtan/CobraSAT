
# coding: utf-8

# In[28]:


import matplotlib.pyplot as plt
import numpy as np

def compare_encodings_minisat():
    workloads = [100, 200, 300]

    rw_tc1 = [1.57716, 27.7370, 209.178]
    rw_tc3 = [1.39612, 22.1905, 166.987]

    twitter_tc1 = [2.23161, 48.9854, 308.112]
    twitter_tc3 = [2.05645, 50.0334, 273.290]

    tpcc_tc1 = [5.37104, 885.760]
    tpcc_tc3 = [2.67085, 403.436]

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(workloads, rw_tc1, workloads, rw_tc3,             workloads, twitter_tc1, workloads, twitter_tc3)
    ax.legend(('rw_tc1', 'rw_tc3', 'twitter_tc1', 'twitter_tc3'))

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(workloads[0:2], tpcc_tc1, workloads[0:2], tpcc_tc3)
    ax.legend(('tpcc_tc1', 'tpcc_tc3'))


# In[29]:


compare_encodings_minisat()


# In[52]:


def compare_encodings_z3():
    workloads = [100, 200, 300]
    
    
    cheng_solve = {
        'tree': [2874, 14948, 23286],
        'top': [2616, 14166, 20192],
        'tc': [200, 1307, 4565]
    }
    
    cheng_build = {
        'tree': [3824, 10962, 34513],
        'top': [1238, 4668, 10659],
        'tc': [2437, 8193, 18677]
    }
    
    cheng = {
        'solve': cheng_solve,
        'build': cheng_build
    }
    
    twitter_solve = {
        'tree': [2961, 16739, 23869],
        'top': [2828, 15287, 22841],
        'tc': [235, 1600, 5539]
    }
    
    twitter_build = {
        'tree': [4073, 16453, 37087],
        'top': [1308, 5238, 11577],
        'tc': [2198, 8735, 20173]
    }
    
    twitter = {
        'solve': twitter_solve,
        'build': twitter_build
    }
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(workloads, np.array(cheng_build['tree']) + np.array(cheng_solve['tree']),             workloads, np.array(cheng_build['top']) + np.array(cheng_solve['top']),             workloads, np.array(cheng_build['tc']) + np.array(cheng_solve['tc']))
    ax.legend(('tree', 'top', 'tc'))
    ax.set_title('cheng: build + solve')
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(workloads, cheng_solve['tree'], workloads, cheng_solve['top'], workloads, cheng_solve['tc'])
    ax.set_title('cheng: solve')
        
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(workloads, cheng_build['tree'], workloads, cheng_build['top'], workloads, cheng_build['tc'])
    ax.set_title('cheng: build')
    
        
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(workloads, np.array(twitter_build['tree']) + np.array(twitter_solve['tree']),             workloads, np.array(twitter_build['top']) + np.array(twitter_solve['top']),             workloads, np.array(twitter_build['tc']) + np.array(twitter_solve['tc']))
    ax.legend(('tree', 'top', 'tc'))
    ax.set_title('twitter: build + solve')
            
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(workloads, twitter_solve['tree'], workloads, twitter_solve['top'], workloads, twitter_solve['tc'])
    ax.set_title('twitter: solve')
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(workloads, twitter_build['tree'], workloads, twitter_build['top'], workloads, twitter_build['tc'])
    ax.set_title('twitter: build')


# In[53]:


compare_encodings_z3()

