import pickle

# results = pickle.load(open('../results.pckl', 'rb'))
# results2 = pickle.load(open('../results-2.pckl', 'rb'))
# results.update(results2)

raw_results = pickle.load(open('../results-3.pckl', 'rb'))
portable_results = []

for experiment in raw_results:
    result = raw_results[experiment]
    polygraph, encoding = experiment
    if not result is None:
        portable_results.append({
            'encoding': encoding.name,
            'polygraph': polygraph,
            'result': result
        })

pickle.dump(portable_results, open('../final.pckl', 'wb'))
