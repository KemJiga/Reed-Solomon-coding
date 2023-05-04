import itertools
import numpy as np

def chkList(lst):
    return len(set(lst)) == 1

def filter_matrix(codeword:list):
    if chkList(codeword) == True:
        return False
    else:
        return True

def generate_matrix(code:list, k:int):
    matrix = []
    aux = code.copy()
    found = 0
    i = 0
    while found < k:
        val = filter_matrix(aux[i])
        if val:
            matrix.append(aux[i])
            aux.pop(i)
            found += 1
        i += 1
    return matrix, aux

def verify_gen(gen:list, matrix:list, code:list, q:int):
    g = []
    to_verify = []

    vv = []
    for i in range(len(gen)):
        row = []
        f = gen[i]
        for c in f:
            row.append(int(c))
        g.append(row) 
    
    g = np.array(g)
    #np.transpose(g)
    g = np.reshape(g, (3,2))

    for codeword in matrix:
        #print(g)
        codeword = np.array(codeword)
        codeword = np.reshape(codeword, (2,1))
        #print(codeword, '\n')

        newc = np.dot(g, codeword)
        newc = np.reshape(newc, (1,3))
        to_verify.append(newc.tolist())
    for v in to_verify:
        for v1 in v:
            vv.append(v1)
    
    str_code = []
    for bit in vv:
        line = ''
        for n in bit:
            n = n%q
            line += str(n)
        str_code.append(line)

    print(str_code)
    print(code)
    print(str_code==code)

def get_space(s:int, length:int):
    space_units = []
    space = []
    for i in range(s):
        space.append(i)

    for i in range(s):
        trivial = []
        for j in range(length):
            trivial.append(i)
        space_units.append(trivial)

    for subset in itertools.permutations(space, length):
        if len(subset) >= length:
            space_units.append(list(subset))

    return space_units


def evaluate_pol(pol:list, x:int, dim:int):
    max_grade = len(pol)
    r = 0
    for grade in range(max_grade):
        coeficiente = pol[grade]
        r += (x**grade)*coeficiente
    return r%dim


def reed_solomon(A, q):
    pairs = []
    for L in range(len(A)):
        for subset in itertools.permutations(A, L):
            if len(subset) >= 2:
                pairs.append(list(subset))

        triviales = []    
        for j in range(len(A)-1):
            triviales.append(L)
        pairs.append(triviales)

    
    C = []
    for p in pairs:
        word = ''
        for el in A:
            bit = evaluate_pol(pol=p, x=el, dim=q)
            word += str(bit)
        C.append(word)

    generadora, generadora_aux = generate_matrix(C, 2) 

    space = get_space(3,2)
    #print(space)
    verify_gen(['111', '012'], space, C, q)


reed_solomon([0,1,2], 3)