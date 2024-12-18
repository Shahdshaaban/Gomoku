from utils import scoreMap

def centerWeightedHeuristic(x, y, size):
    center = size // 2
    return size - (abs(center - x) + abs(center - y))
def evalWindow(sub, ally, opp):
    score = 0
    if f"{ally}{ally}{ally}{ally}{ally}" in sub:
        return scoreMap['5-in-row']
    # Offensive patterns
    if f"0{ally}{ally}{ally}{ally}0" in sub:
        score += scoreMap['4-open']
    elif f"0{ally}{ally}{ally}0" in sub:
        score += scoreMap['3-open']
    elif f"0{ally}{ally}0" in sub:
        score += scoreMap['2-open']
    elif f"{ally}{ally}{ally}{ally}{opp}" in sub or f"{opp}{ally}{ally}{ally}{ally}" in sub:
        score += scoreMap['4-blocked']
    elif f"{ally}{ally}{ally}" in sub:
        score += scoreMap['3-blocked']

    # Defensive patterns
    scaler = 0.8
    if f"0{opp}{opp}{opp}{opp}0" in sub:
        score -= scoreMap['4-open']
    elif f"0{opp}{opp}{opp}0" in sub:
        score -= scoreMap['3-open']
    elif f"0{opp}{opp}0" in sub:
        score -= scoreMap['2-open']
    elif f"{opp}{opp}{opp}{opp}{ally}" in sub or f"{ally}{opp}{opp}{opp}{opp}" in sub:
        score += scoreMap['4-blocked']
    elif f"{opp}{opp}{opp}" in sub:
        score += scoreMap['3-blocked']
    return score


def getDirectionScore(grid, size, x, y, dx, dy, player):
    score = 0
    sub = ""

    for i in range(-5, 6):
        newX = x + dx * i
        newY = y + dy * i
        if 0 <= newX < size and 0 <= newY < size:
            sub += str(grid[newX][newY])
    if len(sub) >= 6:
        score += evalWindow(sub, player, 3 - player)
    return score

def evaluatePosition(grid, size, isMax):
    totalScore = 0
    player = 1 if isMax else 2
    directions = [(0, 1), (1, 0), (1, 1), (-1, -1)]

    for x in range(size):
        for y in range(size):
            if grid[x][y] != 0:
                positionScore = 0
                for dx, dy in directions:
                    directionScore = getDirectionScore(grid, size, x, y, dx, dy, player)
                    positionScore += directionScore

                totalScore += positionScore
    return totalScore