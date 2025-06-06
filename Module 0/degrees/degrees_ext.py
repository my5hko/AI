import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")
    # print(people)
    # print(names)
    # print(movies)
    search = True


    # source = person_id_for_name(input("Name: "))
    # if source is None:
    #     sys.exit("Person not found.")
    # target = person_id_for_name(input("Name: "))
    # if target is None:
    #     sys.exit("Person not found.")
    while search :
        searching()
        search = input("Would you like to repeat search? Press y to repeat, any other key to Exit: ").lower() == "y"
    else:
        sys.exit("Exit!")


 
def searching():
    source, target = optimize_source()
    print("Searching...")
    path = shortest_path(source, target)
    print("Search finished")
    
    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

def optimize_source():
    """
    Optimize the source and target for a given person to use the person with less number of movies as a source to shorten search time

    Parameters:
    - source (str): The name of the source person.
    - target (str): The name of the target person.

    Returns:
    - source (str): The optimized source person.
    - target (str): The optimized target person.
    """
    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    if len(neighbors_for_person(source))/2 > len(neighbors_for_person(target)):
        source, target = target, source
    return source, target




def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # if len(neighbors_for_person(source))/2 > len(neighbors_for_person(target)):
    #     source, target = target, source

    root = Node(source, [], neighbors_for_person(source))
    frontier = QueueFrontier()
    frontier.add(root)
    path = []
    checked = set()

    while not frontier.empty():
        node = frontier.remove()
        for action in node.action:
            path = node.parent + [action]
#            print(node.state)
#            print(path)
            if action[1] == target:
                return path
            else:
                if action[1] not in checked:
                    checked.add(action[1])
#                    print(checked)
                    new_node = Node(action[1], path, neighbors_for_person(action[1]))
                    for new_action in new_node.action:
                        if new_action[1] == target:
                            return new_node.parent + [new_action]
                    frontier.add(new_node)
#        for front in frontier.frontier:
#            print(front.state, front.parent, front.action)

    
    return None


def check_node(node, target):
    """
    Check if the target is present in the node's action.

    Parameters:
    node (object): The node object to be checked.
    target (object): The target object to be searched for in the node's action.

    Returns:
    list: The path from the root node to the target node if found, otherwise None.
    """
    for action in node.action:
        path = node.parent + [action]
#            print(node.state)
#            print(path)
        if action[1] == target:
            return path

    for action in node.action:
            path = node.parent + [action]
#            print(node.state)
#            print(path)
            if action[1] == target:
                return path



def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
#        for person_id in movies[movie_id]["stars"]:
#            neighbors.add((movie_id, person_id))
        for neighbor in movies[movie_id]["stars"] :
            if neighbor != person_id:
                neighbors.add((movie_id, neighbor))
    return neighbors


if __name__ == "__main__":
    main()
