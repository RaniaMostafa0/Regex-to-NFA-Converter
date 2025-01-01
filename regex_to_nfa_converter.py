import graphviz
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

states = 0

def checkformat(y):
    if (y < 48 or y > 57) and (y < 97 or y > 122) and (y < 65 or y > 90):
        return False
    return True

def get_pre(ch):
    if ch in ['+', '*']:
        return 1
    elif ch in ['.']:
        return 2
    elif ch in ['(']:
        return 3
    else:
        return 0

def shunt(x):
    stack = []
    outstring = ""
    for i in x:
        ch = i
        if checkformat(ord(ch)):
            outstring = outstring + ch
        elif ch == '(':
            stack.insert(len(stack), ch)
        elif ch == ')':
            while len(stack) > 0 and stack[len(stack) - 1] != '(':
                outstring = outstring + stack[len(stack) - 1]
                stack.pop(len(stack) - 1)
            stack.pop(len(stack) - 1)
        else:
            while len(stack) > 0 and get_pre(ch) >= get_pre(stack[len(stack) - 1]):
                outstring = outstring + stack[len(stack) - 1]
                stack.pop(len(stack) - 1)
            stack.insert(len(stack), ch)
    while len(stack) > 0:
        outstring = outstring + stack[len(stack) - 1]
        stack.pop(len(stack) - 1)
    return outstring

def pars_str(x):
    res = []
    if len(x) > 1:
        for i in range(len(x) - 1):
            res.append(x[i])
            if (checkformat(ord(x[i])) and checkformat(ord(x[i + 1]))) or (x[i] == ')' and x[i + 1] == '('):
                res.append('.')
            elif checkformat(ord(x[i + 1])) and (x[i] == ')' or x[i] == '*' or x[i] == '+'):
                res.append('.')
            elif x[i + 1] == '(' and (checkformat(ord(x[i])) or x[i] == '*' or x[i] == '+'):
                res.append('.')
        if len(x) > 0:
            check = x[len(x) - 1]
            if check != res[len(res) - 1]:
                res.append(check)
    else:
        res = list(x)
    return ''.join(res)


def NFA_sym(ch):
    global letters
    letters.update(set({ch}))
    global states
    val = ["Q{}".format(states), ch, "Q{}".format(states + 1)]
    nfa["transition_function"].insert(len(nfa["transition_function"]), val)
    states = states + 2
    ret = list(["Q{}".format(states - 2), "Q{}".format(states - 1)])
    return ret

def nfa_unio(nfa1, nfa2):
    global states
    val = ["Q{}".format(states), '$', nfa1[0]]
    nfa["transition_function"].insert(len(nfa["transition_function"]), val)
    val = ["Q{}".format(states), '$', nfa2[0]]
    nfa["transition_function"].insert(len(nfa["transition_function"]), val)
    val = [nfa1[1], '$', "Q{}".format(states + 1)]
    nfa["transition_function"].insert(len(nfa["transition_function"]), val)
    val = [nfa2[1], '$', "Q{}".format(states + 1)]
    nfa["transition_function"].insert(len(nfa["transition_function"]), val)
    states = states + 2
    return ["Q{}".format(states - 2), "Q{}".format(states - 1)]

def loop(nfa1):
    global states
    val = [nfa1[1], '$', nfa1[0]]
    nfa["transition_function"].insert(len(nfa["transition_function"]), val)
    val = ["Q{}".format(states), '$', nfa1[0]]
    nfa["transition_function"].insert(len(nfa["transition_function"]), val)
    val = [nfa1[1], '$', "Q{}".format(states + 1)]
    nfa["transition_function"].insert(len(nfa["transition_function"]), val)
    val = ["Q{}".format(states), '$', "Q{}".format(states + 1)]
    nfa["transition_function"].insert(len(nfa["transition_function"]), val)
    states = states + 2
    return ["Q{}".format(states - 2), "Q{}".format(states - 1)]

def concatenation(nfa1, nfa2):
    global states
    indx = len(nfa['transition_function'])
    val = [nfa1[1], '$', nfa2[0]]
    nfa['transition_function'].insert(indx, val)
    return [nfa1[0], nfa2[1]]

def re2nfa(x):
    stack = []
    for i in x:
        if checkformat(ord(i)):
            stack.append(NFA_sym(i))
        elif i == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            xt = nfa_unio(nfa1, nfa2)
            stack.append(xt)
        elif i == "*":
            xt = loop(stack.pop())
            stack.append(xt)
        elif i == "+":
            nfa1 = stack.pop()
            xt = concatenation(nfa1, loop(nfa1))  # Modification here
            stack.append(xt)
        else:
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            xt = concatenation(nfa1, nfa2)
            stack.append(xt)
    nfa["start_states"] = [stack[0][0]]
    nfa["final_states"] = [stack[0][1]]


letters = set({})

x = input("Enter a regular expression: ")
nfa = {}
nfa["states"] = []
nfa["letters"] = []
nfa["transition_function"] = []

x = pars_str(x)
x = shunt(x)
re2nfa(x)
s = set({})
for x in range(len(nfa["transition_function"])):
    s.update(set({nfa["transition_function"][x][0]}))
    s.update(set({nfa["transition_function"][x][2]}))

templis = list(letters)
nfa["letters"] = templis
s = list(s)
s.sort(key=lambda a: int(a[1:]))
nfa["states"] = s

print("NFA initial states:", nfa["start_states"])
print("NFA final states:", nfa["final_states"])
print("NFA letters:", nfa["letters"])
print("NFA states:", nfa["states"])
print("NFA transition function:", nfa["transition_function"])

dot = graphviz.Digraph()

for state in nfa["states"]:
    if state in nfa["start_states"]:
        dot.node(state)
    elif state in nfa["final_states"]:
        dot.node(state, shape='doublecircle')
    else:
        dot.node(state)

for transition in nfa["transition_function"]:
    dot.edge(transition[0], transition[2], label=transition[1])

dot.render('nfa', format='png', cleanup=True)
img = mpimg.imread('nfa.png')

plt.figure(figsize=(10, 8))
plt.imshow(img)
plt.axis('off')
plt.show()