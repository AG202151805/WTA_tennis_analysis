
def main():
    pass

import csv
import math
import glob

# Importing the files:

data_full = glob.glob("../WTA_tennis_project/tennis_cvs_files/" + "/*.csv")
data_full.sort()
data_full

tennis_all = []
for file in data_full:
    with open(file) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            tennis_all.append(row)

tennis_2007_2021 = [tennis_all[0]]

for row in tennis_all:
    if row[0] != 'Tournament':
        tennis_2007_2021.append(row)


# Adding a demi line in the end of the dataset to avoid index error issues in future operations

tennis_2007_2021.append(['end', 'of', 'dataset', 'demi', 'line', 'to', 'avoid', 'index', 'issues', 'in', 'later', 'procedures' ])


# The first function will define the winner in each match. The function will insert the winners and the losers
# to a new list, line by line. The winner will always show first and the loser second. We also add the name of the
# tournament and the start date for next steps, as well as two fields in the end - the first for the round name,
# and the second for the round number of the tournamnet

def winners(ls, ls2, i):
    """The function takes from the main dataset(tennis_2007_2021, argument ls) each line at a time and determines the winner,
    then inserts the field (tournament, date, winner, loser) to a new list (ls2)
    """

    ls2 = []

    # we first start with the situations in which one of the players retired, and so we know that the other player won
    # Also replacing specific characters in the names that caused duplications of some of the players

    if str(ls[i][4]) in str(ls[i][11]):
        ls2.extend([ls[i][0], ls[i][1], str(ls[i][5]).replace('. ', '.'), str(ls[i][4]).replace('. ', '.'), 0, -1])

    elif str(ls[i][5]) in str(ls[i][11]):
        ls2.extend([ls[i][0], ls[i][1], str(ls[i][4]).replace('. ', '.'),  str(ls[i][5]).replace('. ', '.'), 0, -1])

# There are a few games in which the length of a line is 13 (and not 12). This happened in 5 games of Maria Sharapova,
#  which the M. of her first name is in a separate index from her last name (either indices 4 and 5 or indices 5 and 6).
# There is also a " after the M. so we will remove it as well to have the same naming convention.
# We first deal with these games, and will merge her first and last name to be together (in the same index):

    elif len(ls[i]) == 13:

    # if index 11 is not empty (the index of the third game in the best of 3), we check which player had a higher number
    # in that game, and that way we can determine the winner

        if ls[i][11] != '':
            if str(ls[i][11][0]) > str(ls[i][11][2]):
                ls2.extend([ls[i][0], ls[i][1], str(ls[i][4]).replace('. ', '.'),  str(ls[i][5] + ls[i][6])
                .replace('"',''), 0, -1])
            else:
                ls2.extend([ls[i][0], ls[i][1], str(ls[i][5] + ls[i][6]).replace('"',''),  str(ls[i][4])
                .replace('. ', '.'), 0, -1])

    # if index 11 is empty, this means a player won in two games (so she won 2-0), and so we check the score
    # in both indices (9 and 10) and see if a player had a higher number in both of them, she won. Otherwises, the
    # other player won:

        elif ls[i][11] == '':
            if str(ls[i][9][0]) > str(ls[i][9][2]) and str(ls[i][10][0]) > str(ls[i][10][2]):
                ls2.extend([ls[i][0], ls[i][1], str(ls[i][4] + ls[i][5]).replace('"',''),  str(ls[i][6])
                .replace('. ', '.'), 0, -1])
            else:
                ls2.extend([ls[i][0], ls[i][1],str(ls[i][6]).replace('. ', '.'), str(ls[i][4] + ls[i][5])
                .replace('"',''), 0, -1])

# We can now do the same for the rest of the games, only for those that have a length of 12 and therefore it's for one index before:

    elif ls[i][10] != '':
        if str(ls[i][10][0]) > str(ls[i][10][2]):
            ls2.extend([ls[i][0], ls[i][1], str(ls[i][4]).replace('. ', '.'), str(ls[i][5]).replace('. ', '.'), 0, -1])
        else:
            ls2.extend([ls[i][0], ls[i][1], str(ls[i][5]).replace('. ', '.'), str(ls[i][4]).replace('. ', '.'), 0, -1])
    elif ls[i][10] == '':
        if str(ls[i][8][0]) > str(ls[i][8][2]) and str(ls[i][9][0]) > str(ls[i][9][2]):
            ls2.extend([ls[i][0], ls[i][1], str(ls[i][4]).replace('. ', '.'), str(ls[i][5]).replace('. ', '.'), 0, -1])
        else:
            ls2.extend([ls[i][0], ls[i][1], str(ls[i][5]).replace('. ', '.'), str(ls[i][4]).replace('. ', '.'), 0, -1])

    return ls2

