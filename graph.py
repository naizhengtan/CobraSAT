
# coding: utf-8

# In[11]:


import matplotlib.pyplot as plt

workloads = [100, 200, 300]

rw_tc1 = [1.57716, 27.7370, 209.178]
rw_tc3 = [1.39612, 22.1905, 166.987]

twitter_tc1 = [2.23161, 48.9854, 308.112]
twitter_tc3 = [2.05645, 50.0334, 273.290]

tpcc_tc1 = [5.37104, 885.760]
tpcc_tc3 = [2.67085, 403.436]

fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(workloads, rw_tc1, workloads, rw_tc3,         workloads, twitter_tc1, workloads, twitter_tc3)
ax.legend(('rw_tc1', 'rw_tc3', 'twitter_tc1', 'twitter_tc3'))

fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(workloads[0:2], tpcc_tc1, workloads[0:2], tpcc_tc3)
ax.legend(('tpcc_tc1', 'tpcc_tc3'))

