import re
from qiskit import IBMQ, QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.providers.aer import QasmSimulator
from qiskit_ibm_provider import IBMProvider, least_busy

print('='*50 + '\nQYahtzee135.\nCode by Luiz Filipi Anderson de Sousa Moura\n' + '='*50)

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

nQubits = 1
while 1:
    nQubits = input('Use 1, 3 or 5 qubits? (1 / 3 / 5) ')
    if nQubits == '1' or '3' or '5': break

q = QuantumRegister(int(nQubits))
c = ClassicalRegister(int(nQubits))
qc = QuantumCircuit(q,c)

isFinished = False
step = 0
ptsOnes, ptsTwos, ptsThrees, ptsFours, ptsFives, ptsSixes, ptsBonus, ptsChance, pts3ofakind, pts4ofakind, ptsFullhouse, ptsSmallstr, ptsLargestr, ptsYahtzee, ptsTotal = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
def rollDice():
    if nQubits == '1':
        dice = 1
        for i in range(5):
            qc.h(0)
            qc.measure(0, 0)
            qc.reset(0)
            job = backend.run(qc, shots=1)
            result = job.result()
            counts = result.get_counts()
            if '1' in counts: dice += 1
        return dice
    elif nQubits == '3':
        while 1:
            for i in range(3):
                qc.h(i)
                qc.measure(i, i)
                qc.reset(i)
            job = backend.run(qc, shots=1)
            result = job.result()
            counts = result.get_counts()
            if '111' not in counts and '000' not in counts:
                return int(list(counts.keys())[0], 2)
    elif nQubits == '5':
        for i in range(5):
            qc.h(i)
            qc.measure(i, i)
            qc.reset(i)
        job = backend.run(qc, shots=1)
        result = job.result()
        counts = result.get_counts()
        return [int(i) for i in str(list(counts.keys())[0])].count(1) + 1

def showHelp():
    print('')
    print('\'list\'\t\tto display available plays and total score')
    print('\'all\'\t\tto redice all')
    print('\'a\'\t\tto change dice a*')
    print('\'ab\'\t\tto change dice a and b*')
    print('\'abc\'\t\tto change dice a, b, c*')
    print('\'abcd\'\t\tto change dice a, b, c, d*')
    print('\'1s\'\t\tto mark sum of ones')
    print('\'2s\'\t\tto mark sum of twos')
    print('\'3s\'\tto mark sum of threes')
    print('\'4s\'\t\tto mark sum of fours')
    print('\'5s\'\t\tto mark sum of fives')
    print('\'6s\'\t\tto mark sum of sixes')
    print('\'c\'\tto mark sum of dices')
    print('\'3k\'\t\tto mark sum of dices, if 3 dices are equal')
    print('\'4k\'\t\tto mark sum of dices, if 4 dices are equal')
    print('\'fh\'\t\tto score full house')
    print('\'ss\'\t\tto score small straight')
    print('\'ls\'\t\tto score large straight')
    print('\'y\'\tto score yahtzee')
    print('*a, b, c, d are numbers from 1 to 5')
    print('**If a play not possible is chosen, that play is marked as -1 and is not available anymore. Zero points will be counted in the end of the game.')
    showHand()

def showList():
    print('')
    print('-----------------------------------------------')
    print('\t\tList ')
    print('-----------------------------------------------')
    print('Ones\t\t\t\t\t\t', ptsOnes)
    print('Twos\t\t\t\t\t\t', ptsTwos)
    print('Threes\t\t\t\t\t\t', ptsThrees)
    print('Fours\t\t\t\t\t', ptsFours)
    print('Fives\t\t\t\t\t', ptsFives)
    print('Sixes\t\t\t\t\t', ptsSixes)
    print('Bonus (35 pts if <= 63)\t\t\t\t', ptsBonus)
    print('-----------------------------------------------')
    print('Chance (sum)\t\t\t\t\t', ptsChance)
    print('3 of a kind (sum)\t\t\t\t', pts3ofakind)
    print('4 of a kind (sum)\t\t\t\t', pts4ofakind)
    print('Full house (25 pts)\t\t\t\t', ptsFullhouse)
    print('Small straight (30 pts)\t\t\t\t', ptsSmallstr)
    print('Large Straight (40 pts)\t\t\t\t', ptsLargestr)
    print('Yahtzee (50 pts +100 for each extra time)\t', ptsYahtzee)
    print('-----------------------------------------------')
    print('Total\t\t', getTotal())
    print('-----------------------------------------------')
    showHand()

def showHand():
    global step, hand
    print('\nYour hand is', hand, '(step', step+1, '/ 3)')

def newHand():
    global step, hand
    hand = [int(rollDice()),int(rollDice()),int(rollDice()),int(rollDice()),int(rollDice())]
    step = 0
    showHand()

