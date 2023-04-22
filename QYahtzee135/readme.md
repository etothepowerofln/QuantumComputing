# Yahtzee with 1, 3 or 5 qubits

The algorithm uses properties of quantum mechanics to set a qubit (or a set of qubits) in a superposition state such that the chance of heads or tails is evenly 50% for each case.
In other words, I use quantum mechanics to create a perfect dice for yahtzee.

The game is fully playable through your terminal. You can choose to run on a local simulator running in your machine (IBM QasmSimulator) or to run on an IBM cloud device (a free account in necessary).
IBM allows free access to quantum hardwares with 5 or 7 qubits if you have an account. Also, you can run on cloud simulators.
In the beginning of the game I ask if you want to play with 1, 3 or 5 qubits. 1 qubit require 5 measurements for each dice. 3 or 5 qubits require only 1 measurement for each dice, but with 3 qubits values 0 or 7 are ignored, costing a redice.
