# String-Grouping-Optimization-Algorithms
slightly modified genetic algorithm to group random strings by prefixes and suffixes + simulated annealing algorithm as well \
originally wrote this for something else, but performance proved to be too slow. GA isn't a good approach to solve this string grouping problem, but it's kind of cool. The SA approach was significantly better. This is probably because: 

**1)** SA is single-state, so much less tag calculations compared to GA's population \
**2)** GA uses crossover, which is extremely inefficient for this problem. I got rid of the crossover step in the GA anyways, but another clear reason why GA doesn't really fit well. \
**3)** I modified the GA to have mutations and possible replacements based on fitness evaluations within the elite as well. This significantly slows down the algorithm as usually the non-elite population undergoes mutation, but not the elite. It's a bit overkill over most situations (small number of strings), but maybe it helps converge to minimum more quickly with larger sets of strings.

A better algorithm for this problem can be found [here](https://www.github.com/camelwater/strings-grouping-algorithm)
