import pickle

raw_results = pickle.load(open('./results-3.pckl', 'rb'))
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

pickle.dump(portable_results, open('../final-2.pckl', 'wb'))
