from pomegranate.distributions import Categorical, ConditionalCategorical
from pomegranate.markov_chain import * # type: ignore
from pomegranate.hmm import DenseHMM

import numpy

# ------------------------------------Markov Model------------------------------------

# Define starting probabilities
probs_start = torch.tensor([[0.5,   # sun
                            0.5]    # rain
])
start = Categorical(probs=probs_start)
events = ['sun', 'rain']

# Define transition model
probs_transitions = torch.tensor([
    [0.8, 0.2],  # sun [start]: sun, rain
    [0.3, 0.7]   # rain [start]: sun, rain
])
transitions = ConditionalCategorical(probs=[probs_transitions])

# Create Markov chain
model = MarkovChain([start, transitions])

# print(model.sample(5))

# Sample about 50 states from chain (if starts from sun, can change if desired)
sample = []
named_sample = []
full = []
for i in range(100):
    samples = model.sample(1)
    full.append(samples)
    if samples[:, 0] == 0: # sun as start event
        sample.append(samples[:, 1].item())
        named_sample.append(events[samples[:, 1].item()]) # type: ignore
# print(f"Full #: {len(full)}, samples: {full}")        
print(f"Filtered #: {len(sample)}, samples: {sample}")
print(f"Events #: {len(named_sample)}, samples: {named_sample}")

# ------------------------------------Hidden Markov Models------------------------------------

# Observation model for each state
probs_sun = torch.tensor([[0.2,   # umbrella
                            0.8]    # no umbrella
])
sun = Categorical(probs=probs_sun)
sun.name = 'sun' # Add a name attribute

probs_rain = torch.tensor([[0.9,   # umbrella
                            0.1]    # no umbrella
])
rain = Categorical(probs=probs_rain)
rain.name = 'rain' # Add a name attribute

states = [sun, rain]

# Retrieve names of Categorical objects
state_names = [state.name for state in states]

# Transition model (prediction for tommorow's weather)
edges = [
    [0.8, 0.2], # "sun": sun, rain
    [0.3, 0.7] # "rain": sun, rain
]

# Starting probabilities
starts = [0.5, 0.5]

# Create the model
model = DenseHMM(states, edges=edges, starts=starts)

# Observed data
observations = numpy.array([[[0],[0],[1],[0],[0],[0],[0],[1],[1]]])
print(observations.shape)

# Predict underlying states
predictions_raw = model.predict(observations)
# Predictions as names of events
predictions = [state_names[prediction] for prediction in predictions_raw[0].tolist()]
print(predictions)