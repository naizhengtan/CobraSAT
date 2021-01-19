
# coding: utf-8

# In[2]:


import pickle
from itertools import product
from functools import reduce
from collections import defaultdict

results = pickle.load(open('../final.pckl', 'rb'))
results = sorted(results, key=lambda el: 'zzzz' if el['encoding'] == 'mono' else el['encoding'] + el['polygraph'])


# In[3]:


read_percentages = [50, 75, 90]
polygraph_sizes = range(100, 301, 50)
polygraph_dir = 'polygraphs/workloads3'

polygraphs = [f'{polygraph_dir}/chengR{read_percent}-{size}.polyg'
                for size, read_percent in product(polygraph_sizes, read_percentages)]


# In[4]:


def total_time(timings):
    return reduce(lambda total, key: total + timings[key], timings, 0)

def results_by_encoding_for_percent(results, read_percent):
    encodings = reduce(lambda s, item: s | {item['encoding']}, results, set())
    by_encoding = defaultdict(list)
    for size in polygraph_sizes:
        for result in results:
            if result['polygraph'] == f'{polygraph_dir}/chengR{read_percent}-{size}.polyg':
                by_encoding[result['encoding']].append(total_time(result['result'][1]))
    
    return by_encoding


# In[5]:


get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")
get_ipython().run_line_magic('matplotlib', 'inline')

import numpy as np
import matplotlib.pyplot as plt
import math
from cycler import cycler


# In[6]:


def plot_by_encoding_for_percent(results, read_percent=50, encodings=[], exclude=True, log_scale=True):
    fig, ax = plt.subplots(figsize=(12, 12))

    rows = results_by_encoding_for_percent(results, read_percent)
    default_colors = cycler('color', ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])
    ax.set_prop_cycle(default_colors * cycler(linestyle=['-', '--', ':',]))
    
    for enc in rows:
        # XOR
        if bool(enc in encodings) != exclude: 
            timing = np.pad(rows[enc], (0, 5 - len(rows[enc])), 'constant', constant_values=(math.inf))
            ax.scatter(polygraph_sizes, timing, )
            ax.plot(polygraph_sizes, timing, label=enc)

    if log_scale:
        ax.set_yscale('log')
    ax.legend()


# In[7]:


# plot_by_encoding_for_percent(results, 50, ['tc1', 'tc3', 'tree-bv', 'axiom'])
plot_by_encoding_for_percent(results, 50)


# In[8]:


plot_by_encoding_for_percent(results, 75)


# In[9]:


plot_by_encoding_for_percent(results, 90, ['tc1', 'tc3', 'tree-bv', 'axiom'])


# In[10]:


def by_encoding(results, encoding):
    output = []
    
    for percent in read_percentages:
        rows = results_by_encoding_for_percent(results, percent)
        output.append(rows[encoding])
    
    return output


# In[11]:


def plot_encoding(results, encoding):
    fig, ax = plt.subplots(figsize=(12, 12))
    rows = by_encoding(results, encoding)
    for row in rows:
        timing = np.pad(row, (0, 5 - len(row)), 'constant', constant_values=(math.inf))
        ax.plot(polygraph_sizes, timing)
    ax.legend(read_percentages)
        


# In[12]:


plot_encoding(results, 'tc1')


# In[13]:


plot_encoding(results, 'mono')


# In[14]:


plot_encoding(results, 'binary-label-minisat')


# In[15]:


plot_encoding(results, 'binary-label-z3')


# In[16]:


def encode_timing_for_percent(results, read_percent, timing):
    encodings = reduce(lambda s, item: s | {item['encoding']}, results, set())
    by_encoding = defaultdict(list)
    for size in polygraph_sizes:
        for result in results:
            if f'chengR{read_percent}-{size}.polyg' in result['polygraph']:
                by_encoding[result['encoding']].append(result['result'][1][timing])
    return by_encoding


# In[17]:


def plot_encode_time_for_percent(results, read_percent=50, exclude=[]):
    fig, ax = plt.subplots(figsize=(12, 12))

    rows = encode_timing_for_percent(results, read_percent, 'encode')
    default_colors = cycler('color', ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])
    ax.set_prop_cycle(default_colors * cycler(linestyle=['-', '--', ':',]))
#     cm = plt.get_cmap('gist_rainbow')
#     ax.set_prop_cycle(cycler(color=[cm(1.*i/len(rows)) for i in range(len(rows))]))
    
    for enc in rows:
        if not enc in exclude:
            timing = np.pad(rows[enc], (0, 5 - len(rows[enc])), 'constant', constant_values=(math.inf))
            ax.scatter(polygraph_sizes, timing)
            ax.plot(polygraph_sizes, timing, label=enc)
    
#     ax.set_yscale('log')
    ax.legend()


# In[18]:


