import random
from infos import teams_dict, stadiums_dict

population_size = 500
generations = 5000

def CreateMatchList():
    match_list = []
    selected_teams = []
    selected_stadium = []
    while len(match_list) < 4:
        team1 = random.choice(list(teams_dict.keys()))
        team2 = random.choice(list(teams_dict.keys()))
        stadium = random.choice(list(stadiums_dict.keys()))
        if team1 != team2 and (team1 not in selected_teams and team2 not in selected_teams) and stadium not in selected_stadium:
            selected_teams.append(team1)
            selected_teams.append(team2)
            selected_stadium.append(stadium)
            match_list.append((team1, team2, stadium))
    return match_list

"""def CreateMatchList():
    match_list = []
    teams = list(teams_dict.keys())
    stadiums = list(stadiums_dict.keys())
    random.shuffle(teams)
    random.shuffle(stadiums)
    for _ in range(4):
        team1, team2 = random.sample(teams, 2)
        stadium = random.choice(stadiums)
        match_list.append((team1, team2, stadium))
    return match_list"""



population_match = [CreateMatchList() for _ in range(population_size)]

def Fitness(population):
    score = 0
    for match in population:
        team1, team2, stadium = match
        team1_info = teams_dict[team1]
        team2_info = teams_dict[team2]
        stadium_info = stadiums_dict[stadium]

        team_city1 = team1_info["City"]
        team_stadium1 = team1_info["Stadium"]
        team_city2 = team2_info["City"]
        team_stadium2 = team2_info["Stadium"]
        stadium_city = stadium_info["Stadium City"]

        if team_city1 == stadium_city:
            score += 5
        if team_city2 == stadium_city:
            score += 2
        if team_city1 == team_city2 and stadium_city == team_city1:
            score += 10
        if stadium == team_stadium1 and stadium == team_stadium2:
            score += 30
        if stadium == team_stadium1:
            score += 20
        if stadium == team_stadium2:
            score += 10

    return score

def Selection(population):
    fitness_list = [Fitness(match_list) for match_list in population]
    selected = random.choices(population, weights=fitness_list, k=250)
    return selected

fitness_list = []
generation = 0
while generation <= generations:
    fitness_list.append(max(population_match, key=Fitness))
    selected = Selection(population_match)

    #Crossover
    crossover = []
    for match in selected:
        match_copy = list(match)
        #Swap the first with the third stadium, and the second with the fourth
        match_copy[0] = list(match_copy[0])
        match_copy[1] = list(match_copy[1])
        match_copy[2] = list(match_copy[2])
        match_copy[3] = list(match_copy[3])
        match_copy[0][2], match_copy[2][2] = match_copy[2][2], match_copy[0][2]
        match_copy[1][2], match_copy[3][2] = match_copy[3][2], match_copy[1][2]
        match_copy = tuple(match_copy)
        crossover.append(match_copy)

    #Mutation
    mutation = []
    for match in selected:
        id = random.randint(0, 3)
        team1, team2, old_stadium = match[id]
        new_stadium = random.choice([stadium for stadium in stadiums_dict.keys() if stadium != old_stadium])
        mutated_match = list(match)
        mutated_match[id] = (team1, team2, new_stadium)
        mutation.append(mutated_match)

    population_match = crossover + mutation
    generation += 1

print("Matchs:\n")

best_matches = max(fitness_list, key=Fitness)

for match in best_matches:
    team1, team2, stadium = match
    print(f"{team1} vs {team2} - {stadium}")
print(f"Fitness Value: {Fitness(best_matches)}")