# Next we write a function that determines the number of games played in each tournament

def get_length(ls):
    """checks the number of games in each tournament, each time a tournament name changes it starts the count from 0
    """

    count_lengths = []
    c = 0
    for i in range(len(ls)):
        try:
            if ls[i][0] != ls[i+1][0]:
                count_lengths.append(c)
                c = 0
            c+=1
        except IndexError:
            continue

    return count_lengths


def tournament_per_format(ls):
    """Creates a dictionary with the amount of tournaments per format
    """
    counts = {}
    for n in ls:
        counts[n] = counts.get(n, 0) + 1
    dic_count_desc = dict(reversed(sorted(counts.items(), key=lambda item: item[1])))
    return dic_count_desc

# We create a list with the names of the round robin tournaments to identify them later

round_robin_tours = ['Commonwealth Bank Tournament of Champions', 'Qatar Airways Tournament of Champions Sofia',
              'Sony Ericsson Championships', 'Garanti Koza WTA Tournament of Champions', 'BNP Paribas WTA Finals',
              'WTA Elite Trophy', 'WTA Finals']

# We now write the functions for each format of the tournaments, which is defined by the number of games in each tournament.
## We add in each format the name of the round and the number of the round as two separate fields

def rounds_knockout(ls2, num_of_games, line):
    """Takes 3 arguments - the list to which we insert each game, the number of games
    in the tournament and the line to which the round name and number should be added. Since there are a few tournaments
    with a base of log2 minus 1 games (31, 63 and 127) we can run the same function for them, while the number of num_of_games
    determines what format it is.
    """

    num_of_rounds = math.log2(num_of_games)

    for i in range(1, int(num_of_rounds - 2)):

        num_of_games = num_of_games/2
        for j in range(1, int(num_of_games + 1)):
            ls2[line][4] = i
            ls2[line][5] = i
            line += 1

    for k in range(1, 5):
        ls2[line][4] = 'QF'
        ls2[line][5] = int(num_of_rounds - 2)
        line += 1

    ls2[line][4] = 'SF'
    ls2[line][5] = int(num_of_rounds - 1)
    line += 1
    ls2[line][4] = 'SF'
    ls2[line][5] = int(num_of_rounds - 1)
    line += 1
    ls2[line][4] = 'Final'
    ls2[line][5] = int(num_of_rounds)

    return ls2

def rounds_95_games(ls2, line):
    """Checks if the tournament has 95 games and inserts the rounds accordingly. Since there is only one
    type of format (95) we don't need the number of games as an argument.
    """

    num_of_rounds = 7
    for i in range(1, int(num_of_rounds - 4)):
        num_of_games = 32
        for j in range(1, int(num_of_games + 1)):
            ls2[line][4] = i
            ls2[line][5] = i
            line += 1

    for i in range(3, int(num_of_rounds - 2)):
        num_of_games = num_of_games/2
        for j in range(1, int(num_of_games + 1)):
            ls2[line][4] = i
            ls2[line][5] = i
            line += 1

    for k in range(1, 5):
        ls2[line][4] = 'QF'
        ls2[line][5] = 5
        line += 1

    ls2[line][4] = 'SF'
    ls2[line][5] = 6
    line += 1
    ls2[line][4] = 'SF'
    ls2[line][5] = 6
    line += 1
    ls2[line][4] = 'Final'
    ls2[line][5] = 7

    return ls2

