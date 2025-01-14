from profile.models import User

K = 32
def getExpectedScore(eloA, eloB):
    return 1 / (1 + 10 ** ((eloB - eloA) / 400))

def getNewElo(actualElo, score, expected):
    return actualElo + K * (score - expected)

def getNewEloPaired(ratings, score):
    expectedA = getExpectedScore(ratings[0], ratings[1])
    expectedB = getExpectedScore(ratings[1], ratings[0])
    ratings[0] = getNewElo(ratings[0], score[0], expectedA)
    ratings[1] = getNewElo(ratings[1], score[1], expectedB)

def connect4(ratings, score):
    if score == [1,1]:
        score = [0.5, 0.5]
    elif score == [0,0]:
        return
    getNewEloPaired(ratings, score)

def pong2P(ratings, score):
    if score[0] == 10:
        score = [1, 0]
    elif score[1] == 10:
        score = [0, 1]
    else:
        return
    getNewEloPaired(ratings, score)

def pong4P(ratings, placements):
    scores = [1.0 - 0.25 * (rank - 1) for rank in placements]
    new_ratings = []

    for i in range(len(ratings)):
        for j in range(len(ratings)):
            if i != j:
                expectedScore = getExpectedScore(ratings[i], ratings[j])
                score = 1 if placements[i] < placements[j] else 0
                if placements[i] == placements[j]:
                    score = 0.5
                new_ratings.append(getNewElo(ratings[i], score, expectedScore))
    ratings = new_ratings
    return new_ratings


def getElos(players, gameType):
    elos = []
    for player in players:
        if gameType == False:
            elos.append(User.objects.filter(pk=player).values_list("eloPong", flat=True).first())
        else:
            elos.append(User.objects.filter(pk=player).values_list("eloConnect", flat=True).first())
    return elos

def saveElos(players, ratings, gameType):
    for i in range(len(players)):
        if gameType == False:
            User.objects.filter(pk=players[i]).update(eloPong=ratings[i])
        else:
            User.objects.filter(pk=players[i]).update(eloConnect=ratings[i])

def elo(game):
    ratings = getElos(game["players"], game["gameType"])
    if game["gameType"] == False:
        if game["maxPlayers"] == 4:
            pong4P(ratings, game["score"])
        elif game["gameType"] == 2:
            pong2P(ratings, game["score"])
    else:
        connect4(ratings, game["score"])
    saveElos(game["players"], ratings, game["gameType"])
    return