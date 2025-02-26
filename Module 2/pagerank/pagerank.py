import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    model = dict()
    page_links_number = len(corpus[page])
    # if page has no outgoing links, then transition_model should return a probability distribution that chooses 
    # randomly among all pages with equal probability. (In other words, if a page has no links, we can pretend it 
    # has links to all pages in the corpus, including itself.)
    if page_links_number == 0: 
        probability = 1 / len(corpus)
        model = {link: probability for link in corpus}
        # for link in corpus: replaced with dict comprehension
        #     model[link] = 1/len(corpus)
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
        random_surfer_prob = (1 - damping_factor) / len(corpus)
        link_prob = damping_factor / page_links_number
        for link in corpus:
            if link not in corpus[page]:
                model[link] = random_surfer_prob
            else:
                model[link] = link_prob + random_surfer_prob
    
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = [key for key in corpus] # getting pages in corpus
    rank = {page: 0 for page in pages} # initial ranks for each page in corpus
    start_page = random.choice(pages) # choosing a random page to start
    rank[start_page] += 1 # incrementing rank for the start page
    page = start_page

    for i in range(n-1):
        model = transition_model(corpus, page, damping_factor)
        next_page = random.choices(list(model.keys()), list(model.values()), k=1)[0] #chhosing next page based on weighting in the model
        rank[next_page] += 1 # incrementing rank for the next page
        page = next_page # setting next page as page for the next cycle
    print(sum(rank.values())) # checking if sum of ranks is equal to n
    rank = {key: value/sum(rank.values()) for key, value in rank.items()} # normalizing ranks to probabilities
    return rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    threshold = 0.001 # threshold for convergence
    pages = [key for key in corpus] # getting pages in corpus
    rank = {page: 1/len(corpus) for page in pages} # initial ranks for each page in corpus = 1/number of pages
    old_rank = {page: 0 for page in pages} # new ranks for each page with zeros
    # print(corpus)
    # print(rank)

    while any(abs(rank[page] - old_rank[page]) > threshold for page in pages): # iterating until convergence according to threshold
        old_rank = rank.copy() #copying current rank as old rank
        new_rank = {page: 0 for page in pages} # empty new rank with zeros for each page 
        for page in pages: # iterating pages to calculate page rank
            links_rank = 0
            for link in corpus: # iterating links in corpus to find pages with links to the target page 
 #               corpus[link] = corpus[link] if corpus[link] else set(corpus) # if page has no links, then it has links to all pages in the corpus
                corpus[link] = {page for page in corpus} if not corpus[link] else corpus[link] # if page has no links, then it has links to all pages in the corpus
                if page in corpus[link]: #if link to page is found
                    links_rank += rank[link] / len(corpus[link]) #getting rank for all pages with links to the target page 
            new_rank[page] = (1 - damping_factor) / len(corpus) + damping_factor * links_rank # iterative formula for page rank
        rank = new_rank.copy()
        # print(rank)
    return old_rank


#    raise NotImplementedError


if __name__ == "__main__":
    main()
