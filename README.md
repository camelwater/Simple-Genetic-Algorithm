# String-Grouping-Optimization-Algorithms
slightly modified genetic algorithm to group random strings by prefixes and suffixes + simulated annealing algorithm as well \
originally wrote this for something else, but performance proved to be too slow. GA isn't a good approach to solve this string grouping problem, but it's kind of cool. The SA approach was significantly better. This is probably because: 

**1)** SA is single-state, as opposed to GA, which initializes many states to make up a population. This means there are much less fitness calculations and tag-finding when using SA. \
**2)** GA uses crossover, which is extremely inefficient for this problem. I got rid of the crossover step in the GA anyways, but another clear indication of GA's poor fit for this problem. \
**3)** I modified the GA to have mutations on within the elite as well as the non-elite. This significantly slows down the algorithm as usually the non-elite population undergoes mutation, but not the elite. It's a bit overkill for most situations for this algorithm (most of the time there are a small number of strings), but maybe it helps converge to minimum more quickly with larger sets of strings (I don't know, I haven't really tested).

A better algorithm for this problem can be found [here](https://www.github.com/camelwater/strings-grouping-algorithm)