def only2RedicesAllowed():
    print('\nOnly 2 redices allowed')
    showHand()

def rediceAll():
    global step, hand
    if step >= 2: only2RedicesAllowed()
    else:
        hand = [int(rollDice()),int(rollDice()),int(rollDice()),int(rollDice()),int(rollDice())]
        step += 1
        showHand()
        if hand.count(hand[0]) == 5 and ptsYahtzee >= 50: newYahtzee()

def redice(dices):
    global step, hand
    if step >= 2: only2RedicesAllowed()
    elif len(dices) != len(set(dices)):
        print(f'Repeating numbers')
        showHand()
    else:
        for i in dices: hand[i-1] = int(rollDice())
        step += 1
        showHand()
        if hand.count(hand[0]) == 5 and ptsYahtzee >= 50: newYahtzee()

def alreadyMarkedPlay():
    print('Already marked play')
    showHand()

def ones():
    global ptsOnes, ptsBonus, hand
    if ptsOnes != 0: alreadyMarkedPlay()
    else:
        ptsOnes = hand.count(1)
        if ptsOnes == 0: ptsOnes = -1
        if ptsBonus == 0 and ptsOnes + ptsTwos + ptsThrees + ptsFours + ptsFives + ptsSixes >= 63:
            ptsBonus = 35
        checkIfIsFinished()

def twos():
    global ptsTwos, ptsBonus, hand
    if ptsTwos != 0: alreadyMarkedPlay()
    else:
        ptsTwos = hand.count(2) * 2
        if ptsTwos == 0: ptsTwos = -1
        if ptsBonus == 0 and ptsOnes + ptsTwos + ptsThrees + ptsFours + ptsFives + ptsSixes >= 63:
            ptsBonus = 35
        checkIfIsFinished()

def threes():
    global ptsThrees, ptsBonus, hand
    if ptsThrees != 0: alreadyMarkedPlay()
    else:
        ptsThrees = hand.count(3) * 3
        if ptsThrees == 0: ptsThrees = -1
        if ptsBonus == 0 and ptsOnes + ptsTwos + ptsThrees + ptsFours + ptsFives + ptsSixes >= 63:
            ptsBonus = 35
        checkIfIsFinished()

def fours():
    global ptsFours, ptsBonus, hand
    if ptsFours != 0: alreadyMarkedPlay()
    else:
        ptsFours = hand.count(4) * 4
        if ptsFours == 0: ptsFours = -1
        if ptsBonus == 0 and ptsOnes + ptsTwos + ptsThrees + ptsFours + ptsFives + ptsSixes >= 63:
            ptsBonus = 35
        checkIfIsFinished()

def fives():
    global ptsFives, ptsBonus, hand
    if ptsFives != 0: alreadyMarkedPlay()
    else:
        ptsFives = hand.count(5) * 5
        if ptsFives == 0: ptsFives = -1
        if ptsBonus == 0 and ptsOnes + ptsTwos + ptsThrees + ptsFours + ptsFives + ptsSixes >= 63:
            ptsBonus = 35
        checkIfIsFinished()

def sixes():
    global ptsSixes, ptsBonus, hand
    if ptsSixes != 0: alreadyMarkedPlay()
    else:
        ptsSixes = hand.count(6) * 6
        if ptsSixes == 0: ptsSixes = -1
        if ptsBonus == 0 and ptsOnes + ptsTwos + ptsThrees + ptsFours + ptsFives + ptsSixes >= 63:
            ptsBonus = 35
        checkIfIsFinished()

def chance():
    global ptsChance, hand
    if ptsChance != 0: alreadyMarkedPlay()
    else:
        ptsChance = hand[0] + hand[1] + hand[2] + hand[3] + hand[4]
        checkIfIsFinished()

def threeK():
    global pts3ofakind, hand
    if pts3ofakind != 0: alreadyMarkedPlay()
    elif hand.count(hand[0]) >= 3 or hand.count(hand[1]) >= 3 or hand.count(hand[2]) >= 3:
        pts3ofakind = hand[0] + hand[1] + hand[2] + hand[3] + hand[4]
        checkIfIsFinished()
    else:
        pts3ofakind = -1
        checkIfIsFinished()

def fourK():
    global pts4ofakind, hand
    if pts4ofakind != 0: alreadyMarkedPlay()
    elif hand.count(hand[0]) >= 4 or hand.count(hand[1]) >= 4:
        pts4ofakind = hand[0] + hand[1] + hand[2] + hand[3] + hand[4]
        checkIfIsFinished()
    else:
        pts4ofakind = -1
        checkIfIsFinished()