def rounds_60_games(ls2, line):
    """Checks if the tournament has 60 games and inserts the rounds accordingly.
    """

    num_of_rounds = 6

    for i in range(1, int(num_of_rounds - 4)):
        num_of_games = 29
        for j in range(1, int(num_of_games + 1)):
            ls2[line][4] = i
            ls2[line][5] = i
            line += 1

    num_of_games = 32

    for i in range(2, int(num_of_rounds - 2)):
        num_of_games = num_of_games/2
        for j in range(1, int(num_of_games + 1)):
            ls2[line][4] = i
            ls2[line][5] = i
            line += 1

    for k in range(1, 5):
        ls2[line][4] = 'QF'
        ls2[line][5] = 4
        line += 1

    ls2[line][4] = 'SF'
    ls2[line][5] = 5
    line += 1
    ls2[line][4] = 'SF'
    ls2[line][5] = 5
    line += 1
    ls2[line][4] = 'Final'
    ls2[line][5] = 6

    return ls2

def rounds_59_games(ls2, line):
    """Checks if the tournament has 59 games and inserts the rounds accordingly.
    """

    num_of_games = 49
    num_of_rounds = 6

    for i in range(1, int(num_of_rounds - 3)):
        num_of_games = num_of_games/1.75
        for j in range(1, int(num_of_games + 1)):
            ls2[line][4] = i
            ls2[line][5] = i
            line += 1

    for i in range(3, int(num_of_rounds - 2)):
        num_of_games = num_of_games/2
        for j in range(1, int(num_of_games + 1)):
            ls2[line][4] = i
            ls2[line][5] = i
            line += 1

    for k in range(1, 5):
        ls2[line][4] = 'QF'
        ls2[line][5] = 4
        line += 1

    ls2[line][4] = 'SF'
    ls2[line][5] = 5
    line += 1
    ls2[line][4] = 'SF'
    ls2[line][5] = 5
    line += 1
    ls2[line][4] = 'Final'
    ls2[line][5] = 6
    return ls2

def rounds_55_games(ls2, line):
    """Checks if the tournament has 55 games and inserts the rounds accordingly.
    """

    num_of_games = 36
    num_of_rounds = 6
    for i in range(1, int(num_of_rounds - 3)):
        num_of_games = num_of_games/1.5
        for j in range(1, int(num_of_games + 1)):
            ls2[line][4] = i
            ls2[line][5] = i
            line += 1

    for i in range(3, int(num_of_rounds - 2)):
        num_of_games = num_of_games/2
        for j in range(1, int(num_of_games + 1)):
            ls2[line][4] = i
            ls2[line][5] = i
            line += 1

    for k in range(1, 5):
        ls2[line][4] = 'QF'
        ls2[line][5] = 4
        line += 1


    ls2[line][4] = 'SF'
    ls2[line][5] = 5
    line += 1
    ls2[line][4] = 'SF'
    ls2[line][5] = 5
    line += 1
    ls2[line][4] = 'Final'
    ls2[line][5] = 6

    return ls2

def rounds_54_games(ls2, line):
    """Checks if the tournament has 54 games and inserts the rounds accordingly.
    """

    num_of_rounds = 6

    for i in range(1, int(num_of_rounds - 4)):
        num_of_games = 23
        for j in range(1, int(num_of_games + 1)):
            ls2[line][4] = i
            ls2[line][5] = i
            line += 1

    num_of_games = 32

    for i in range(2, int(num_of_rounds - 2)):
        num_of_games = num_of_games/2
        for j in range(1, int(num_of_games + 1)):
            ls2[line][4] = i
            ls2[line][5] = i
            line += 1

    for k in range(1, 5):
        ls2[line][4] = 'QF'
        ls2[line][5] = 4
        line += 1

    ls2[line][4] = 'SF'
    ls2[line][5] = 5
    line += 1
    ls2[line][4] = 'SF'
    ls2[line][5] = 5
    line += 1
    ls2[line][4] = 'Final'
    ls2[line][5] = 6

    return ls2

def rounds_53_games(ls2, line):
    """Checks if the tournament has 53 games and inserts the rounds accordingly.
    """

    num_of_rounds = 6
    for i in range(1, int(num_of_rounds - 4)):
        num_of_games = 22
        for j in range(1, int(num_of_games + 1)):
            ls2[line][4] = i
            ls2[line][5] = i
            line += 1

    num_of_games = 32

    for i in range(2, int(num_of_rounds - 2)):
        num_of_games = num_of_games/2
        for j in range(1, int(num_of_games + 1)):
            ls2[line][4] = i
            ls2[line][5] = i
            line += 1

    for k in range(1, 5):
        ls2[line][4] = 'QF'
        ls2[line][5] = 4
        line += 1

    ls2[line][4] = 'SF'
    ls2[line][5] = 5
    line += 1
    ls2[line][4] = 'SF'
    ls2[line][5] = 5
    line += 1
    ls2[line][4] = 'Final'
    ls2[line][5] = 6

    return ls2

