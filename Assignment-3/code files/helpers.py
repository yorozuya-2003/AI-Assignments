# functions used in cnf calculation
def find_before_jb(x):
    x = x.replace(' ', '')

    stack = []
    temp = x[::-1][1:]

    stack.append(')')
    rIdx = 0

    for each in range(len(temp)):
        char = temp[each]
        if char == '(':
            if len(stack) == 1:
                rIdx = each+1
                break
            else:
                stack.pop()
        elif char == ')':
            stack.append(')')

    return x[:-(rIdx+1)], x[-(rIdx+1):]


def find_after_ja(x):
    x = x.replace(' ', '')

    stack = []
    temp = x[1:]

    stack.append('(')
    rIdx = 0

    for each in range(len(temp)):
        char = temp[each]
        if char == ')':
            if len(stack) == 1:
                rIdx = each+1
                break
            else:
                stack.pop()
        elif char == '(':
            stack.append('(')

    return x[(rIdx+1):], x[:(rIdx+1)]


# function for handling biconditional proposition
def handleBiconditional(expression):
    expression = expression.replace(' ', '')
    
    while '=' in expression:
        idx = expression.find('=')

        before = expression[:idx]
        after = expression[idx+1:]
        # print(before, after)

        jb = expression[idx-1]
        ja = expression[idx+1]

        fb = 0
        fa = 0

        if jb == ')':
            fb = 1
            before, jb = find_before_jb(before)

        if ja == '(':
            fa = 1
            after, ja = find_after_ja(after)

        if fb == 0:
            before = before[:-1]
        if fa == 0:
            after = after[1:]

        res = before
        res += f'(({jb}>{ja})&({ja}>{jb}))'
        res += after
        expression = res
        # print(expression)
        # print()

    return expression


# function for handling implication
def handleImplication(expression):
    expression = expression.replace(' ', '')
    
    while '>' in expression:
        idx = expression.find('>')

        before = expression[:idx]
        after = expression[idx+1:]
        # print(before, after)

        jb = expression[idx-1]
        ja = expression[idx+1]

        fb = 0
        fa = 0

        if jb == ')':
            fb = 1
            before, jb = find_before_jb(before)

        if ja == '(':
            fa = 1
            after, ja = find_after_ja(after)

        if fb == 0:
            before = before[:-1]
        if fa == 0:
            after = after[1:]

        res = before
        res += f'!{jb}|{ja}'
        res += after
        expression = res
        # print(expression)
        # print()

    return expression


# handling symbols in expression
import importlib.metadata as importlib_metadata
engletters = "a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
symletters = "𝕒 𝕓 𝕔 𝕕 𝕖 𝕗 𝕘 𝕙 𝕚 𝕛 𝕜 𝕝 𝕞 𝕟 𝕠 𝕡 𝕢 𝕣 𝕤 𝕥 𝕦 𝕧 𝕨 𝕩 𝕪 𝕫 𝔸 𝔹 ℂ 𝔻 𝔼 𝔽 𝔾 ℍ 𝕀 𝕁 𝕂 𝕃 𝕄 ℕ 𝕆 ℙ ℚ ℝ 𝕊 𝕋 𝕌 𝕍 𝕎 𝕏 𝕐 ℤ"

englist = engletters.split()
symlist = symletters.split()

engtosym = {}
symtoeng = {}

for each in range(len(englist)):
    engtosym[englist[each]] = symlist[each]
    symtoeng[symlist[each]] = englist[each]

lib = 'sympy'
symbols = {
    '|': '|',
    '&': '&',
    '!': '~',
    '>': '>>',
}

import sys, subprocess, warnings
warnings.filterwarnings("ignore")
installed = {pkg.metadata['Name'] for pkg in importlib_metadata.distributions()}
missing = {lib} - installed
if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

def expression(formula):
    res = ''
    for each in formula:
        if each in symbols:
            res += symbols[each]
        else:
            res += each
    return res


# function to convert expression to cnf
def CNF(x):
    tempx = ''
    for each in x:
        if each in englist:
            tempx += engtosym[each]
        else:
            tempx += each
    
    x = tempx
    x = handleBiconditional(x)
    x = expression(x)
    
    from sympy import to_cnf
    cnf = str(to_cnf(x))
    cnf = cnf.replace('~', '!')
    cnf = cnf.replace(' ', '')
    
    tempcnf = ''
    for each in cnf:
        if each in symlist:
            tempcnf += symtoeng[each]
        else:
            tempcnf += each
    
    return tempcnf

# functions for handling resolution
def areOpposite(x, y):
    if abs(len(x) - len(y)) == 1:
        if x[-1] == y[-1]:
            return True
        return False
    return False


