from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np
import matplotlib.pyplot as plt

# BB84 Protocol Simulation

rng = np.random.default_rng()
# this creates an rng object
bit_num = 31
# this generates a random int between 2 & 30
qc = QuantumCircuit(bit_num, bit_num * 2)
# this initializes the circuit with bit_num qubits and classical bits 
# the * 2 is for eve

# STEP ONE
# Random bits and bases for alice

a_bits = rng.integers(0, 2, size=bit_num)
# Generates the random bits that Alice will send
# rng.integers generates integers (0 or 1)

a_bases = rng.integers(0, 2, size=bit_num)
# This generates random numbers if the number is 0 alice uses Rectilinear base {|0>,|1>}
# if the base is 1 then she uses the Diagonal base {|+>,|->}

for n in range(bit_num):
    if a_bits[n] == 1: 
        qc.x(n)
    # note for moi : if the bit is 0 then it's already in |0> so no point in appllying the X gate
    # BUT if the bit is 1 then we need to apply Pauli-X to flip it to |1>
    
    if a_bases[n] == 1:
        qc.h(n)
    # note for moi 2: if the base is 1 then we need to apply the Hadamard gate to
    # put the qubits in superposition, diladi
    # |0> -> |+> and |1> -> |->

    # no need to write a lot of if statements this way is more efficient
    # (if you get confused when you read it, just write it on a piece of paper and you will remember it)
qc.barrier()

# STEP TWO
# Eve Detection

e_bases = rng.integers(0, 2, size=bit_num)
# the logic is the same as the one used for Alice and Bob, Eve randomly chooses her bases

for j in range(bit_num):
    if e_bases[j] == 1:
        qc.h(j)
    # again if the base is 0 then there is no reason to appy a Pauli-X gate since the qubits are already in the rectilinear base

    qc.measure(j, j + bit_num)

    if e_bases[j] == 1:
        qc.h(j)
    # if eve applied a Hadamard gate before the measurement the she needs to apply it again so that the qubis are in the same state as before the measurement 

qc.barrier()

# STEP THREE 
# Bob's measurment

b_bases = rng.integers(0, 2, size=bit_num)
# bob randomly chooses his bases 
# logic same as before

for m in range(bit_num):
    if b_bases[m] == 1:
        qc.h(m)
    # Note for moi 3: Q.Cs measure using the rectilinear base by default so if the base Bob chose is 0
    qc.measure(m, m)

# VISUALISATION 1
# print("Alice's bits :", a_bits)
# print("Alice's bases : ", a_bases)
# print("Bob's Bases : ", b_bases)
# qc.draw("mpl", style={'figsize': (50, 50)})
# plt.show()

# STEP FOUR
backend = AerSimulator()
# high-performance local quantum chip simulator 
# Note for moi 4 : Prev. used Aer.get_backend('qasm_simulator') but had an error so i changed it to AerSimulator()
# qasm stands for quantum assembly language

job = backend.run(qc, shots=1)
# each photon is sent only once
result = job.result()
# this waits for the simulation to finish and then

counts = result.get_counts()
# returns a dictionary with the results of the measurement
output = list(counts.keys())[0][::-1]
# In qiskit the qubits are ordered from right to left dialdi [1 0] will be read as 01 
# the [::-1] opperator flips them back to 10
# list(counts.keys()) basically transforms the dictionart from a string to a list of bits
b_bits = [int(bit) for bit in output[:bit_num]]
# output[:bit_num] tells python to start at index 0 and stop at index bit_num
e_bits = [int(bit) for bit in output[bit_num: 2*bit_num]]
# output[bit_num: 2*bit_num] tells python to start at index bit_num and stop at index 2*bit_num
# note for moi 5: basically tells python to slice the second half of the output ( the part that contains eve's bits)

# STEP FIVE
# Sifting the key

a_key = []
b_key = []

for i in range(bit_num):
    if a_bases[i] == b_bases[i]:
        a_key.append(int(a_bits[i]))
        b_key.append(int(b_bits[i]))
        # checks if alice and bob used the same bases if they did then the bits are added to the key
        # note for moi 6: remeber from class they choose the same bases with a prob. of 50% on average

print("------------------------------------------")
print("Alice's bits :", a_bits)
print("Alice's bases : ", a_bases)

print("\nEve's bits :", e_bits)
print("Eve's bases :", e_bases)

print("\nBob's Bases :", b_bases)
print("Bob's bits :", b_bits)

print("-----------sifting the key----------------")
print(f"Alice's key : {a_key}")
print(f"Bob's key : {b_key}")
print("------------------------------------------")

# STEP SIX
# Quantum Bit Error Rate (QBER)

if len(a_key) > 0:
    mismatched = 0
    for k in range(len(a_key)):
        if a_key[k] != b_key[k]:
            mismatched += 1
        # counts the number of mismatched bits 
        # mismatched meaning bob's and alice's bits where different even though they used the same bases, 
        # this can only happen if eve measured the qubits in the wrong bases changing the state of the qubits
    QBER = mismatched/ len(a_key) * 100

    # calculates the Quantum Bit Error Rate (QBER)
    # QBER = #of mismatched bits / #of sifted bits
    if QBER > 11.0:
        print("Eve detected! QBER above 11%")
    else:
        print("QBER is below the threshold")
    print(f"QBER : {QBER:.2f}%")
else:
    print("The sifted key is empty, QBER cannot be calculated")

print("------------------------------------------")

qc.draw("mpl", 
        fold=-1,                  # This keeps the circuit in one continuous line
        scale=0.6,                # Shrinks the qubits so more can fit on screen
        style={'figsize': (50, 15),
               'fontsize': 8},    
               # this makes the tect smaller so it's more readable
        plot_barriers=True)
plt.show();