def rounds_47_games(ls2, line):
    """Checks if the tournament has 47 games and inserts the rounds accordingly.
    """

    num_of_games = 16
    num_of_rounds = 6
    for i in range(1, int(num_of_rounds - 3)):
        for j in range(1, int(num_of_games + 1)):
            ls2[line][4] = i
            ls2[line][5] = i
            line += 1

    for i in range(3, int(num_of_rounds - 2)):
        num_of_games = num_of_games/2
        for j in range(1, int(num_of_games + 1)):
            ls2[line][4] = i
            ls2[line][5] = i
            line += 1

    for k in range(1, 5):
        ls2[line][4] = 'QF'
        ls2[line][5] = 4
        line += 1

    ls2[line][4] = 'SF'
    ls2[line][5] = 5
    line += 1
    ls2[line][4] = 'SF'
    ls2[line][5] = 5
    line += 1
    ls2[line][4] = 'Final'
    ls2[line][5] = 6

    return ls2

def rounds_30_games(ls2, line):
    """Checks if the tournament has 30 games and inserts the rounds accordingly.
    """

    num_of_rounds = 5
    for i in range(1, int(num_of_rounds - 3)):
        num_of_games = 15
        for j in range(1, int(num_of_games + 1)):
            ls2[line][4] = i
            ls2[line][5] = i
            line += 1

    for i in range(2, int(num_of_rounds - 2)):
        num_of_games = 8
        for j in range(1, int(num_of_games + 1)):
            ls2[line][4] = i
            ls2[line][5] = i
            line += 1

    for k in range(1, 5):
        ls2[line][4] = 'QF'
        ls2[line][5] = 3
        line += 1

    ls2[line][4] = 'SF'
    ls2[line][5] = 4
    line += 1
    ls2[line][4] = 'SF'
    ls2[line][5] = 4
    line += 1
    ls2[line][4] = 'Final'
    ls2[line][5] = 5

    return ls2

def rounds_29_games(ls2, line):
    """Checks if the tournament has 29 games and inserts the rounds accordingly.
    """

    num_of_games = 24.5
    num_of_rounds = 5
    for i in range(1, int(num_of_rounds - 2)):
        num_of_games = num_of_games/1.75
        for j in range(1, int(num_of_games + 1)):
            ls2[line][4] = i
            ls2[line][5] = i
            line += 1

    for k in range(1, 5):
        ls2[line][4] = 'QF'
        ls2[line][5] = 3
        line += 1

    ls2[line][4] = 'SF'
    ls2[line][5] = 4
    line += 1
    ls2[line][4] = 'SF'
    ls2[line][5] = 4
    line += 1
    ls2[line][4] = 'Final'
    ls2[line][5] = 5

    return ls2

def rounds_27_games(ls2, line):
    """Checks if the tournament has 27 games and inserts the rounds accordingly.
    """

    num_of_games = 18
    num_of_rounds = 5

    for i in range(1, int(num_of_rounds - 2)):
        num_of_games = num_of_games/1.5
        for j in range(1, int(num_of_games + 1)):
            ls2[line][4] = i
            ls2[line][5] = i
            line += 1

    for k in range(1, 5):
        ls2[line][4] = 'QF'
        ls2[line][5] = 3
        line += 1

    ls2[line][4] = 'SF'
    ls2[line][5] = 4
    line += 1
    ls2[line][4] = 'SF'
    ls2[line][5] = 4
    line += 1
    ls2[line][4] = 'Final'
    ls2[line][5] = 5

    return ls2

def rounds_8_games(ls2, line):
    """Checks if the tournament has 8 games and inserts the rounds accordingly.
    """

    num_of_rounds = 4
    for i in range(1, num_of_rounds + 1):
        ls2[line][4] = 'QF'
        ls2[line][5] = 1
        line += 1

    ls2[line][4] = 'SF'
    ls2[line][5] = 2
    line += 1
    ls2[line][4] = 'SF'
    ls2[line][5] = 2
    line += 1
    ls2[line][4] = 'Third Place'
    ls2[line][5] = 3
    line += 1
    ls2[line][4] = 'Final'
    ls2[line][5] = 3

    return ls2

