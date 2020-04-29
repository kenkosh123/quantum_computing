# Import Library
import os
import fire
# from os.path import expanduser
from qiskit import (
    IBMQ,
    QuantumRegister,
    ClassicalRegister,
    QuantumCircuit,
    BasicAer,
    execute
)

# Login IBMququantum
#token_path = os.environ["HOME"]+"/"+".IBMQ_token.txt"
token_path = "../IBMQ_token"
with open(token_path, "r") as file:
    token = file.read()
IBMQ.save_account(token, overwrite=True)


def carry(circ, qr_1, qr_2, a, i):
    circ.ccx(qr_1[i], qr_2[i], a[i+1])
    circ.cx(qr_1[i], qr_2[i])
    circ.ccx(a[i], qr_2[i], a[i+1])

def icarry(circ, qr_1, qr_2, a, i):
    circ.ccx(a[i], qr_2[i], a[i+1])
    circ.cx(qr_1[i], qr_2[i])
    circ.ccx(qr_1[i], qr_2[i], a[i+1])

def sum(circ, ctl_1, ctl_2, tgt):
    circ.cx(ctl_1, tgt)
    circ.cx(ctl_2, tgt)

def isum(circ, ctl_1, ctl_2, tgt):
    # sum = isum
    circ.cx(ctl_2, tgt)
    circ.cx(ctl_1, tgt)

def adder(circ, a, b, c, n):
    #--- |a>|b> -> |a>|a+b>
    for i in range(n):
        carry(circ, a, b, c, i)
    circ.cx(a[n-1], b[n-1])
    sum(circ, c[n-1], a[n-1], b[n-1])
    for j in range(n-2, -1, -1):
        icarry(circ, a, b, c, j)
        sum(circ, c[j], a[j], b[j])

def subtractor(circ, a, b, c, n):
    #--- |a>|b> -> |a>|a-b>
    for i in range(n-1):
        isum(circ, c[i], a[i], b[i])
        carry(circ, a, b, c, i)
    isum(circ, c[n-1], a[n-1], b[n-1])
    circ.cx(a[n-1], b[n-1])
    for j in range(n-1, -1, -1):
        icarry(circ, a, b, c, j)



def modulo_adder(a, b, N):
    # store inputs a & b
    input_1 = [a, int(len(bin(a)[2:]))]
    input_2 = [b, int(len(bin(b)[2:]))]
    input_3 = [N, int(len(bin(N)[2:]))]
    print(input_1, input_2, input_3)

    #--- decide number of qubit
    qb = max(input_1[1], input_2[1], input_3[1])

    # set backend
    backend = BasicAer.get_backend('qasm_simulator')

    #--- make register
    aq = QuantumRegister(qb)
    bq = QuantumRegister(qb)
    cq = QuantumRegister(qb+1)
    nq = QuantumRegister(qb)
    nq_spare = QuantumRegister(qb)
    tq = QuantumRegister(1)
    cc = ClassicalRegister(qb+1)
    qcirc = QuantumCircuit(aq, bq, cq, nq, nq_spare, tq, cc)

    #--------------
    #--- initialization
    #--------------
    # reflect input a to register
    for i in range(input_1[1]):
        if (1 << i) & input_1[0]:
            qcirc.x(aq[i])

    # reflect input b to register
    for i in range(input_2[1]):
        if (1 << i) & input_2[0]:
            qcirc.x(bq[i])

    # reflect input N to register
    for i in range(input_3[1]):
        if (1 << i) & input_3[0]:
            qcirc.x(nq[i])
            qcirc.x(nq_spare[i])

    #--------------
    #--- caliculation
    #--------------
    #--- Adder
    adder(qcirc, aq, bq, cq, qb)
    #--- Swap (a, N)
    for i in range(qb):
        qcirc.swap(aq[i], nq[i])
    #--- Substractor
    subtractor(qcirc, aq, bq, cq, qb)
    #--- Overflow
    qcirc.x(cq[qb])
    qcirc.cx(cq[qb], tq[0])
    qcirc.x(cq[qb])
    #--- Arrow Gate
    for i in range(input_3[1]):
        if (1 << i) & input_3[0]:
            qcirc.ccx(tq[0], nq_spare[i], aq[i])
    #--- Adder (result in modulo adder)
    adder(qcirc, aq, bq, cq, qb)
    #--------------
    #--- post procedure
    #--------------
    # Arrow
    for i in range(input_3[1]):
        if (1 << i) & input_3[0]:
            qcirc.ccx(tq[0], nq_spare[i], aq[i])
    # Swap (a, N)
    for i in range(qb):
        qcirc.swap(aq[i], nq[i]) 
    # Subtractor
    subtractor(qcirc, aq, bq, cq, qb)
    # Reset tq
    qcirc.cx(cq[qb], tq[0])
    # Adder
    adder(qcirc, aq, bq, cq, qb)

    #--- Measure
    for i in range(qb):
        qcirc.measure(bq[i], cc[i])
    #--- Overflow
    qcirc.measure(cq[qb], cc[qb])

    # Start Simulation
    job = execute(qcirc, backend=backend, shots=1)
    result = job.result()
    result_dict = result.get_counts(qcirc)
    print(result_dict)
   


if __name__ == '__main__':
     fire.Fire()