Title: Knapsack problem
Date: 2017-08-14 16:45
Category: Data Struct & Algo
Tags: dynamic programming, greedy algorithm
Summary: summarizes knapsack problem and its variations

I'm studying this problem on my way from Beijing to Austin to kill some time.
This problem works pretty well for this purpose. There are three kinds of 
forms of the problem, which I'll summarize below. Also, this is a good example
of dynamic programming paradigm.

[TOC]

## Knapsack problem

Suppose we are planning a hiking trip; and we are, therefore, interested in 
filling a knapsack with items that are considered necessary for the trip. 
There are $N$ different item types that are deemed desirable; 
these could include bottle of water, apple, orange, sandwich, and so
forth. Each item type has a given set of two attributes, namely a weight $W$ and a
value that quantifies the level of importance associated with each unit of that 
type of item. Since the knapsack has a limited weight capacity, 
the problem of interest is to figure out how to load the knapsack with a 
combination of units of the specified types of items that yields the greatest total value. 

A large variety of resource allocation problems can be cast in the framework of a knapsack
problem. The general idea is to think of the capacity of the knapsack as the available amount
of a resource and the item types as activities to which this resource can be allocated. Two
quick examples are the allocation of an advertising budget to the promotions of individual
products and the allocation of your effort to the preparation of final exams in different
subjects.

## A breif revisit to dynamic programming

Dynamic programming is a algorithm design strategy when a problem can be broken
down into recurring small problems. Specifically, it is used when the solution can be
recursively described in terms of solutions to subproblems and algorithms find solutions
to subproblems and store them for later use. This is better than "brute-force methods",
which solves the same subproblem over and over again. It is different from divide-and-conquer
paradigm in the sense that divide-and-conquer divides the problem into independent subproblems
and solve them individually, and then combine them to form the final solution. There is
no re-use of a solution to one subproblem in order to solve another subproblem, like dynamic programming.
From this perspective, dynamic programm is more like recursion + re-use [^1].