def rounds_round_robin(ls2, line):
    """Checks if the tournament has 15 games (round robin format) and inserts the rounds accordingly.
    """
    num_of_rounds = 3
    num_of_games = 15
    for i in range(1, num_of_games - 2):
        ls2[line][4] = 'Round Robin'
        ls2[line][5] = 1
        line += 1

    ls2[line][4] = 'SF'
    ls2[line][5] = 2
    line += 1
    ls2[line][4] = 'SF'
    ls2[line][5] = 2
    line += 1
    ls2[line][4] = 'Final'
    ls2[line][5] = 3

    return ls2

def rounds_15_games(ls2, line):
    """Checks if the tournament has 15 games (knockout format) and inserts the rounds accordingly.
    """

    num_of_games = 16
    num_of_rounds = math.log2(num_of_games)
    for i in range(1, int(num_of_rounds - 2)):
        num_of_games = num_of_games/2
        for j in range(1, int(num_of_games + 1)):
            ls2[line][4] = i
            ls2[line][5] = i
            line += 1

    for k in range(1, 5):
        ls2[line][4] = 'QF'
        ls2[line][5] = 2
        line += 1

    ls2[line][4] = 'SF'
    ls2[line][5] = 3
    line += 1
    ls2[line][4] = 'SF'
    ls2[line][5] = 3
    line += 1
    ls2[line][4] = 'Final'
    ls2[line][5] = 4

    return ls2

# Writing the main function that will call all the rounds functions

def round_numbering_functions(ls2, num_of_games, line):
    """Calls the relevant functions from the rounds functions above for each tournament.
    """

    if num_of_games != 16:

        if num_of_games == 32 or num_of_games == 64 or num_of_games == 128:

            rounds_knockout(ls2, num_of_games, line)


        if num_of_games == 96:

            rounds_95_games(ls2, line)


        if num_of_games == 61:

            rounds_60_games(ls2, line)


        if num_of_games == 60:

            rounds_59_games(ls2, line)


        if num_of_games == 56:

            rounds_55_games(ls2, line)


        if num_of_games == 55:

            rounds_54_games(ls2, line)


        if num_of_games == 54:

            rounds_53_games(ls2, line)


        if num_of_games == 48:

            rounds_47_games(ls2, line)


        if num_of_games == 31:

            rounds_30_games(ls2, line)


        if num_of_games == 30:

            rounds_29_games(ls2, line)


        if num_of_games == 28:

            rounds_27_games(ls2, line)


        if num_of_games == 9:

            rounds_8_games(ls2, line)

    if num_of_games == 16:

        if ls2[line][0] in round_robin_tours:

            rounds_round_robin(ls2, line)

        else:

            rounds_15_games(ls2, line)

    return ls2


# Now we run the functions line by line and create a new list with the tournament, date, winner, loser and round of each game:

line = 0
winners_rounds = []
try:
    while line < len(tennis_2007_2021):
        tournament_name = tennis_2007_2021[line][0]
        c = 1
        while tennis_2007_2021[line][0] == tournament_name:
            winners_rounds.append(winners(tennis_2007_2021, winners_rounds, line))
            c += 1
            line += 1

        round_numbering_functions(winners_rounds, c, line-c + 1)

except IndexError:
    pass

# Around 1% of the data that wasn't sorted to rounds because of split data in the beginning and end of
# some of the fiels. We will fetch them and hardcode them:

missing_rounds = []

for i in winners_rounds[1::]:
    if i[4] == 0:
        missing_rounds.append(i)


# We can use itemgetter to sort the list by the names of the tournaments

from operator import itemgetter

missing_round_sorted = sorted(missing_rounds, key=itemgetter(0))

# Writing a function to count the number of games per tournament and know what kind of format it is:

def count_item(ls, j):

    counter = []
    for i in ls:
        if i[0] == j:
            counter.append(i)

    return len(counter)


# example - count_item(ls, 'ASB Classic')

# Now that we have the tournaments sorted, we can run for each the fitting rounds function,
# coresponding to the indices of the games:

