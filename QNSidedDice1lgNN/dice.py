from qiskit import IBMQ, QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.providers.aer import QasmSimulator
from qiskit_ibm_provider import IBMProvider, least_busy
import math

print('='*50 + '\nQNSidedDice1lgNN.\nCode by Luiz Filipi Anderson de Sousa Moura\n' + '='*50)

try:
    realDevice = str()
    while 1:
        realDevice = input('Use cloud device or local simulator? (cloud / local) ')
        if realDevice != 'cloud' or 'local': break
    if realDevice == 'local':
        backend = QasmSimulator()
    else:
        print('You can find your IBM API TOKEN at https://quantum-computing.ibm.com/lab/docs/iql/manage/account/ibmq')
        token = input('Insert IBM API TOKEN: ')

        IBMProvider.save_account(token, overwrite=True) 
        provider = IBMProvider()
        backend = provider.get_backend("ibmq_qasm_simulator")
        print(provider.backends())
        while 1:
            try:
                backend = provider.get_backend(str(input('Choose backend: ')))
                break
            except:
                continue   
except:
    print('Not possible to load quantum device. You may need to pip3 install qiskit and qiskit_ibm_provider.')
    exit()
print('Selected:', backend)

N = 6
while 1:
    N = input('Number of sides: ')
    if int(N) > 1: break
N = int(N)

includeZero = False
while 1:
    includingZero = input('Including zero? (yes / no) ')
    if includingZero == 'yes':
        includeZero = True
        print('Settings:\n\tDice (0 to ' + str(N-1) + ')')
        break
    if includingZero == 'no':
        includeZero = False
        print('Settings:\n\tDice (1 to ' + str(N) + ')')
        break

Q = 1
while 1:
    nQubits = input('Use 1, lgN or N-1 qubits? (1 / lgN / N) ')
    if nQubits == '1':
        Q = 1
        break
    if nQubits ==  'lgN':
        Q = int(math.log2(N))
        break
    if nQubits == 'N':
        Q = N - 1
        break

q = QuantumRegister(Q)
c = ClassicalRegister(Q)
qc = QuantumCircuit(q,c)

def rollDice():
    if Q == 1:
        if includeZero == True: dice = 0
        else: dice = 1
        for i in range(N-1):
            qc.h(0)
            qc.measure(0, 0)
            qc.reset(0)
            job = backend.run(qc, shots=1)
            result = job.result()
            counts = result.get_counts()
            dice += int(list(counts.keys())[0], 2)
        return dice
    elif Q == math.log2(N):
        while 1:
            for i in range(Q):
                qc.h(i)
                qc.measure(i, i)
                qc.reset(i)
            job = backend.run(qc, shots=1)
            result = job.result()
            counts = result.get_counts()
            if int(list(counts.keys())[0], 2) < N and includeZero == True:
                return [int(i) for i in str(list(counts.keys())[0])].count(1)
            if 0 < int(list(counts.keys())[0], 2) <= N and includeZero == False:
                return [int(i) for i in str(list(counts.keys())[0])].count(1)
    elif Q == N - 1:
        for i in range(Q):
            qc.h(i)
            qc.measure(i, i)
            qc.reset(i)
        job = backend.run(qc, shots=1)
        result = job.result()
        counts = result.get_counts()
        if includeZero: return [int(i) for i in str(list(counts.keys())[0])].count(1)
        else: return [int(i) for i in str(list(counts.keys())[0])].count(1) + 1
        
print('Result: ' + str(rollDice()))