plot_encode_time_for_percent(results, 50)


# In[19]:


def plot_solve_time_for_percent(results, read_percent=50, exclude=[]):
    fig, ax = plt.subplots(figsize=(12, 12))

    rows = encode_timing_for_percent(results, read_percent, 'solve')
    default_colors = cycler('color', ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])
    ax.set_prop_cycle(default_colors * cycler(linestyle=['-', '--', ':',]))
#     cm = plt.get_cmap('gist_rainbow')
#     ax.set_prop_cycle(cycler(color=[cm(1.*i/len(rows)) for i in range(len(rows))]))
    
    for enc in rows:
        if not enc in exclude:
            timing = np.pad(rows[enc], (0, 5 - len(rows[enc])), 'constant', constant_values=(math.inf))
            ax.scatter(polygraph_sizes, timing)
            ax.plot(polygraph_sizes, timing, label=enc)
    
#     ax.set_yscale('log')
    ax.legend()


# In[20]:


plot_solve_time_for_percent(results, 50, exclude=['tree-bv'])


# In[21]:


# number of clauses?


# In[50]:


import matplotlib.cm as cm
counts = pickle.load(open('../count.pckl', 'rb'))
sat_vars = ['binary-label', 'unary-label', 'tc1', 'tc3', 'axiom', 'topo-bv']
# {'tc3', 'unary-label', 'binary-label', 'tc1'}

var_counts_and_timings = {}

def has_sat_vars(encoding_name):
    return any([sv in encoding_name for sv in sat_vars])
    
def plot_sat_vars(results, counts):
    fig, ax = plt.subplots(figsize=(12, 12))
    
    timings_y = []
    encodings = {}
    var_counts_x = defaultdict(list)
    solve_time_y = defaultdict(list)
    
    row_count_binary = 0
    row_count_unary = 0
    row_count_topo = 0
    
    for row in results:
        enc = row['encoding']
        polyg = row['polygraph']
        
        # Only binary label has variable counts for size over 300.
        size = int(polyg[len('polygraphs/workloads3/chengR'):].split('-')[1].split('.')[0])         
        
        if size <= 300 and has_sat_vars(enc) and polyg:
            count_enc = enc
            
            # not really just minisat, but needs that for the label
            if 'binary-label' in enc:
                count_enc = 'binary-label-minisat'
                row_count_binary += 1
    
            # not really just minisat, but needs that for the label
            elif 'unary-label' in enc:
                count_enc = 'unary-label-minisat'
                row_count_unary += 1
            
            elif count_enc == 'topo-bv':
                row_count_topo += 1
                
            if not 'tc' in count_enc and count_enc != 'axiom':            
                encodings[count_enc] = True
                var_counts_x[count_enc].append(int(counts[(count_enc, polyg)]['var']))
                solve_time_y[count_enc].append(total_time(row['result'][1]))
    
    for encoding in encodings:
            ax.scatter(var_counts_x[encoding], solve_time_y[encoding])
    
    ax.set_yscale('log')
    ax.legend(encodings)


# In[51]:


plot_sat_vars(results, counts)


# In[52]:


binary_unary = ['binary-label-minisat', 'binary-label-z3', 'binary-label-yices2', 'unary-label-minisat', 'unary-label-z3', 'unary-label-yices2']
plot_by_encoding_for_percent(results, 50, binary_unary, False, False)


# In[53]:


plot_by_encoding_for_percent(results, 50, ['unary-label-minisat', 'unary-label-z3', 'unary-label-yices2'], False)


# In[54]:


plot_by_encoding_for_percent(results, 50, ['tree-bv'])


# In[55]:


def plot_sat_vars_solves(results, counts):
    fig, ax = plt.subplots(figsize=(12, 12))
    
    timings_y = []
    encodings = {}
    var_counts_x = defaultdict(list)
    solve_time_y = defaultdict(list)
    
    for row in results:
        enc = row['encoding']
        polyg = row['polygraph']

        if has_sat_vars(enc):
            count_enc = enc
            if 'binary-label' in enc:
                count_enc = 'binary-label-minisat'
            elif 'unary-label' in enc:
                count_enc = 'unary-label-minisat'
            
            encodings[count_enc] = True
            
            var_counts_x[count_enc].append(int(counts[(count_enc, polyg)]['var']))
            solve_time_y[count_enc].append(row['result'][1]['solve'])
    
    for encoding in encodings:
        ax.scatter(var_counts_x[encoding], solve_time_y[encoding])
    
    ax.set_xscale('log')
    ax.legend(encodings.keys())


# In[56]:


# TODO: how to interpret log scale graphs?
plot_sat_vars_solves(results, counts)


# In[57]:


plot_by_encoding_for_percent(results, 75, ['binary-label-minisat', 'binary-label-z3', 'binary-label-yices2'], False)

