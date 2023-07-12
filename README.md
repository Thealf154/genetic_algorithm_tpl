# Introduction

Implementation of all mutation operators mentionated in the **Combined Mutation Operators of Genetic Algorithm for the Travelling Salesman problem**, you can checkout the paper in link: https://www.redalyc.org/pdf/2652/265219635002.pdf. You can understand the gist of the operators just form reading the paper, however, there's the whole explanation of the algorithms in the TPL_LATEX pdf in SPANISH.

The problem solves a classic Travelling Salesman Problem using a matrix of points in a city. The code is in the `genetic_algoritm.*`,  the `.py` file is only there for debugging pourposes.

# Mutation operators
- Inversion
- Displacement
- Exchange
- Insertion
- Inverted exchange
- Inverted displacement

# Performance

The performance is measured in loop cycles, (THIS IS WITHOUT ANY MUTATION PERCENTAGE LIMIT):
![Performance of mutation operators](/graph_performance.png)