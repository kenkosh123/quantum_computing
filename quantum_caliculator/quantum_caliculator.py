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

def adder(circ, a, b, c, n):
    for i in range(n):
        carry(circ, a, b, c, i)
    circ.cx(a[n-1], b[n-1])
    sum(circ, c[n-1], a[n-1], b[n-1])
    for j in range(n-2, -1, -1):
        icarry(circ, a, b, c, j)
        sum(circ, c[j], a[j], b[j])




def plain_adder(a, b):
    #--- store inputs a & b
    input_1 = [a, int(len(bin(a)[2:]))]
    input_2 = [b, int(len(bin(b)[2:]))]
    print(input_1, input_2)

    #--- decide number of qubit
    qb = max(input_1[1], input_2[1])

    # set backend
    backend = BasicAer.get_backend('qasm_simulator')

    #--- make register
    aq = QuantumRegister(qb)
    bq = QuantumRegister(qb)
    cq = QuantumRegister(qb+1)
    cc = ClassicalRegister(qb+1)
    qcirc = QuantumCircuit(aq, bq, cq, cc)

    #--- initialization
    # reflect input a to register
    for i in range(input_1[1]):
        if (1 << i) & input_1[0]:
            qcirc.x(aq[i])

    # reflect input b to register
    for i in range(input_2[1]):
        if (1 << i) & input_2[0]:
            qcirc.x(bq[i])

    #--- Plain Adder
    adder(qcirc, aq, bq, cq, qb)

    #--- measure
    for i in range(qb):
        qcirc.measure(bq[i], cc[i])
    #--- overflow counter
    qcirc.measure(cq[qb], cc[qb])

    # Start Simulation
    job = execute(qcirc, backend=backend, shots=1)
    result = job.result()
    result_dict = result.get_counts(qcirc)
    print(result_dict)

if __name__ == '__main__':
     fire.Fire()