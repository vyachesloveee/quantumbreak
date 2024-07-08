import numpy as np 

#qbit states
up = np.array([1, 0])
down = np.array([0, 1])

#identity gate
def  I():
    return np.identity(2)

#pauli-X
def X():
    return np.identity(2)[..., ::-1]

#pauli-y
def Y():
    temp = [[0, -1.j], [1.j, 0]]
    return temp

#pauli-Z
def Z():
    temp = np.identity(2)
    temp[[1], [1]] = -1
    return temp

#hadamard
def H():
    return np.array([[1, 1], [1, -1]])/np.sqrt(2)

#phase
def S():
    return np.array([[1, 0], [0, 1j]])

#pi/8
def T():
    return np.array([[1, 0], [0, (1 + 1j)/np.sqrt(2)]])

#controlled not
def CX():
    temp = np.identity(4)
    temp[[2, 3]] = temp[[3, 2]]
    return temp

#controlled z
def CZ():
    temp = np.identity(4)
    temp[[3],[3]] = -1
    return temp

#swap
def SWAP():
    temp = np.identity(4)
    temp[[1, 2]] = temp[[2, 1]]
    return(temp)

#toffoli
def TOFF():
    temp = np.identity(8)
    temp[[6, 7]] = temp[[7, 6]]
    return(temp)

#применение гейтов
def apply(v, *gates):
  m = gates[0]
  gates = gates[1:]
  for gate in gates:
    m = np.kron(gate, m)
  return m.dot(v)

#коллапс волновой функции
def observe(v):
  v2 = np.absolute(v) ** 2
  c = np.random.choice(v.size, 1, p=v2)
  print('you observed the state number', c[0] + 1)
  return 

#тест
'''
a = np.kron(up, up)
a = apply(a, H(), I())
a = apply(a, H(), I())
print(a)
observe(a)
'''

a = '0 0 0'
print(a.split())