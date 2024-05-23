import random

def updatePlayersFile(updated_players):
    with open("Players.txt", "r") as file:
        existing_player_lines = file.readlines()

    for i, (player, rating) in enumerate(updated_players):
        for j, line in enumerate(existing_player_lines):
            if player in line:
                player_number = line.split(". ")[0]
                updated_line = f"{player_number}. {player}, {rating}\n"
                existing_player_lines[j] = updated_line
                break

    with open("Players.txt", "w") as file:
        file.writelines(existing_player_lines)
        
    return 1

def updateElo(team1, team2, winner, underdog, undergain, underloss, uppergain, upperloss):
    team1 = [tuple(player.split()) for player in team1.split(',')]
    team2 = [tuple(player.split()) for player in team2.split(',')]

    updated_players = []

    if winner == 1:  # Team 1 is the winner
        for player, rating in team1:
            rating = int(rating)
            if underdog == 1:  # Team 1 is the underdog
                rating += undergain
            else:
                rating += uppergain
            updated_players.append((player, rating))

        for player, rating in team2:
            rating = int(rating)
            if underdog == 2:  # Team 2 is the underdog
                rating -= underloss
            else:
                rating -= upperloss
            updated_players.append((player, rating))
    elif winner == 2:  # Team 2 is the winner
        for player, rating in team1:
            rating = int(rating)
            if underdog == 1:  # Team 1 is the underdog
                rating -= underloss
            else:
                rating -= upperloss
            updated_players.append((player, rating))

        for player, rating in team2:
            rating = int(rating)
            if underdog == 2:  # Team 2 is the underdog
                rating += undergain
            else:
                rating += uppergain
            updated_players.append((player, rating))

    return updated_players

#read the file and format selected players
def readPlayers(selection, amount):
     my_file = open("Players.txt", "r")
     player = my_file.readlines()
     players = []
     for i in range(amount):
         players.append(player[selection[i] - 1])
     my_file.close()
     cleaned_list = [entry.strip('\n') for entry in players]
     cleaned_list = [entry.split('. ')[1] for entry in cleaned_list]
     return cleaned_list

#count the number of players
def countLines():
    with open("Players.txt", 'r') as fp:
        lines = len(fp.readlines())
        return lines


def randomize(lines, amount):
    options = []
    selection = []
    playerNum = 0
    
    for i in range(1, lines + 1):
        options.append(i)
    
    for i in range(amount):
        playerNum = random.randint(1, len(options))
        selection.append(options[playerNum-1])
        options.pop(playerNum-1)


    # while len(selection) < amount:
    #     playerNum = random.randint(1, lines)
    #     selection.append(playerNum)
    #     for i in range(1, len(selection)):
    #         if selection[i] == selection[i-1]:
    #             selection.pop(i-1)
            

    # for i in range(amount):
    #     playerNum = random.randint(1, lines)
    #     selection.append(playerNum)
    
    return selection
    


#create a tuple with name and rating
def getPlayers(player):
    paired = []
    for pair in player:
        members, rating_str = pair.split(', ')
        rating = int(rating_str)
        paired.append((members, rating))
    return paired

def selectionSort(arr):
    for i in range(len(arr) - 1):
        minIndex = i
        for j in range(i + 1, len(arr)):
            if arr[minIndex][1] > arr[j][1]:
                minIndex = j

        arr[i], arr[minIndex] = arr[minIndex], arr[i]
    return arr


def formatTeams(players):
    player_ratings = {f"{player} {rating}" for player, rating in players}
    formatted_players = ",  ".join(player_ratings)
    return formatted_players

def balance(tuple):
    team1 = []
    team2 = []

    team1.append(tuple[0])

    for i in range(1, len(tuple)):

        avg1 = sum(t[1] for t in team1) / len(team1) 
        avg2 = sum(t[1] for t in team2) / len(team2) if len(team2) > 0 else float('inf')

        new_avg1 = (sum(p[1] for p in team1) + tuple[i][1]) / (len(tuple) + 1)
        new_avg2 = sum(p[1] for p in team2) / len(team2) if len(team2) > 0 else float('inf')

        if abs(new_avg1 - avg2) < abs(avg1 - new_avg2):
            team1.append(tuple[i])
        else:
            team2.append(tuple[i])

        if len(team1) - len(team2) > 1:
            team2.append(team2.pop())
        elif len(team2) - len(team1) > 1:
            team1.append(team2.pop())

    return team1, team2

def average(team):
    avg = 0
    sum = 0
    count = 0
    for _, rating in team:
        sum += rating
        count +=1
        
    avg = sum / count
    
    return avg