for i in missing_round_sorted:

    if i[0] == 'ASB Classic':
        rounds_knockout(missing_round_sorted, 32, 0)
        rounds_knockout(missing_round_sorted, 32, 31)
        rounds_knockout(missing_round_sorted, 32, 62)
        rounds_knockout(missing_round_sorted, 32, 95)

    if i[0] == 'Brisbane International':
        rounds_29_games(missing_round_sorted, 140)
        rounds_29_games(missing_round_sorted, 169)
        rounds_29_games(missing_round_sorted, 198)

    if i[0] == "Mondial Australian Women's Hardcourts":
        rounds_knockout(missing_round_sorted, 32, 227)

    if i[0] == "Shenzhen Longgang Gemdale Open":
        rounds_knockout(missing_round_sorted, 32, 258)

    if i[0] == "Shenzhen Open":
        rounds_knockout(missing_round_sorted, 32, 289)
        rounds_knockout(missing_round_sorted, 32, 320)
        rounds_knockout(missing_round_sorted, 32, 351)

# There are still some games with no rounds, so we can just change it for them manually, after checking that these are
# the right rounds:

for i in missing_round_sorted:
    if i[4] == 0:
        i[4] = 1
        i[5] = 1

# For one tournament - 'Brisbane International' in 2012/13, the split caused some of the rows to get a function
# of another format, so we can just manually change these games from first round to second round and we're all set!

for i in winners_rounds:
    if i[0] == 'Brisbane International' and '2013-01-01' in i[1] and i[4] == 1:
        i[4] = 2
        i[5] = 2


# Writing the functions to answer the queries in question 1:

def final_winner_year(ls, tournament, year):
    """Takes three arguments - the list (dataset), name of tournament and year. Prints the winners
    in the final of the tournament. Example for arguments - (winners_rounds, 'US Open', '2015')
    """

    for i in ls:
        if i[0] == tournament and i[1][0:4] == year and i[4] == 'Final':
            print (i[2] + ' won the final')

def round_all_games(ls, rounds, year, tournament):
    """Takes 4 arguments - name of dataset, round, year and name of tournament. Prints
    all games of that round and who was the winner. Example - (winners_rounds, 4, '2015', 'French Open').
    """

    for i in ls:
        if i[0] == tournament and i[1][0:4] == year and i[4] == rounds:
            print (i[2], 'won', i[3])


def finals_appearance(ls, player):
    """Takes two arguments - the datset and the name of player. Prints in how
    many finals this player appeared. Example - finals_appearance(winners_rounds, 'Williams V.').
    """

    appear = []
    for i in ls:
        if i[2] == player and i[4] == 'Final':
            appear.append(i)
        elif i[3] == player and i[4] == 'Final':
            appear.append(i)

    print (player + ' appeared in ' + str(len(appear)) + ' finals')


def round_elimination(ls, tournament, year, player):
    """Takes 4 arguments - dataset, name of tournament, year and name of player.
    Prints in what round the player was eliminated from the tournament. In case the player
    did not particiate or won the tournament it will print those options.
    Example - (winners_rounds, 'Wimbledon', '2012', 'Peer S.')
    """

    p = []
    for i in ls:

        if i[0] == tournament and i[1][0:4] == year and i[3] == player:
            p.append(i[3])
            print(player, 'was eliminated in round', i[4], 'in', tournament, year)

        if i[0] == tournament and i[1][0:4] == year and i[2] == player and i[4] == 'Final':
            p.append(i[2])
            print(player, 'won the tournament')

    if player not in p:
        print(player, 'did not participate in the tournament')


def head_to_head(ls, player1, player2):
    """Takes 3 arguments - dataset, name of first player and name of second player.
    Prints how many times the players faced each other and how many times each one won.
    Example - (winners_rounds, 'Wozniacki C.', 'Jankovic J.')
    """

    matches = []

    for i in ls:
        if i[2] == player1 and i[3] == player2 or i[3] == player1 and i[2] == player2:
            matches.append(i[2])
    print(player1, 'and', player2, 'faced each other', matches.count(player1) + matches.count(player2), 'times')
    print(player1, 'won', matches.count(player1), 'times')
    print(player2, 'won', matches.count(player2), 'times')


if __name__ == '__main__':
    main()
