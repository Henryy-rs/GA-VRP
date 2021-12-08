# Steady State Genetic Algorithm with Capacitated Vechile Routing(for practice)

Python implementation of capacitated vehicle routing problem with steady state genetic algorithm.

See here for a detailed explanation.

https://github.com/krishna-praveen/Capacitated-Vehicle-Routing-Problem#problem-statement

## Pseudocode

<b>Steady State Genetic Algorithm with Capacitate Vehicle Routing Problem</b>

 ```bash
1 initialize population
2 save initial cost of population
3   while not convergence:
4   select two best chromosomes from population
5   crossover chromosomes 
6   mutate offsprings with a certain probability
7   If offsprings are not same then 
7     for each offsprings:
8       If offspring has a lower cost than the worst chromosome) 
9         then replace worst chromosome with offspring
10  save cost for this iteration

 ```

## usage


 ```bash
 
    python run.py

 ```

## result

![cost](https://user-images.githubusercontent.com/28619620/145239898-183a54d1-6fa5-41be-927e-79329d87895b.png)
![route](https://user-images.githubusercontent.com/28619620/145239929-1c85429b-43a6-4d2c-9f87-0bdf2e1ddee6.png)


## Reference
- input data, ordered crossover, plotting route codes are borrowed from here. thanks for your work.

https://github.com/krishna-praveen/Capacitated-Vehicle-Routing-Problem#assumptions

- capacitated vehicle routing problem

https://developers.google.com/optimization/routing/cvrp

- steady state GA

https://arxiv.org/pdf/1911.00490.pdf

- ordered crossover

http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.50.1898&rep=rep1&type=pdf p3~4

- mutation

https://www.tutorialspoint.com/genetic_algorithms/genetic_algorithms_mutation.htm

