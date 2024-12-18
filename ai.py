import time
from utils import gameOver, INF
from eval import evaluatePosition, centerWeightedHeuristic

def minimaxAlphaBeta(grid, size, depth, isMax, alphaBetaOn, alpha, beta, centerHeuristicOn):
    result = gameOver(grid, size)
    if depth == 0 or result != -1:
        if result == 1:
            return INF, None
        if result == 2:
            return -INF, None
        if result == 0:
            return 0, None

        return evaluatePosition(grid, size, isMax), None

    bestMove = [-1, -1]
    if isMax:
        maxScore = -INF
        for i in range(size):
            for j in range(size):
                if grid[i][j] == 0:
                    grid[i][j] = 1
                    score, _ = minimaxAlphaBeta(grid, size, depth - 1, False, alphaBetaOn, alpha, beta, centerHeuristicOn)
                    score += centerHeuristicOn * centerWeightedHeuristic(i, j, size)
                    grid[i][j] = 0
                    if score > maxScore:
                        maxScore = score
                        bestMove = [i, j]
                    alpha = max(alpha, score)
                    if alphaBetaOn and beta <= alpha:
                        break
        return maxScore, bestMove

    else:
        minScore = INF
        for i in range(size):
            for j in range(size):
                if grid[i][j] == 0:
                    grid[i][j] = 2
                    score, _ = minimaxAlphaBeta(grid, size, depth - 1, True, alphaBetaOn, alpha, beta, centerHeuristicOn)
                    score -= centerHeuristicOn * centerWeightedHeuristic(i, j, size)
                    grid[i][j] = 0
                    if score < minScore:
                        minScore = score
                        bestMove = [i, j]
                    beta = min(beta, score)
                    if alphaBetaOn and beta <= alpha:
                        break

        return minScore, bestMove

def moveAI(grid, size, depth, alphaBetaOn, centerHeuristicOn):
    start_time = time.time()
    _, move = minimaxAlphaBeta(grid, size, depth, True, alphaBetaOn, -INF, INF, centerHeuristicOn)
    print(f"AI Moved: {move}\nTime to make move: {time.time() - start_time}")
    return move
