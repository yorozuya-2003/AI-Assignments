from helpers import *

# taking input
n,m, formulas, query = provide_input()
print()

# applying search operations
print('applying uninformed search (BFS):')
res = solve(n, m, formulas, query, method='uninformed', submethod='BFS')
print()
print()

print('applying uninformed search (DFS):')
res = solve(n, m, formulas, query, method='uninformed', submethod='DFS')
print()
print()

print('applying greedy search:')
res = solve(n, m, formulas, query, method='greedy')
print()
print()