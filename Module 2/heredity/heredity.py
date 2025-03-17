import csv
import itertools
import sys
from icecream import ic

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])
    # print(people)

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }
    # print(probabilities)

    # Loop over all sets of people who might have the trait
    names = set(people)
    # ic(powerset(names))
    for have_trait in powerset(names):
        # ic(have_trait)
        
        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        # print(fails_evidence)
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            # ic(one_gene)

            for two_genes in powerset(names - one_gene):
                # ic(two_genes)
                
                
                # ic(people, one_gene, two_genes, have_trait)
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results

    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        
        for row in reader:

            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    p = 1
    for person in people: #iterating over all persons and defining gene and trait to calculate probability
        gene = 2 if person in two_genes else 1 if person in one_gene else 0
        trait = person in have_trait
        # ic(person, gene, trait)
        if not people[person]["mother"] and not people[person]["father"]: # if person has no mother and father, then gene is unconditional
            prob = PROBS["gene"][gene] * PROBS["trait"][gene][trait] # conditional probability for person
            p*=prob # multiplying all probabilities to get joint probability
            # ic(person, prob, p)
        else: #if person has parents, then checking if both parents have information about trait and can pass gene
            mother = people[person]["mother"]
            father = people[person]["father"]
            passed = {mother: 0.0, father: 0.0}
            for parent in passed:
                if parent in one_gene: #if parent has one gene, then 50% chance of passing gene
                    passed[parent] = 0.5
                elif parent in two_genes: #if parent has two genes, then 100% chance of passing gene minus mutation
                    passed[parent] = 1 - PROBS["mutation"]
                else:
                    passed[parent] = PROBS["mutation"] #if parent has no gene, then 1% chance of mutation
            prob = 1
            if gene == 2: #if caluclating probability for two genes, then probability is product of both parents passing gene
                prob = passed[mother] * passed[father]
            elif gene == 1: #if caluclating probability for one gene, then probability is product of one parent passing gene and other not passing gene
                prob = passed[mother] * (1 - passed[father]) + (1 - passed[mother]) * passed[father]
            else: #if caluclating probability for no gene, then probability is product of both parents not passing gene
                prob = (1 - passed[mother]) * (1 - passed[father])
            prob *= PROBS["trait"][gene][trait] #conditional probability for person
            p*=prob # multiplying all probabilities to get joint probability
            # ic(person, prob, p)
    return p
#    raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:

        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p

        probabilities[person]["trait"][person in have_trait] += p # if person in have_trait, add p to True, else add p to False
    # raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    
    for person in probabilities:
        probabilities[person]["gene"] = {gene: probabilities[person]["gene"][gene] / sum(probabilities[person]["gene"].values()) for gene in probabilities[person]["gene"]}
        probabilities[person]["trait"] = {trait: probabilities[person]["trait"][trait] / sum(probabilities[person]["trait"].values()) for trait in probabilities[person]["trait"]}
    # normalization of gene and trait probabilities using dictionary comprehension, for each key in gene and trait dict, 
    # divide the value by sum of all values


if __name__ == "__main__":
    main()
