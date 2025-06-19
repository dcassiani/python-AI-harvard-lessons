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
            #print(names) 
            # {'kevin bacon': {'102'}, 'tom cruise': {'129'}, 'cary elwes': {'144'}, 'tom hanks': {'158'}, 
            # 'mandy patinkin': {'1597'}, 'dustin hoffman': {'163'}}

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }
            #print(movies)
            # {'112384': {'title': 'Apollo 13', 'year': '1995', 'stars': set()}, 
            # '104257': {'title': 'A Few Good Men', 'year': '1992', 'stars': set()}}
                  
    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass
            #print(people)
            # {'102': {'name': 'Kevin Bacon', 'birth': '1958', 'movies': {'112384', '104257'}}, '129': {'name': 'Tom Cruise', 'birth': '1962', 
            # 'movies': {'104257', '95953'}}, '144': {'name': 'Cary Elwes', 'birth': '1962', 'movies': set()}, '158': {'name': 'Tom Hanks', 
            # 'birth': '1956', 'movies': set()}, '1597': {'name': 'Mandy Patinkin', 'birth': '1952', 'movies': set()}, '163': {'name': 'Dustin Hoffman', 
            # 'birth': '1937', 'movies': set()}, '1697': {'name': 'Chris Sarandon', 'birth': '1942', 'movies': set()}, '193': {'name': 'Demi Moore', 
            # 'birth': '1962', 'movies': set()}, '197': {'name': 'Jack Nicholson', 'birth': '1937', 'movies': set()}, '200': {'name': 'Bill Paxton', 
            # 'birth': '1955', 'movies': set()}, '398': {'name': 'Sally Field', 'birth': '1946', 'movies': set()}, '420': {'name': 'Valeria Golino', 
            # 'birth': '1965', 'movies': set()}, '596520': {'name': 'Gerald R. Molen', 'birth': '1935', 'movies': set()}, '641': {'name': 'Gary Sinise', 
            # 'birth': '1955', 'movies': set()}, '705': {'name': 'Robin Wright', 'birth': '1966', 'movies': set()}, '914612': {'name': 'Emma Watson', 
            # 'birth': '1990', 'movies': set()}}
            #print(movies)
            # {'112384': {'title': 'Apollo 13', 'year': '1995', 'stars': {'158', '102'}}, '104257': {'title': 'A Few Good Men', 'year': '1992', 
            # 'stars': {'102', '193', '129'}}, '109830': {'title': 'Forrest Gump', 'year': '1994', 'stars': {'158'}}, 
            # '93779': {'title': 'The Princess Bride', 'year': '1987', 'stars': {'144', '1597', '1697'}}, '95953': {'title': 'Rain Man', 
            # 'year': '1988', 'stars': {'129', '163'}}}

def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "small"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name (ie.Tom Hanks): "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name (ie.Dustin Hoffman): "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target) 
    # TODO :  compute the shortest path between the two people - from the person with id source to the person with the id target
    # 
    # should return a list, where each list item is the next (movie_id, person_id) pair
    #
    #  if the return value of shortest_path were [(1, 2), (3, 4)], that would mean that the source starred 
    # in movie 1 with person 2, person 2 starred in movie 3 with person 4, and person 4 is the target.
    #
    # If there are multiple paths of minimum length from the source to the target, your function can return any of them.
    #
    # If there is no possible path between two actors, your function should return None.
    #
    # You may call the neighbors_for_person function, which accepts a person’s id as input, and returns 
    # a set of (movie_id, person_id) pairs for all people who starred in a movie with a given person. 
    # You should not modify anything else in the file other than the shortest_path function, though 
    # you may write additional functions and/or import other Python standard library modules

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


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # inicializar rastreador de numero de estados explorados
    num_explored = 0
    
    # inicializar o Node inicial (source:target-ator) na Fronteira - QueueFrontier
    firstActorNode = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(firstActorNode)   
    
    # inicializar os Explorados vazia
    explored = set()

    # while True: loop até que Fronteira vazia ou Solução encontrada:
    while True:
    # testar se Fronteira vazia, se sim, retornar None (sem solucao)
        if frontier.empty():
            return None

    # remove e instancia um Node da Fronteira
        node = frontier.remove()
    # soma uma ao contador de estados explorados
        num_explored += 1
    
    # IF DA SOLUCAO
    # se essa instancia do Node (node) conter o alvo (target:ator-id)
    # obs: state = source = start-actor-id - ver maze.py
        if node.state == target: 
            # trocar actions e cells para movies e people
            movies = []
            people = []
            # while do node.parent
            while node.parent is not None:                
                movies.append(node.action)
                people.append(node.state)
                node = node.parent
            # manter os reverse para depois printar na ordem certa
            movies.reverse()
            people.reverse()
            # retorno list de (movie_id, person_id) com zip(movies, people) 
            return list(zip(movies, people))
    
    # senao poe id do ator (esta no node.state) nos Explorados
        explored.add(node.state)
    
    # FOR loop dos movie-id, person-id do Node obtendo seus Nodes 
    # vizinhos neighbors_for_person (provided-19:05) para cada Node do loop
        for movie_id, person_id in neighbors_for_person(node.state):
            # IF comparar se a Fronteira NOT util.py.contains_state(person-id)
            # AND person-id NOT IN Explorados
            if not frontier.contains_state(person_id) and person_id not in explored:
                # Entao instanciar novo util.py.Node(state=person-id, parent=node, action=movie-id)
                child = Node(state=person_id, parent=node, action=movie_id)
                # adicionar na Fronteira
                frontier.add(child)

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
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
