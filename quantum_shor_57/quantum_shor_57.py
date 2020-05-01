import os
import fire
import math # for pi
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

def input_state(circ, q, n):
    for i in range(n):
        circ.h(q[i])


def rev_qreg(circ, q, n):
        for i in range(int(n/2)):
            circ.swap(q[i], q[(n-1)-i])


def iqft(circ, q, n):
    # 上位ビットから処理
    for j in range(n-1,-1,-1):
        circ.h(q[j])
        for k in reversed(range(j)):
            circ.cu1((-1)*math.pi/float(2**(j-k)), q[j], q[k])
    rev_qreg(circ, q, n)


def shor_57():
    # set backend
    backend = BasicAer.get_backend('qasm_simulator')

    q = QuantumRegister(6)
    a = QuantumRegister(7)
    c = ClassicalRegister(7)
    qcirc = QuantumCircuit(q, a, c)

    #--- initialization
    input_state(qcirc, q, 6)
    #--- set quantum oracle
    qcirc.cx(q[0], a[2])
    qcirc.cx(q[0], a[5])
    qcirc.x(a[0])
    #--- 逆量子フーリエ変換
    iqft(qcirc, q, 6)

    # show circuit
    qcirc.draw(output="mpl",filename="./qcircuit1.png")

    #--- measure
    for i in range(6):
        qcirc.measure(q[i], c[i])

    # Start Simulation
    job = execute(qcirc, backend=backend, shots=128)
    result = job.result()
    result_dict = result.get_counts(qcirc)
    print(result_dict)


if __name__ == '__main__':
     fire.Fire()