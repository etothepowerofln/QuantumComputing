# N Sided Dice with 1, lg N or N qubits

This program uses quantum superposition effects to create a perfect dice with N sides. The N sided dice can include numbers [1, N] or [0, N - 1] by choosing if zero should be included or not.

The user can choose to simulate the dice on local machine or to use one of the cloud machines from IBM (a free account is necessary for the former option). Further option is the number of qubits used. You can always use only 1 qubit for any dice, but it might take longer, because N - 1 measurements are necessary. Choosing lg N or N qubits are faster options. When N - 1 qubits are not available, 1 + truncated lg N qubits is a fast substitute, with the drawback of having to repeat measurement with a chance close to 1 - N / (1 + truncated lg N)^2.
