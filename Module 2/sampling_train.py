import numpy 
import torch
from collections import Counter
from bayesian_model import model

# sample = model.sample(10)
# print('s', sample)

# probability = model.probability(sample)
# print(probability)

# Compute distribution of Appointment given that train is delayed
N = 10000
data = []
    # Generate a sample based on the model that we defined earlier
sample = model.sample(N)
    
# print('sample', i, ':', sample )

# Repeat sampling 10,000 times
for i in range(N):

    # If, in this sample, the variable of Train has the value delayed, save the sample.
    # Since we are interested in the probability distribution of Appointment given that the train is delayed,
    # we discard the samples where the train was on time.
    if sample[i, 2] == 1:  # Assuming train delayed is encoded as 1 (i row in the tensor and 3nd column)
        data.append(sample[i, 3].item())  # Appointment (value of 4th column)

# Count how many times each value of the variable appeared
count = Counter(data)
prob_attend = count[0] / sum(count.values())
print(count)
print(f"Probability that you attend given train is delayed: {prob_attend:.4f}")