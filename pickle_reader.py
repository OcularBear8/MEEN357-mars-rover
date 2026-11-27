import pickle

with open('FA25_SecYY_TeamXX_candidate.pickle', 'rb') as file:
    data = pickle.load(file)

print(data)
