from pulp import *
import tsplib95
import time
import networkx as nx


def solve(problem, timeLimit):

    G = problem.get_graph()
    n = len(G.nodes)
    addedCuts = 0

    # Solution of the relaxation and set of subcycles in this solution
    cycle = []
    S = []

    # Trivial subtours with 2 vertices (i->j->i)
    for e in itertools.combinations(list(range(1, n + 1)), 1):
        S.append(e)

    # Relaxed problem (without subtour constraints)
    prob = LpProblem("TSP", LpMinimize)
    succ = LpVariable.matrix("succ", (G.nodes, G.nodes), 0, 1, LpBinary)
    # One successor and one predecessor per vertex
    for i in G.nodes:
        prob += lpSum(succ[i - 1][j - 1] for j in G.nodes) == 1
    for j in G.nodes:
        prob += lpSum(succ[i - 1][j - 1] for i in G.nodes) == 1

    prob += (lpSum([succ[i - 1][j - 1] * G[i][j]["weight"] for j in G.nodes for i in G.nodes]),"obj",)

    start = time.time()

    # Run loop while relaxed solution contains subtours
    while len(cycle) != 1:

        # Breaks if the limit of solving time is reached
        if time.time() - start > timeLimit:
            return ("Max time reached", None, None, timeLimit, None)

        # Add cuts for subtours countained in the previous solution of the relaxation
        for e in S:
            prob += lpSum(succ[i - 1][j - 1] for i in e for j in e) <= len(e) - 1
            addedCuts += 1
            del e

        # Solve the problem with the new constraints
        prob.solve(GUROBI(msg=0))

        print("Status:", LpStatus[prob.status],"|", "Cuts added :",addedCuts, "|", "Lower bound value :", prob.objective.value(),)

        # Recover edges of the solution path in a "readable" form
        edges = []
        for i in G.nodes:
            for j in G.nodes:
                if succ[i - 1][j - 1].varValue > 0:
                    edges.append((i, j))

        # Find subtours in the solution of the relaxation
        G2 = nx.DiGraph(edges)
        cycle = [n for n in nx.simple_cycles(G2)]

        # Add the subtours on which we will add constraints
        S = []
        for i in range(len(cycle)):
            S.append([cycle[i][j] for j in range(len(cycle[i]))])

    end = time.time()

    return LpStatus[prob.status], prob.objective.value(), cycle, end - start, addedCuts


def cuttingplanes(filename, timeLimit):

    problem = tsplib95.load_problem(filename)

    print("----------------------------------------------------------------------------------")
    print("Problem :", problem.comment)
    print("----------------------------------------------------------------------------------")

    status, optimal_value, optimal_path, solvingTime, addedCuts = solve(problem, timeLimit)

    print("----------------------------------------------------------------------------------")
    
    print("Problem :", problem.comment,"\nNumber of cities :", len(list(problem.get_nodes())),"\nMethod : Cutting planes\nStatus :", status)
    if status == "Optimal":
        print("Optimal value :", round(optimal_value),"\nOptimal tour :", optimal_path[0],"\nSolving time :", solvingTime,"\nCuts added :", addedCuts)
    
    print("----------------------------------------------------------------------------------")


# --------------------------------------------------------------------------- #

if len(sys.argv) == 3:
    if not os.path.isfile(sys.argv[1]):
        print("file .tsp do not exist ")
    else:
        cuttingplanes(sys.argv[1], float(sys.argv[2]))
