# Import Library
import os
# from os.path import expanduser
from qiskit import (
    IBMQ,
    QuantumRegister,
    ClassicalRegister,
    QuantumCircuit,
    BasicAer,
    execute
)

# reference
# https://qiita.com/ksj555/items/1a035a5aead8486d30a8

# Login IBMququantum
#token_path = os.environ["HOME"]+"/"+".IBMQ_token.txt"
token_path = "../IBMQ_token"
with open(token_path, "r") as file:
    token = file.read()
IBMQ.save_account(token, overwrite=True)

def main():
    # make Old register
    cr0 = ClassicalRegister(1)

    cr1 = ClassicalRegister(1)

    cr2 = ClassicalRegister(1)

    # make basic circuit
    circ = QuantumCircuit(QuantumRegister(3), cr0, cr1, cr2)

    # show circuit
    circ.draw(output="mpl",filename="./circuit1.png")

    # make circuit for tereportation
    circ.h(0)
    circ.h(1)
    circ.cx(1,2)
    circ.cx(0,1)
    circ.h(0)

    # make circuit for measure
    circ.barrier(range(3))
    circ.measure(0, 0)
    circ.measure(1,1)
    circ.z(2).c_if(cr0, 1)
    circ.x(2).c_if(cr1, 1)
    circ.measure(2, 2)

    # show circuit
    circ.draw(output="mpl",filename="./circuit2.png")

    # do 4096 simulation
    backend = BasicAer.get_backend('qasm_simulator')
    shots = 4096
    job = execute(circ, backend=backend, shots=shots)

    ##################################################
    ################## Print result ##################
    ##################################################
    result = job.result()
    result_dict = result.get_counts(circ)
    ########## Export result ##########
    with open("result.ssv", "w") as file:
        file.write("# qubit probability\n")
        for i in result_dict:
            file.write("{0} {1:.8E}\n".format(i, result_dict[i]/shots))




if __name__=="__main__":
    main()
