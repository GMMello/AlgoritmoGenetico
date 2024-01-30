import random
import infos

population_size = 500
generations = 5000

def CreateMatchList():
    match_list = []
    selected_teams = []
    selected_stadium = []
    while len(match_list) < 4:
        team1 = random.choice(infos.teams)["Team"]
        team2 = random.choice(infos.teams)["Team"]
        stadium = random.choice(infos.stadium)["Stadium"]
        if team1 != team2 and (team1 not in selected_teams and team2 not in selected_teams) and stadium not in selected_stadium:
            selected_teams.append(team1)
            selected_teams.append(team2)
            selected_stadium.append(stadium)
            match_list.append((team1, team2, stadium))
    return match_list

population_match = [CreateMatchList() for _ in range(population_size)]

def Fitness(population):
    score = 0
    aux = 0
    for i in range(len(population)):
        match = population[i]
        team1 = match[aux]
        team2 = match[aux + 1]
        stadium = match[aux + 2]
        aux = 0

        for team in infos.teams:
            if team["Team"] == team1:
                team_city1 = str(team["City"])
                team_stadium1 = str(team["Stadium"])
            if team["Team"] == team2:
                team_city2 = str(team["City"])
                team_stadium2 = str(team["Stadium"])
        for stadium_ in infos.stadium:
            if stadium_["Stadium"] == stadium:
                stadium_city = str(stadium_["Stadium City"])

        if team_city1 == stadium_city:
            score +=5
        if team_city2 == stadium_city:
            score +=2
        if (team_city1 == team_city2) and (stadium_city == team_city1):
            score +=10
        if (stadium == team_stadium1) and (stadium == team_stadium2):
            score +=30
        if (stadium == team_stadium1):
            score +=20
        if (stadium == team_stadium2):
            score +=10

    return score

def Selection(population):
    fitness_list = []
    for match_list in population:
        fitness = Fitness(match_list)
        fitness_list.append(fitness)
    selected = random.choices(population, k=250)
    return selected

fitness_list = []
generation = 0
while generation <= generations:
    fitness_list.append(max(population_match, key=Fitness))
    selected = Selection(population_match)

    #Crossover
    crossover = []
    for i in range(len(selected)):
        match = selected[i]
        id = random.randint(0, len(match) -1)
        stadium_match1 = match[0][2]
        stadium_match2 = match[1][2]
        stadium_match3 = match[2][2]
        stadium_match4 = match[3][2]
        crossover_matches = list(match)
        crossover_matches[0] = (match[0][0], match[0][1], stadium_match3)
        crossover_matches[1] = (match[1][0], match[1][1], stadium_match4)
        crossover_matches[2] = (match[2][0], match[2][1], stadium_match1)
        crossover_matches[3] = (match[3][0], match[3][1], stadium_match2)

        crossover_matches = tuple(crossover_matches)
        crossover.append(crossover_matches)

    #Mutation
    mutation = []
    for i in range(len(selected)):
        random_stadium = random.choice(infos.stadium)["Stadium"]
        match = selected[i]
        id = random.randint(0, len(match) -1)
        mutation_matches = list(match)
        if (match[0][2] != random_stadium) and (match[1][2] != random_stadium) and (match[2][2] != random_stadium) and (match[3][2] != random_stadium):
            mutation_matches[id] = (match[id][0], match[id][1], random_stadium)
            mutation_matches = tuple(mutation_matches)
            mutation.append(mutation_matches)

    population_match = crossover + mutation
    generation += 1

print("Matchs:\n")

best_matchs = max(fitness_list, key=Fitness)

for i in range(4):
    print(f"{best_matchs[i][0]} vs {best_matchs[i][1]} - {best_matchs[i][2]}")
print(f"Fitness Value: {Fitness(best_matchs)}")
