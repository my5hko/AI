
from pomegranate.distributions import Categorical, ConditionalCategorical
from pomegranate.bayesian_network import BayesianNetwork
import numpy 
import torch

# Вузол «дощ» не має батьків
# rain = Node(Categorical({
#     "none": 0.7,
#     "light": 0.2,
#     "heavy": 0.1
# }), name="rain")
rain_events = {"none" : 0, "light" : 1, "heavy" : 2}
rain_probs = [0.7, 0.2, 0.1]
rain = Categorical([rain_probs])
# print(rain.probs)

# Вузол «ремонт» залежить від вузла «дощ»
maintenance_events = {"yes" : 0, "no" : 1}
maintenance_probs = numpy.array([[0.4, 0.6], [0.2, 0.8], [0.1, 0.9]])
# maintenance = Node(ConditionalCategorical([
#     ["none", "yes", 0.4],
#     ["none", "no", 0.6],
#     ["light", "yes", 0.2],
#     ["light", "no", 0.8],
#     ["heavy", "yes", 0.1],
#     ["heavy", "no", 0.9]
# ], [rain.distribution]), name="maintenance")
maintenance = ConditionalCategorical([maintenance_probs])

# Вузол «потяг» залежить від вузлів «дощ» і «ремонт»
train_events = {"on time" : 0, "delayed" : 1}
train_probs = numpy.array([[[0.8, 0.2], [0.9, 0.1]], [[0.6, 0.4], [0.7, 0.3]], [[0.4, 0.6], [0.5, 0.5]]])
# train = Node(ConditionalCategorical([
#     ["none", "yes", "on time", 0.8],
#     ["none", "yes", "delayed", 0.2],
#     ["none", "no", "on time", 0.9],
#     ["none", "no", "delayed", 0.1],
#     ["light", "yes", "on time", 0.6],
#     ["light", "yes", "delayed", 0.4],
#     ["light", "no", "on time", 0.7],
#     ["light", "no", "delayed", 0.3],
#     ["heavy", "yes", "on time", 0.4],
#     ["heavy", "yes", "delayed", 0.6],
#     ["heavy", "no", "on time", 0.5],
#     ["heavy", "no", "delayed", 0.5],
# ], [rain.distribution, maintenance.distribution]), name="train")
train = ConditionalCategorical([train_probs])

# Вузол «зустріч» залежить від вузла «потяг»
appointment_events = {"attend" : 0, "miss" : 1}
appointment_probs = numpy.array([[0.9, 0.1], [0.6, 0.4]])
# appointment = Node(ConditionalCategorical([
#     ["on time", "attend", 0.9],
#     ["on time", "miss", 0.1],
#     ["delayed", "attend", 0.6],
#     ["delayed", "miss", 0.4]
# ], [train.distribution]), name="appointment")
appointment = ConditionalCategorical([appointment_probs])

events = [['rain', ["none", "light", "heavy"]], ['maintenance', ["yes", "no"]], ['train', ["on time", "delayed"]], ['appointment', ["attend", "miss"]]]
#Створіть Баєсову мережу і додайте стани
model = BayesianNetwork()
#model.add_states(rain, maintenance, train, appointment)

model.add_distributions([rain, maintenance, train, appointment])
# Позначте стрілками пов’язані вузли
model.add_edge(rain, maintenance)
model.add_edge(rain, train)
model.add_edge(maintenance, train)
model.add_edge(train, appointment)
# Завершіть модель
#model.bake()

# Обчисліть імовірність для цього спостереження

#probability = model.probability([["none", "no", "on time", "attend"]])
# probability = model.probability([[rain_events["none"], maintenance_events["no"], train_events["on time"], appointment_events["attend"]]])
#X = torch.tensor([[0, 0, 0, 0]])
X = torch.tensor([[rain_events["none"], maintenance_events["no"], train_events["on time"], appointment_events["miss"]]])
print(X)
probability = model.probability(X)
print(probability)
X_masked = torch.masked.MaskedTensor(X, mask=X == 1)
print(X_masked)
print(model.predict_proba(X_masked))
# print(model.predict_proba(X_masked)[0])
# print(model.predict_proba(X_masked)[1])
# print(model.predict_proba(X_masked)[2])
# print(model.predict_proba(X_masked)[3])

for event, prediction in zip(events, model.predict_proba(X_masked)):
    if (prediction[0] == 1).any():
        index_of_1 = torch.nonzero(prediction[0] == 1)[0]
        print(f"{event[0]}: {event[1][index_of_1]}")
    else:
        print(f"{event[0]}")
        for i in range(len(prediction[0])):
    #        print(len(prediction[0]))
            
            print(f"     {event[1][i]}: {prediction[0][i]:.4f}")

# print(model.distributions[0].probs)
# print(model.distributions[1].probs[0])
# print(model.distributions[2].probs[0])
# print(model.distributions[3].probs[0])
# print('d', model.distributions)
# print('e', model.edges)
print('s', model.sample(10))