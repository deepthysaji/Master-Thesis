from qiskit import *
from qiskit.visualization import plot_histogram
import numpy as np
import math
import qiskit
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator

clause_list = [[[0,1],[2,3]],[[0,1],[4,5]],[[0,1],[6,7]],[[2,3],[4,5]],[[2,3],[8,9]],[[4,5],[10,11]],
               [[6,7],[8,9]],[[6,7],[10,11]],[[8,9],[10,11]]]
def XOR(qc, q0, q1, q2, q3, output):                                                
    qc.cx(q0, q2)
    qc.cx(q2, output)
    qc.cx(q1, q3)
    qc.cx(q3, output)
    qc.ccx(q2, q3, output)
    qc.cx(q0, q2)
    qc.cx(q1, q3)

def oracle(qc, clause_list, clause_qubits, var_qubits, output_qubit):
    for i in range(6):                                                #cast oracla dle obr. 9.3             
        qc.ccx(var_qubits[2*i], var_qubits[2*i + 1], clause_qubits[9])     
        
    # qc.er()      #oddeleni pro lepsi graficke znazorneni
    
    qc.mcx([0,1,2,3],clause_qubits[9])      #cast oracla dle obr. 9.4
    qc.mcx([0,1,4,5],clause_qubits[9])                                  
    qc.mcx([0,1,6,7],clause_qubits[9])                    
    qc.mcx([0,1,8,9],clause_qubits[9])                    
    qc.mcx([0,1,10,11],clause_qubits[9])                  
    qc.mcx([2,3,4,5],clause_qubits[9])
    qc.mcx([2,3,6,7],clause_qubits[9])
    qc.mcx([2,3,8,9],clause_qubits[9])
    qc.mcx([2,3,10,11],clause_qubits[9])
    qc.mcx([4,5,6,7],clause_qubits[9])
    qc.mcx([4,5,8,9],clause_qubits[9])
    qc.mcx([4,5,10,11],clause_qubits[9])
    qc.mcx([6,7,8,9],clause_qubits[9])
    qc.mcx([6,7,10,11],clause_qubits[9])
    qc.mcx([8,9,10,11],clause_qubits[9])
    
    # qc.barrier()

    i = 0
    for clause in clause_list:                        #kotrola policek dle podminek clause_list
        clause_ = clause_list[i] 
        policko1 = clause_[0]
        policko2 = clause_[1]
        XOR(qc, policko1[0], policko1[1], policko2[0], policko2[1], clause_qubits[i])
        # qc.barrier()
        i += 1

    qc.mcx(clause_qubits, output_qubit) #jsou-li vsechny podminkove qubity 1, tak dojde k flipnuti vystupniho 
                                        #qubitu z druheho registru                        
    # qc.barrier()                        #je-li alespon jeden z qubitu 0, tak nejsou splneny pozadavky a ke zmene
                                        #nedojde
    i = 0
    for clause in clause_list:          #vraceni podminkovych qubitu do puvodniho stavu zopakovanim celeho 
        clause_ = clause_list[i]        #oracla znovu
        policko1 = clause_[0]
        policko2 = clause_[1]
        XOR(qc, policko1[0], policko1[1], policko2[0], policko2[1], clause_qubits[i])
        # qc.barrier()
        i += 1
    
    for i in range(6):                                                        
        qc.ccx(var_qubits[2*i], var_qubits[2*i + 1], clause_qubits[9])
        
    # qc.barrier()
    qc.mcx([0,1,2,3],clause_qubits[9])
    qc.mcx([0,1,4,5],clause_qubits[9])
    qc.mcx([0,1,6,7],clause_qubits[9])
    qc.mcx([0,1,8,9],clause_qubits[9])
    qc.mcx([0,1,10,11],clause_qubits[9])
    qc.mcx([2,3,4,5],clause_qubits[9])
    qc.mcx([2,3,6,7],clause_qubits[9])
    qc.mcx([2,3,8,9],clause_qubits[9])
    qc.mcx([2,3,10,11],clause_qubits[9])
    qc.mcx([4,5,6,7],clause_qubits[9])
    qc.mcx([4,5,8,9],clause_qubits[9])
    qc.mcx([4,5,10,11],clause_qubits[9])
    qc.mcx([6,7,8,9],clause_qubits[9])
    qc.mcx([6,7,10,11],clause_qubits[9])
    qc.mcx([8,9,10,11],clause_qubits[9])
    