def resolve(s1, s2):
    c1 = s1.split('|')
    c2 = s2.split('|')
    
    c1.sort(key=lambda x : x[-1])
    c2.sort(key=lambda x : x[-1])

    flag = 0
    r1, r2 = None, None
    for i in range(len(c1)):
        for j in range(len(c2)):
            if areOpposite(c1[i], c2[j]):
                flag = 1
                r1, r2 = c1[i], c2[j]
                break

    res = c1 + c2
    
    if not flag:
        return None
    
    res.remove(r1)
    res.remove(r2)

    res = list(set(res))
    res.sort(key=lambda x: x[-1])
    
    res_formula = ''
    for each in res:
        res_formula += each + '|'
    res_formula = res_formula[:-1]    
    
    return res_formula


# functions for constructing knowledge base
def flatten(l):
    from itertools import chain
    return list(chain(*l))


def makeKB(formulas):
    KB = []
    for f in formulas:
        KB.append(f.split('&'))
        
    KB = flatten(KB)
    
    for each in range(len(KB)):
        KB[each] = KB[each].replace('(', '').replace(')', '')
        temp = KB[each].split('|')
        temp.sort(key=lambda x: x[-1])
        tempstr = ''
        for t in temp:
            tempstr += t + '|'
        KB[each] = tempstr[:-1]
    
    return KB


# function for handling resolution-refutation as search
def get_heuristic(f):
    return len(f[-1].split('|'))


def search(kb, method='uninformed', submethod='BFS', show=False):
    from datetime import datetime
    if method=='greedy':
        submethod = 'BFS'
    starttime = datetime.now()
    successor_ds = []
    successor_ds.append({'KB': kb, 'path': [kb]})
    visited = []
    
    num_nodes = 0
    while successor_ds:
        if submethod == 'BFS': ds_top = successor_ds.pop(0)
        elif submethod == 'DFS': ds_top = successor_ds.pop()
        
        top = ds_top['KB']
        path = ds_top['path']
        
        if show: print(top)
        num_nodes += 1

        for i in range(len(top)):
            for j in range(i+1, len(top)):
                ti, tj = top[i], top[j]
                if ti+'+'+tj not in visited:
                    res = resolve(ti, tj)

                    # goal state
                    if res == '':
                        if show: print(f'{ti}, {tj} resolved to Empty Clause')
                        print(1)
                        temp = top.copy()
                        temp.append(res)
                        temp_path = path.copy()
                        temp_path.append(temp)
                        
                        endtime = datetime.now()
                        execution_time = endtime - starttime
                        
                        return {'resolvable': True,
                                'path': temp_path,
                                'number of nodes explored': num_nodes,
                                'execution time': execution_time.total_seconds() }

                    # successor state
                    elif res:
                        if res not in top:
                            # print(f'{ti}, {tj} resolved to {res}\n')
                            visited.append(ti+'+'+tj)
                            temp = top.copy()
                            temp.append(res)
                            
                            temp_path = path.copy()
                            temp_path.append(temp)
                            
                            successor_ds.append({ 'KB': temp, 'path': temp_path })
        
        if method=='greedy': successor_ds.sort(key=lambda x: get_heuristic(x['KB']))
        
    print(0)
    endtime = datetime.now()
    execution_time = endtime - starttime
    return {'resolvable': False,
            'number of nodes explored': num_nodes,
            'execution time': execution_time.total_seconds() }


# functions for handling input, dealing with different search methods and displaying the results
def provide_input():
    n, m = map(int, input('Enter values for n and m: ').split())
    formulas = []
    for _ in range(n):
        f = input('Enter formula to be added to the knowlege base: ')
        formulas.append(f)
    query = input('Enter the query: ')
    
    return (n, m, formulas, query)


def solve(n, m, formulas, query, method='uninformed', submethod='BFS'):    
    cnf_formulas = [
        CNF(each) for each in formulas
    ]
    kb = makeKB(cnf_formulas)
    
    q = CNF('~(' + query + ')')
    q = makeKB([q])
    
    for each in q:
        kb.append(each)
    
    return search(kb=kb, method=method, submethod=submethod, show=(m==1))
        

def print_results(res):
    if res['resolvable']:
        print(f"total number of nodes explored: {res['number of nodes explored']}")
        print(f"execution time: {res['execution time']} seconds")
        print()
        print(f'number of nodes in the path: {len(res["path"])}')
        print(f'path:')
        for each in res['path']:
            print(each)
    else:
        print(f"total number of nodes explored: {res['number of nodes explored']}")
        print(f"execution time: {res['execution time']} seconds")
        print('query is not entailed by the knowledge base')
