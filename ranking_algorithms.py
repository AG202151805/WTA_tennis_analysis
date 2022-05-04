
def main():
    pass


# For question 2 we create a function that will get all the winners from our dataset and will
# insert it to a dictionary, that will sort and aggregate the number of wins for each player.
# We then convert it back to a list

def winners_win(ls, year, year_2):
    """takes 3 arguments - the dataset, and the time frame we are interested in.
    If we want to run it only for one year we put the same year in both arguments. If we want for a period of time,
    say from 2012 to 2019, we will put both those years. Returns the ranked list of players.
    Returns a list of the winners ranked by their total number of wins
    """

    #  Calculating the score of each player based on their number of wins
    dic_points = {}
    for i in ls:
        if year <= i[1][0:4] <= year_2:
            for p in [[i[2],1]]:
                if p[0] in dic_points:
                    dic_points[p[0]] = dic_points[p[0]]+p[1]
                else:
                    dic_points[p[0]] = p[1]

    # After calculating the score of each player we sort and rank them from highest to lowest
    dict_winners_win = dict(reversed(sorted(dic_points.items(), key=lambda item: item[1])))
    total_winners_win_points = list(dict_winners_win.items())

    winners_win_total_ranked = [list(x) for x in enumerate(total_winners_win_points, 1)]

    return winners_win_total_ranked


# For question 3 we write a function that will run on all rounds as we defined in question one (the last index of each line -
# the number of the round). This way we can calculate the points of each player based on the round she played in.
# We calculate first the points for wins, and after that the reduced points for losses and aggregate the score


def winners_dont_lose(ls, year,year_2):
    """takes 3 arguments - the dataset, and the time frame we are interested in.
    If we want to run it only for one year we put the same year in both arguments. If we want for a period of time,
    say from 2012 to 2019, we will put both those years. Returns the ranked list of players.
    Returns a wighted list of the winners ranked by their total number of wins, losses and the round on which they won and lost
    """

    #  Calculating the score of each player based on their number of wins and the round on which they won
    dic_points = {}
    for i in ls:

        if year <= i[1][0:4] <= year_2:
            for p in [[i[2],i[5]]]:

                if p[0] in dic_points:
                    dic_points[p[0]] = dic_points[p[0]]+p[1]
                else:
                    dic_points[p[0]] = p[1]

            for p in [[i[3],i[5]]]:
                if p[0] in dic_points:
                    dic_points[p[0]] = dic_points[p[0]] -(1/i[5])
                else:
                    dic_points[p[0]] = - (p[1]/i[5])

    # After calculating the score of each player we sort and rank them from highest to lowest
    dict_winners_win = dict(reversed(sorted(dic_points.items(), key=lambda item: item[1])))
    total_winners_win_points = list(dict_winners_win.items())

    winners_win_total_ranked = [list(x) for x in enumerate(total_winners_win_points, 1)]

    return winners_win_total_ranked

# For questions 4 we write a function that ranks the players based on the players they beat, meaning if a player won a
# good player (i.e. a player with a strong win-lose ratio) she receives a higher score for it

def wbw_rank(ls, year, year_2):
    """takes 3 arguments - the dataset, and the time frame we are interested in.
    If we want to run it only for one year we put the same year in both arguments. If we want for a period of time,
    say from 2012 to 2019, we will put both those years. Returns the ranked list of players.
    Returns a weighted list with ranked players based on the oppoenents that they beat
    """

    # We start with creating a list of the names of the players, using the function winners_dont_lose (from question 3)
    # to pull out their names, in the order of their ranking:
    player_rank_name = []
    for i in winners_dont_lose(ls, year, year_2):
        player_rank_name.append(i[1][0])

    # Creating a list of the indices of each player in its order (so the first ranked player's index is 0)
    players_ranked_index = []

    for i in player_rank_name:
        players_ranked_index.append(player_rank_name.index(i))

    # Creating a list of lists that will contain the index of each player
    losers_list = []

    for i in player_rank_name:
        losers_list.append([player_rank_name.index(i)])

    # Adding to the list of lists the indices of all the players that each player lost to, with a condition
    # of years we would want to check it for
    for i in ls[1::]:
        try:
            if int(i[1][0:4]) >= int(year) and int(i[1][0:4]) <= int(year_2):
                losers_list[player_rank_name.index(i[3])].append(player_rank_name.index(i[2]))
        except ValueError:
            continue

    # Creating a similar table, but without the index of the first player (so only the winners of each player)
    losers_list_without_first_index = []

    for i in range(len(losers_list)):
        losers_list_without_first_index.append(losers_list[i][1::])

    # Counting the number of times each player lost to each one of her opponents
    count_dict = []
    for j in losers_list_without_first_index:
        count = {}
        for i in j: count[i] = count.get(i, 0) + 1
        count_dict.append(count.items())

    # Converting back to a list
    count_losers_lost = [list(x) for x in count_dict]

    # Starting the procedure of the rankings - creating two tables - one with the initial score of each player,
    # which is the same score in the beginning for each player, and the second list with 0 as the initial score for each player:

    first_table = []
    second_table = []

    for i in players_ranked_index:
        first_table.append(1/len(players_ranked_index))
        second_table.append(0)

    # Now, for each player we check how many points she needs to pass to each opponent (based on the number of games she lost),
    # we add those scores to second_table and reset the scores in first_table.
    # We update the scores and then run the same process, but flip between the tables each time.
    # Once the delta (the absoult difference between the scores in the first_table and second_table) surpasses the threshold, we
    # can say that the algorithm has converged and stop the iterations

    delta = 1
    while delta > 0.00000001:
        try:

            for i in players_ranked_index:
                sum_of_losses = 0

                for j in count_losers_lost[i]:
                    sum_of_losses = sum_of_losses + j[1] # aggregating the number of losses of each player

                atomic_unit =  first_table[i] / sum_of_losses # the score each player should receive - their current score divided by number of losses

                for j in count_losers_lost[i]:
                    # Updating and scaling the score of each player
                    second_table[j[0]] = (second_table[j[0]] + (atomic_unit * j[1]) * 0.85) + (0.15/len(players_ranked_index))

                first_table[i] = 0 # Reseting the scores in the first_table

            for i in players_ranked_index:
                sum_of_losses = 0

                for j in count_losers_lost[i]:
                    sum_of_losses = sum_of_losses + j[1] # aggregating the number of losses of each player

                atomic_unit = second_table[i] / sum_of_losses # the score each player should receive - their current score divided by number of losses

                for j in count_losers_lost[i]:
                    # Updating and scaling the score of each player
                    first_table[j[0]] = (first_table[j[0]] + (atomic_unit * j[1]) * 0.85) + (0.15/len(players_ranked_index))

                delta = abs(second_table[i] - first_table[i]) # Calculating and updating delta
                second_table[i] = 0 # Reseting the scores in the second_table


        except IndexError:
            continue

    # Once the algorithm has convereged and we have the scores of each player, we can sort and rank them based on their final scores
    ranking_wbw = []

    for i in range(len(player_rank_name)):
        try:
            ranking_wbw.append([player_rank_name[i], first_table[i]])
        except IndexError:
            continue

    dict_winners_wbw = dict(reversed(sorted(ranking_wbw, key=lambda item: item[1])))
    total_winners_wbw = list(dict_winners_wbw.items())

    wbw_total_ranked = [list(x) for x in enumerate(total_winners_wbw, 1)]

    return wbw_total_ranked


if __name__ == '__main__':
    main()