def underDog(averageFirst, averageSecond):
    underdog = 0
    dif = abs(averageFirst - averageSecond)
    elo_dif = int(dif / 25)
    undergain = 25 + elo_dif
    underloss = 25 - elo_dif
    uppergain = 25 - elo_dif
    upperloss = 25 + elo_dif
    if undergain > 50:
        undergain = 50
    if underloss > 50:
        underloss = 50
    if uppergain > 50:
        uppergain = 50
    if upperloss > 50:
        upperloss = 50
    
    if averageFirst < averageSecond:
        print("Team 1 is the underdog by", int(dif), "elo. Team 1: +", undergain, "/-", underloss, "Team2: +", uppergain, "/-", upperloss)
        underdog = 1
        return underdog, undergain, underloss, uppergain, upperloss
    elif averageSecond < averageFirst:
        print("Team 2 is the underdog by", int(dif), "elo. Team 2: +", undergain, "/-", underloss, "Team1: +", uppergain, "/-", upperloss)
        underdog = 2
        return underdog, undergain, underloss, uppergain, upperloss
    


def main():
    my_file = open("Players.txt", "r")
    print(my_file.read())
    my_file.close()

    choice = int(input("Matchmaking queue or Create your own teams?: 1 or 2: "))
    if choice == 1:
        amount = int(input("how many players total? "))
        manual = int(input("manual player input or randomize? 1 or 2: "))
        if manual == 1:
            selection = input("Which players do you want?: Ex. 5, 3, 8, 12, 15, 7, 2, 1, 15, 16 : ")
            selection = selection.split(', ')
            selection = [int(i) for i in selection]
        
            playerin = readPlayers(selection, amount)
            separated = getPlayers(playerin)
            sorted = selectionSort(separated)
            team1, team2 = balance(sorted)
            t1_avg = average(team1)
            t2_avg = average(team2)
            team1 = formatTeams(team1)
            team2 = formatTeams(team2)
            print("Team1: ", team1, "Average: ", t1_avg)
            print("Team2: ", team2, "Average: ", t2_avg)
            underdog, undergain, underloss, uppergain, upperloss = underDog(t1_avg, t2_avg)
            winner  = int(input("Which team won?"))
            updated_players = updateElo(team1, team2, winner, underdog, undergain, underloss, uppergain, upperloss)
            updatePlayersFile(updated_players)
            
         
        elif manual == 2:
            lines = countLines()
            selection = randomize(lines, amount)
            playerin = readPlayers(selection, amount)
            separated = getPlayers(playerin)
            sorted = selectionSort(separated)
            team1, team2 = balance(sorted)
            t1_avg = average(team1)
            t2_avg = average(team2)
            team1 = formatTeams(team1)
            team2 = formatTeams(team2)
            print("Team1: ", team1, "Average: ", t1_avg)
            print("Team2: ", team2, "Average: ", t2_avg)
            underdog, undergain, underloss, uppergain, upperloss = underDog(t1_avg, t2_avg)
            winner  = int(input("Which team won?"))
            updated_players = updateElo(team1, team2, winner, underdog, undergain, underloss, uppergain, upperloss)
            updatePlayersFile(updated_players)
            

    elif choice == 2:
        team_amount = int(input("How many players on each team: "))
        team1 = input("Which players are on team 1?: Ex. 5, 3, 8, 12, 15 : ")
        team1 = team1.split(', ')
        team1 = [int(i) for i in team1]
        player_team1 = readPlayers(team1, team_amount)
        split_team1 = getPlayers(player_team1)
        
        team2 = input("Which players are on team 2?: Ex. 5, 3, 8, 12, 15 : ")
        team2 = team2.split(', ')
        team2 = [int(i) for i in team2]
        player_team2 = readPlayers(team2, team_amount)
        split_team2 = getPlayers(player_team2)
        
        t1_avg = average(split_team1)
        t2_avg = average(split_team2)
        team1 = formatTeams(split_team1)
        team2 = formatTeams(split_team2)
        print("Team1: ", team1, "Average: ", t1_avg)
        print("Team2: ", team2, "Average: ", t2_avg)
        underdog, undergain, underloss, uppergain, upperloss = underDog(t1_avg, t2_avg)
        winner  = int(input("Which team won?"))
        updated_players = updateElo(team1, team2, winner, underdog, undergain, underloss, uppergain, upperloss)
        updatePlayersFile(updated_players)
        

if __name__ == "__main__":
    main()