def fh():
    global ptsFullhouse, hand
    if ptsFullhouse != 0: alreadyMarkedPlay()
    elif len(set(hand)) == 2 and (hand.count(hand[0]) == 2 or 3):
        ptsFullhouse = 25
        checkIfIsFinished()
    else:
        ptsFullhouse = -1
        checkIfIsFinished()

def ss():
    global ptsSmallstr, hand
    if ptsSmallstr != 0: alreadyMarkedPlay()
    elif len(set(hand)) >= 4 and 3 in hand and 4 in hand:
        if 1 in hand and 2 in hand:
            ptsSmallstr = 30
            checkIfIsFinished()
        elif 2 in hand and 5 in hand:
            ptsSmallstr = 30
            checkIfIsFinished()
        elif 5 in hand and 6 in hand:
            ptsSmallstr = 30
            checkIfIsFinished()
    else:
        ptsSmallstr = -1
        checkIfIsFinished()

def ls():
    global ptsLargestr, hand
    if ptsLargestr != 0: alreadyMarkedPlay()
    elif len(set(hand)) == 5 and 2 in hand and 3 in hand and 4 in hand and 5 in hand:
        if 1 in hand:
            ptsSmallstr = 30
            checkIfIsFinished()
        elif 6 in hand:
            ptsSmallstr = 30
            checkIfIsFinished()
    else:
        ptsLargestr = -1
        checkIfIsFinished()

def yahtzee():
    global ptsYahtzee, hand
    if ptsYahtzee != 0: alreadyMarkedPlay()
    elif hand.count(hand[0]) == 5:
        ptsYahtzee = 50
        checkIfIsFinished()
    else:
        ptsYahtzee = -1
        checkIfIsFinished()

def newYahtzee():
    global ptsYahtzee
    ptsYahtzee += 100
    print('New yahtzee! +100 pts')

def getTotal():
    global ptsTotal, ptsOnes, ptsTwos, ptsThrees, ptsFours, ptsFives, ptsSixes, ptsBonus, ptsChance, pts3ofakind, pts4ofakind, ptsFullhouse, ptsSmallstr, ptsLargestr, ptsYahtzee
    ptsTotal = ptsBonus
    if ptsOnes >= 1: ptsTotal += ptsOnes
    if ptsTwos >= 1: ptsTotal += ptsTwos
    if ptsThrees >= 1: ptsTotal += ptsThrees
    if ptsFours >= 1: ptsTotal += ptsFours
    if ptsFives >= 1: ptsTotal += ptsFives
    if ptsSixes >= 1: ptsTotal += ptsSixes
    if ptsChance >= 1: ptsTotal += ptsChance
    if pts3ofakind >= 1: ptsTotal += pts3ofakind
    if pts4ofakind >= 1: ptsTotal += pts4ofakind
    if ptsFullhouse >= 1: ptsTotal += ptsFullhouse
    if ptsSmallstr >= 1: ptsTotal += ptsSmallstr
    if ptsLargestr >= 1: ptsTotal += ptsLargestr
    if ptsYahtzee >= 1: ptsTotal += ptsYahtzee
    return ptsTotal

def checkIfIsFinished():
    global isFinished, ptsTotal, ptsOnes, ptsTwos, ptsThrees, ptsFours, ptsFives, ptsSixes, ptsBonus, ptsChance, pts3ofakind, pts4ofakind, ptsFullhouse, ptsSmallstr, ptsLargestr, ptsYahtzee
    if ptsOnes !=0 and ptsTwos !=0 and ptsThrees !=0 and ptsFours !=0 and ptsFives !=0 and ptsSixes !=0:
        if ptsChance !=0 and pts3ofakind !=0 and pts4ofakind !=0 and ptsFullhouse !=0 and ptsSmallstr !=0 and ptsLargestr !=0 and ptsYahtzee !=0:
            print(f'End game! Total points: {getTotal()}')
            isFinished = True
    else: newHand()

hand = list()
newHand()
while isFinished == False:
    cmd = input('\nCommand> ')
    if cmd == 'help': showHelp()
    elif cmd == 'list': showList()
    elif cmd == 'all': rediceAll()
    elif re.search("^[1-5]$|^[1-5][1-5]$|^[1-5][1-5][1-5]$|^[1-5][1-5][1-5][1-5]$", cmd): redice([int(i) for i in str(cmd)])
    elif cmd == '1s': ones()
    elif cmd == '2s': twos()
    elif cmd == '3s': threes()
    elif cmd == '4s': fours()
    elif cmd == '5s': fives()
    elif cmd == '6s': sixes()
    elif cmd == 'c': chance()
    elif cmd == '3k': threeK()
    elif cmd == '4k': fourK()
    elif cmd == 'fh': fh()
    elif cmd == 'ss': ss()
    elif cmd == 'ls': ls()
    elif cmd == 'y': yahtzee()
    else: print('Command not valid. Enter \'help\' if necessary.')