[^1]: See [Difference between Divide and Conquer Algo and Dynamic Programming SO post](https://stackoverflow.com/questions/13538459/difference-between-divide-and-conquer-algo-and-dynamic-programming)

The general steps to use dynamic programming paradigm is that:

1. Define the subproblems
2. Define the solution to subproblems, which can be reused by other subproblems (if you think of recursion, the solution to
subproblem can be re-used by the subproblem one function call earlier).
3. Solve the problem bottom-up from "basic cases", building a table of solved subproblems that are used to solve larger ones

## 0-1 knapsack problem

The first type of knapsack program has the following restriction on how the item should
be picked: *items are not divisible*. In other words, you either take an item or not.

Let's first formulate this problem mathematically. Given a knapsack with 
maximum capacity $W$, and a set $S$ consisting of $n$ items. 
Each item $i$ has some weight $w_i$ and benefit value $b_i$
(all $w_i$, $b_i$ and $W$ are integer values). The problem we try to solve is 
how to pack the knapsack to achieve maximum total value of packed items? In other words,
we try to find $\text{max}\sum_{i \in S} b_i \text{ subject to } \sum_{i \in S} w_i \le W$.

The first step in dynamic programming is to define the subproblems. In this problem, we 
can try to label the items from $1 \dots n$, and then a subproblem is to find an optimal
solution for $S_i = \left\lbrace \text{items labeled }  1,2,\dots, i \right\rbrace$. Once
we have a definition for the subproblem, we need to ask: can we describe the final solution
(i.e., $S_n$) in terms of subproblems (i.e., $S_i$)? Let's take a look at an example:

| Item          | 1 | 2 | 3 | 4 | 5  |
|---------------|---|---|---|---|----|
| Weight $w_i$  | 2 | 3 | 4 | 5 | 9  |
| Benefit $b_i$ | 3 | 4 | 5 | 8 | 10 |

Suppose $W = 20$. Then for $S_4$, the optimal solution is to put 
item $1,2,3,4$ into knapsack because the total weight is $2 + 3 + 4 + 5 = 14$, which
is less than $20$ and we have the maximum benefit: $20$. For $S_5$, the optimal solution
is to put item $1,3,4,5$ into knapsack with the total weight $2 + 4 + 5 + 9 = 20$ and maximum
benefit $26$. However, as you can see, the solution for $S_4$ (i.e., $1,2,3,4$) is not part
of the solution for $S_5$ (i.e., $1,3,4,5$). Thus, our definition of subproblem is not right.
Let's refine our subproblem definition by adding another parameter $w$ that represents the
exact weight for each subset of items. Then, our subproblem is to find the best subset of 
$S_i$ that has total weight $w$. The benefits corresponding with the best subset is denoted
as $B[i, w]$.

!!!note
    The problem with the first subproblem definition is that we kind of play greedy algorithm in
    the sense that we always choose the optimal solution for $S_i$ given $W$. However, the
    problem with greedy approach is that the optimal solution for $S_i$ may not be the part
    of solution for $S_n$. The refinement to that is that we allow to tweak $W$ to reflect
    the number of items we are considering. This idea will become clear once we walk through
    the solution to the problem. All in all, coming up a good subproblem definition is the 
    key in using dynammic programming, which requires many practice.

Once we have the subproblem definition, we can define our solution to the subproblem. In this 
case, our recursive formula for subproblems look like below:

$$
B[i,w]=\left\{
                \begin{array}{ll}
                  B[i-1,w] \text{ if } w_i > w \\
                  \text{max}\{B[i-1, w], B[i-1, w-w_i] + b_i\} \text{ otherwise }
                \end{array}
              \right.
$$

The idea for above recursion formula is that the best subset of $S_i$ that
has total weight $w$ either contains item $i$ or not. First case: $w_i > w$. 
Item $i$ can't be part of the solution because including item $i$ will have
the total weight greater than $w$, which is unacceptable. The second case:
$w_i \le w$. Item $i$ **can** be in the solution, and we choose the case 
with greater value: not contain $i$ (i.e., $B[i-1, w]$) or contain 
$i$ (i.e., $B[i-1, w-w_i] + b_i$).

!!!note
    As you can see from recursive formula, the solution $B[i,w]$ reuses
    the solution to $B[i-1, w]$ and $B[i-1, w-w_i]$, which is the signature of
    dynamic programming.

The algorithm is below:

```
for w = 0 to W 
    B[0,w] = 0
for i = 1 to n 
    B[i,0] = 0 
for i = 1 to n
    for w = 1 to W
        if w_i <=w  //item i can be part of the solution 
            if b_i + B[i-1,w-w_i ] > B[i-1,w]
                B[i,w] = b_i + B[i-1, w-w_i]
            else
                B[i,w] = B[i-1,w]
        else 
            B[i,w] = B[i-1,w] // w_i > w
```

The running time for this algorithm is $O(n*W)$ because of the double for loop. To understand this algorithm,
let's take a look at an example:

| Item          | 1 | 2 | 3 | 4 |
|---------------|---|---|---|---|
| Weight $w_i$  | 2 | 3 | 4 | 5 |
| Benefit $b_i$ | 3 | 4 | 5 | 6 |

Suppose $W = 5$ and with algorithm above, we essentially fill out a table like following:

| i \ w | 0 | 1 | 2 | 3 | 4 | 5 |
|-------|---|---|---|---|---|---|
| 0     | 0 | 0 | 0 | 0 | 0 | 0 |
| 1     | 0 |   |   |   |   |   |
| 2     | 0 |   |   |   |   |   |
| 3     | 0 |   |   |   |   |   |
| 4     | 0 |   |   |   |   |   |

Each cell in the above table represents $B[i,w]$ and the table looks like above after we executing 
the first two for loops

```
for w = 0 to W 
    B[0,w] = 0
for i = 1 to n 
    B[i,0] = 0 
```

Now, let's take a look at $B[1,1]$. We have $i = 1, b_i = 3, w_i = 2, w = 1$, and since $w_i > w$, and by our
algorithm, we have $B[i,w] = B[i-1,w]$, which is $B[0,1]$. Thus, $B[1,1] = 0$ and the table becomes

| i \ w | 0 | 1 | 2 | 3 | 4 | 5 |
|-------|---|---|---|---|---|---|
| 0     | 0 | 0 | 0 | 0 | 0 | 0 |
| 1     | 0 | 0 |   |   |   |   |
| 2     | 0 |   |   |   |   |   |
| 3     | 0 |   |   |   |   |   |
| 4     | 0 |   |   |   |   |   |

We can fill out the table like this and have

| i \ w | 0 | 1 | 2 | 3 | 4 | 5 |
|-------|---|---|---|---|---|---|
| 0     | 0 | 0 | 0 | 0 | 0 | 0 |
| 1     | 0 | 0 | 3 | 3 | 3 | 3 |
| 2     | 0 | 0 | 3 | 4 | 4 | 7 |
| 3     | 0 | 0 | 3 | 4 | 5 | 7 |
| 4     | 0 | 0 | 3 | 4 | 5 | 7 |

Now, we have the maximum benefit value given the capacity of the knapsack, which is $B[4,5] = 7$. 
The next question is to find out what items we should put inside the knapsack in order to have
this maximum benefit (i.e., $7$). The algorithm is below:

```
Let i = n and k = W
while i > 0 and k > 0
    if B[i,k] != B[i-1,k], then
        mark the ith item as in the knapsack
        i = i - 1
        k = k - w_i
    else
        i = i - 1
```

Let's first take a look a few examples on how this algorithm runs and then we will
see the intuition behind this algorithm. In our example, we start with
$i = 4, k = 5, w_i = 5, B[i,k] = 7, B[i-1,k] = 7$. Then, by our algorithm, we
decrements $i$ and move on. Same situtation happens when $i=3$ because $B[i,k] = B[i-1,k]$.
Now, when $i = 2$, we have $B[i,k] = 7$ and $B[i-1,k] = 3$. Thus, we mark $i=2$th item
as in the knapsack and this item has weight $w_2 = 3$ and $b_2 = 4$. Now, we decrement $i$ 
and update $k$ by $k = k - w_i = 5 - 4 = 3$. Now, we are at $B[1,2]$ cell. We do the same
for $i = 1$ and it turns out $i = 1$ should also be inside the knapsack.

You may now probably tell that the idea for the algorithm to find the exactly items inside
the knapsack is that *we always want to put the item inside the knapsack that has value 
gain*. This is just like "marginal thinking" in Economics. For example, we don't 
want to put $i = 4$th item inside knapsack because from $i = 3$ to $i = 4$, there is no value
gain (i.e. $B[i,k] = B[i-1,k] = 5$).

!!!note
    The detailed implementation of the algorithm in C can be found from 
    [my code-for-blog repo](https://github.com/xxks-kkk/Code-for-blog/blob/master/2017/knapsack/knapsack.c).

## 0-x knapsack problem

0-x knapsack problem is a generalization of 0-1 knapsack problem in the sense that
for item $i$ we can load multiple of it into our knapsack. Let $x_i$ to denote
the number of $i$th item are loaded into the knapsack. One requirement to $x_i$
is that it has to be integer-valued.

The problem formulation and subproblem definition is just like the 0-1 knapsack problem.
The only thing we need to do is to adjust is the recursive solution to subproblems:

$$
B[i,w]=\left\{
                \begin{array}{ll}
                  B[i-1,w] \text{ if } w_i > w \\
                  \max_{0 \le x_i \le \lfloor\frac{w}{w_i}\rfloor}\{B[i-1, w], B[i-1, w-w_ix_i] + b_ix_i\} \text{ otherwise }
                \end{array}
              \right.
$$

When $w_i > w$, we cannot include item $i$ at all. However, when $w_i < w$, we have more options 
because we can include multiple of item $i$. But, we cannot assign a value greater than $w/w_i$
to $x_i$. In addition, $w/w_i$ may not be an integer. So, we $x_i$ should be in the range 
$0 \le x_i \le \lfloor w/w_i \rfloor$, where the notation $\lfloor x \rfloor$ is, for any given $x$, 
defined as the greatest integer less than or equal to $x$. The algorithm is shown below:

```
for w = 0 to W
    B[0,w] = 0
for i = 1 to n
    B[i,0] = 0
for i = 1 to n
    for w = 1 to W
        if w_i <= w
            cands_B = a list of (w/x_i+1) items // hold the possible B[i,w] value for each x_i
            for x_i = 0 to w/x_i
                cands_B[x_i] = B[i-1, w - w_i * x_i] + b_i * x_i
                B[i,w] = max(cands_B)
                x[i,w] = x_i that is associated with B[i,w]
        else
            B[i,w] = B[i-1,w]
            x[i,w] = x_i that is associated with B[i-1,w]
```

Let's walk through an example to better understand the algorithm idea:

| Item          | 1 | 2 | 3 |
|---------------|---|---|---|
| Weight $w_i$  | 3 | 8 | 5 |
| Benefit $b_i$ | 4 | 6 | 5 |

$W = 8$ in our example. The algorithm essentially
tries to build fill out two tables $B[i,w]$ table like
the 0-1 knapsack problem:

| i \ w | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|-------|---|---|---|---|---|---|---|---|---|
| 0     | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1     | 0 | 0 | 0 | 4 | 4 | 4 | 8 | 8 | 8 |
| 2     | 0 | 0 | 0 | 4 | 4 | 4 | 8 | 8 | 8 |
| 3     | 0 | 0 | 0 | 4 | 4 | 5 | 8 | 8 | 9 |

and $x[i,w]$ table to keep track of the optimal
value of $x_i$ for each $i$ and $w$

| i \ w | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|-------|---|---|---|---|---|---|---|---|---|
| 1     | 0 | 0 | 0 | 1 | 1 | 1 | 2 | 2 | 2 |
| 2     | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 3     | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |

For $i = 1$, we have $w_i = 3, b_i = 4$. Thus, when
$w = 0,1,2$, we have $B[i,w] = 0$ and $x[i,w] = 0$ as well.
When $w = 3$, we can include $w_i$ inside the knapsack and
we calculate the following:

$$
B[1,3] = \max \{B[0,3], B[0,3-3*1]+4*1\} = \max \{0, 0+4\} = 4
$$

So, we fill in $B[1,3] = 4$ and $x[1,3] = 1$. We can repeatedly
doing this for other $i$s. We can take a look at the values
from another perspective like the tables below:

| B[1,w] | w | x_1* |
|--------|---|------|
| 0      | 0 | 0    |
| 0      | 1 | 0    |
| 0      | 2 | 0    |
| 4      | 3 | 1    |
| 4      | 4 | 1    |
| 4      | 5 | 1    |
| 8      | 6 | 2    |
| 8      | 7 | 2    |
| 8      | 8 | 2    |

| B[2,w] | w | x_2* |
|--------|---|------|
| 0      | 0 | 0    |
| 0      | 1 | 0    |
| 0      | 2 | 0    |
| 4      | 3 | 0    |
| 4      | 4 | 0    |
| 4      | 5 | 0    |
| 8      | 6 | 0    |
| 8      | 7 | 0    |
| 8      | 8 | 0    |

| B[3,w] | w | x_3* |
|--------|---|------|
| 0      | 0 | 0    |
| 0      | 1 | 0    |
| 0      | 2 | 0    |
| 4      | 3 | 0    |
| 4      | 4 | 0    |
| 5      | 5 | 1    |
| 8      | 6 | 0    |
| 8      | 7 | 0    |
| 9      | 8 | 1    |

The values are all the same but the data are organized differently. Clearly, two tables
are better than three tables in terms of space. As you can see from either two sets of 
tables, the maximum benefit we can achieve is $9$, which is entry of $B[3,8]$. In order to find out the exact
composition of the knapsack, we can work backwards from $i = 3$. With $i = 3$ and $w = 8$, $x_1 = 1$. Since
$w_1 = 5$ and $W = 8$, then we have $3$ left in knapsack in terms of weight. For $i = 2$ and $w = 3$ (because
we have only $3$ left in our knapsack weight capacity), $x_2 = 0$. Then, for $i = 1, w = 3$ (we still have $3$
budge left), $x_1 = 1$. Thus, our optimal choice for each item is $x_1 = 1, x_2 = 0, x_3 = 1$.

## Fractional knapsack problem

Another type of knapsack problem is the fractional knapsack problem. In this setting, *the item is divisible*. In
other words, we can take fraction of item. This problem 
can also be considered as a generalization of 0-x knapsack problem by not requiring $x_i$ has to be integer value.
In this case, we actually use the *greedy algorithm* paradigm instead of *dynamic programming* paradigm to solve the
problem. 

Let's use the same example as 0-x knapsack problem. In this case, we actually calculate the benefit per unit of weight
first:

$$
\frac{b_1}{w_1} = \frac{4}{3}, \frac{b_2}{w_2} = \frac{6}{8}, \frac{b_3}{w_3} = \frac{5}{5}
$$

as you can see, the first item gives the maximum benefit per unit of weight and we want to load this item as much as possible,
which is $W/w_1 = 8/3$. The reason we can use greedy algorithm to do this is because we can have fraction of item. If we don't
allow the fraction of item like we do in the 0-x knapsack problem, this appraoch will get suboptimal solution: we can only
have $2$ item $1$ (because $\lfloor\frac{8}{3}\rfloor = 2$) and the last $2$ knapsack weight capacity is not big enough to 
fit any item any more. Thus, the benefit we get in this case is $2*4 = 8$, which is smaller than $9$ our maximum benefit obtained
from *dynamic programming* approach.

## Links to resources

Here are some of the resources I found helpful while preparing this article:

- [UT-Dallas Introduction to Operations Research course material](https://www.utdallas.edu/~scniu/OPRE-6201/documents/DP3-Knapsack.pdf)
- [University of Nebraska CSCE 310J Data Structures and Algorithms lecture note](http://cse.unl.edu/~goddard/Courses/CSCE310J/Lectures/Lecture8-DynamicProgramming.pdf)