import itertools
import numpy as np

def chkList(lst):
    return len(set(lst)) == 1

def filter_matrix(codeword:list):
    if chkList(codeword) == True:
        return False
    else:
        return True
    
def clean_matrix(m:list):
    a = []
    for c in m:
        if chkList(c) != True:
            a.append(c)
    return a    

def generate_matrix(code:list, k:int):
    space = clean_matrix(code)
    pos_gen = []
    for subset in itertools.permutations(space, k):
        if len(subset) >= k:
            pos_gen.append(list(subset))
    return pos_gen

def verify_gen(gen:list, matrix:list, code:list, q:int, n:int, k:int):
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
    g = np.reshape(g, (n,k))

    for codeword in matrix:
        codeword = np.array(codeword)
        codeword = np.reshape(codeword, (k,1))

        newc = np.dot(g, codeword)
        newc = np.reshape(newc, (1,n))
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

    compared = list(set(str_code) & set(code))
    if len(code) == len(compared):
        print('Generadora verificada con exito\n', gen)
        #print('Codigo generado con la matriz\n',str_code)
        #print('Codigo obtenido por el conjunto de polinomios\n',code)
        return True
    else:
        #print('Chale... Sigue intentando')
        return False

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


def reed_solomon(A, q, n:int, k:int):
    print('Longitud del codigo: ', n)
    print('Dimension del codigo: ', k)
    print('Distancia minima: ', str(n-k+1))
    pairs = []
    for L in range(len(A)):
        for subset in itertools.permutations(A, L):
            if len(subset) >= k:
                pairs.append(list(subset))

        triviales = []    
        for j in range(len(A)-1):
            triviales.append(L)
        pairs.append(triviales)

    print('Coeficientes del conjunto de polinomios (los exponentes son representamos por el indice del coeficiente en el vector. ej: [1,1] = 1+x):\n', pairs)

    C = []
    for p in pairs:
        word = ''
        for el in A:
            bit = evaluate_pol(pol=p, x=el, dim=q)
            word += str(bit)
        C.append(word)

    print('Codigo generado por el conjunto de polinomios: ', C)

    space = get_space(q,2)
    generadoras = generate_matrix(C, 2)

    sw = False
    while not sw:
        sw = verify_gen(generadoras[0], space, C, q, n=n, k=k)
        if not sw:
            generadoras.pop(0)
    gen = generadoras[0]


reed_solomon([0,1,2], 3, n=3, k=2)