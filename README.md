# QKD-Simulator
This Qiskit code simulates the BB84 Quantum Key Distribution Protocol.
It simulates the exchange of qubits between Alice and Bob, and checks the security of the 
key when an eavesdropper (Eve) is present

Features:
1) Uses the Quantum circuit class to model the three parties
2) The eavesdropper uses an Intersept-Resend attack in order to gain access to the information
3) Compares Alice's and Bob's bases create the sifted key
4) Calculates the Quantum Bit Error Rate (QBER)
5) Generates a high-resolution Circuit using Matplotlib

Requirements:
1) python 3.13+
2) qiskit
3) qiskit_aer
4) numpy
5) matplotlib

Results:
1) Alice's and Bob's Keys
2) Quantum Bit Error Rate :
                           1) If the QBER < 11% Then a Secure Key has been Established
                           2) If the QBER > 11% Connection is not Secure => Eavesdropper Detected


