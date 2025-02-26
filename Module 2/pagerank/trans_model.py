import random

corpus = {'ai.html': {'inference.html', 'algorithms.html'}, 'algorithms.html': {'programming.html', 'recursion.html'}, 'c.html': {'programming.html'}, 'inference.html': {'ai.html'}, 'logic.html': {'inference.html'}, 'programming.html': {'python.html', 'c.html'}, 'python.html': {'programming.html', 'ai.html'}, 'recursion.html': set()}
keys = [key for key in corpus]
start = random.choice(keys)
print('Keys:', keys)
print(start)
print(set(corpus))

page = 'ai.html'
damping_factor = 0.85

model = dict()
page_links_number = len(corpus[page])

if not page_links_number: 
    for link in corpus:
        model[link] = 1/len(corpus)
# The return value of the function should be a Python dictionary with one key for each page in the corpus. 
# Each key should be mapped to a value representing the probability that a random surfer would choose that page next. 
# The values in this returned probability distribution should sum to 1.
#   With probability damping_factor, the random surfer should randomly choose one of the links from page with equal probability.
#   With probability 1 - damping_factor, the random surfer should randomly choose one of all pages in the corpus with equal probability.
# For example, if the corpus were {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}, the page was 
# "1.html", and the damping_factor was 0.85, then the output of transition_model should be {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}. 
# This is because with probability 0.85, we choose randomly to go from page 1 to either page 2 or page 3 
# (so each of page 2 or page 3 has probability 0.425 to start), but every page gets an additional 0.05 because with 
# probability 0.15 we choose randomly among all three of the pages. 
else:
    for link in corpus:
        if link not in corpus[page]:
            model[link] = (1 - damping_factor) / len(corpus)
        else:
            model[link] = damping_factor / page_links_number + (1 - damping_factor) / len(corpus)
    
print(model)
next_page = random.choices(list(model.keys()), list(model.values()), k=1)
print(next_page[0])