#vytvoreni oracla se vsemi castmi
def diffuser(nqubits):
    qc = QuantumCircuit(nqubits)
    for qubit in range(nqubits):
        qc.h(qubit)
        
    for qubit in range(nqubits):
        qc.x(qubit)
        
    qc.h(nqubits-1)
    qc.mcx(list(range(nqubits-1)), nqubits-1)
    qc.h(nqubits-1)
    for qubit in range(nqubits):
        qc.x(qubit)
        
    for qubit in range(nqubits):
        qc.h(qubit)
    U_s = qc.to_gate()
    U_s.name = "U_s"
    return U_s

def grover_operator(clause_list, var_qubits, clause_qubits, output_qubit):
    # Create Grover operator as a gate
    qc = QuantumCircuit(var_qubits, clause_qubits, output_qubit)

    
    # Oracle
    
    oracle(qc, clause_list, clause_qubits, var_qubits, output_qubit)

    # Diffuser (only on var_qubits)
    diff = diffuser(len(var_qubits))
    qc.append(diff, var_qubits[:])
    # diff = diffuser(len(var_qubits))
    # qc.append(diff, range(len(var_qubits)))
    
    # Convert to gate
    grover_gate = qc.to_gate()
    grover_gate.name = "Grover"
    return grover_gate

def qpe_with_grover(clause_list, precision_qubits):
    # Create registers
    t = precision_qubits  # number of precision qubits
                                 
    var_qubits = QuantumRegister(12,name='q')
    clause_qubits = QuantumRegister(10, name='c')
    output_qubit = QuantumRegister(1, name='o')
    phase_qubits = QuantumRegister(t, 'phase')
    cbits = ClassicalRegister(t, 'cbits')
    
    # Create circuit
    qc = QuantumCircuit(phase_qubits, var_qubits, clause_qubits, output_qubit, cbits)
    
    # Initialize var_qubits in superposition
    for qubit in var_qubits:
        qc.h(qubit)
    
    # Initialize phase estimation qubits
    for qubit in phase_qubits:
        qc.h(qubit)
    for qubit in output_qubit:
        qc.x(qubit)
        qc.h(qubit)
    # Create Grover operator
    grover = grover_operator(clause_list, var_qubits, clause_qubits, output_qubit)
    # Controlled Grover operations
    for i in range(t-1,-1,-1):
        # Apply 2^i controlled Grover operations
        # print(i)
        index = t-i-1
        for j in range(2**index):
            c_q = grover.control()
            qc.append(c_q, [phase_qubits[i]] + var_qubits[:] + clause_qubits[:] + output_qubit[:])
    # print(qc.draw("mpl"))
    qc.append(QFT(t).inverse(), phase_qubits)

    # Measure phase qubits
    qc.barrier()
    qc.measure(phase_qubits, cbits)
    
    return qc


n = 12
e = 0.05  #error probability
m = np.ceil(n/2) +1
# m = n
t = math.ceil(m+ np.log2(2+1/(2*e)))
print("Precision qubits: ", t)
precision_qubits = int(t)  # Number of qubits for phase estimation
precision_qubits
qc = qpe_with_grover(clause_list, precision_qubits)


# backend = AerSimulator()
backend = AerSimulator(method='matrix_product_state')
qc_transpiled = transpile(qc, backend, optimization_level=1)



# Execute the transpiled circuit on the real quantum device
job = backend.run(qc_transpiled, shots=1024)


result = job.result()
counts = result.get_counts()
counts1 = result.get_counts(qc)

# Gets the most frequent value from counts1, which is the j that QPE returns
freq = qiskit.result.Counts.most_frequent(counts1)
qpe_result = int(freq,2)
print("phase: ",qpe_result) #finding j
# finding the number of solutions
m = math.ceil(2**n*(math.sin(math.pi*qpe_result/(2**precision_qubits) - math.pi/2))**2)
print("Number of solutions:", m)   

print("Time taken: ",result.time_taken)