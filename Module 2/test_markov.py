from pomegranate.markov_chain import MarkovChain
import torch
import numpy

model = MarkovChain(k=3)

X = torch.tensor([[[1], [0], [0], [1]],
                  [[0], [1], [0], [0]],
                  [[0], [0], [0], [0]],
                  [[0], [0], [0], [1]],
                  [[0], [1], [1], [0]]])

model.fit(X)

print(model.distributions[0].probs[0])

sequence = 'CGACTACTGACTACTCGCCGACGCGACTGCCGTCTATACTGCGCATACGGC'
X = numpy.array([[[['A', 'C', 'G', 'T'].index(char)] for char in sequence]])
X.shape
print(X)