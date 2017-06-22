Title: The tortoise and the hare
Date: 2017-06-18 20:20
Category: Data Struct & Algo
Tags: linked-list, leetcode, algorithm
Summary: Floyd's Tortoise and Hare w/ leetcode 142, 287

Recently, I start to work on [leetcode's problems](https://github.com/xxks-kkk/shuati). 
My goal is to solve two problems per day (mission possible, right?). The problems I'm looking
at are [142. Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/) and 
[287. Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/), 
which both can be solved by Folyd's Tortoise and Hare algorithm.

This post will try to take a deeper look at the correctness of the algorithm and
how to apply it to solve problems.

## Introduction

[Floyd's Tortoise and Hare algorithm](https://en.wikipedia.org/wiki/Cycle_detection#Floyd.27s_Tortoise_and_Hare)
is used with three purposes under the context of linked list:

1. Detect whether there is a cycle in the list
2. Find the starting point of the cycle (i.e. list 1->4->3->4, starting point is 4)
3. Decide the length of the cycle (i.e. 2 for above example)

The algorithm idea is following:

1. We use two pointers: tortoise and hare. Both start at the beginning of the list.
Hare runs twice as fas the tortoise.
2. If there is no-cycle, then hare will reach the finish line before the tortoise.
3. If there is a cycle, then hare will always be ahead and eventually he would
so far ahead that he laps the tortoise. That's the place we know we have a cycle in the list.
4. Once we detect the cycle, we send hare back to the beginning and advance both of 
them at the same speed until they meet again. The second meeting place, which we'll prove
immediately, is the entry point of the cycle. 
5. Then, one of them will keep moving to finish the victory lap to find the period
of the cycle.

The key difference when the list has a cycle is that at some point on the track, 
the hare will be at the same spot as the tortoise ...

## Proof of correctness

Let $\mu$ be the index of the start of the cycle, and let $\lambda$ be period of the
cycle. Let $i$ be the distance (i.e number of nodes) that tortoise travels and
let $x_i$ denotes the index of the node at which both tortoise and hare meet. $x_0$
is the first node in the list.

!!!note
    The notation here is similar to the concept in physics: distance vs. displacement.
    $i$ is the "distance" or the number of nodes that our character (tortoise or hare)
    has travelled since the beginning of the list and 
    $x_i$ is the "displacement" between the first node and the current node that our
    characters are at.

The key observation for showing the correctness of the algorithm lies in 
the following fact:

$$
\begin{equation}
x_{j+k\lambda} = x_j \text{ for all integers }j \ge \mu \text{ and } k \ge 0 \label{eqn:1}
\end{equation}
$$

This statement says that going around the loop any number of times takes you 
back to the same places as long as you start somewhere on the loop. Let's 
define the following set of notation here for future use:

- $y$ be the displacement between $x_{\mu}$ and $x_i$
- $m$ be the number of laps that tortoise have travelled before he meets
with hare at $x_i$
- $n$ be the number of laps that hare have travelled before he meets with 
tortoise at $x_i$

Since the hare runs twice as fast as the tortoise, then the distance hare travelled
when he meets with tortoise is $2i$ [^1]. Then, we have the following set of equations

$$
\begin{eqnarray}
i = \mu + y + m \cdot \lambda  \label{eqn:2} \\
2i = \mu + y + n \cdot \lambda \label{eqn:3}
\end{eqnarray}
$$

Now we subtract \ref{eqn:2} from \ref{eqn:3} and we have

$$
\begin{equation}
i = (n-m) \cdot \lambda \label {eqn:4}
\end{equation}
$$

Let's revisit our key observation \ref{eqn:1} and set $j = \mu$ and $k = (n-m)$, we have
$x_{\mu + (n-m)\lambda} = x_{\mu}$. Then, by \ref{eqn:4}, we have
$x_{\mu + i} = x_{\mu}$, which can be rewritten as $x_{i+\mu} = x_{\mu}$!!! This equation
tells us that the node at which the cycle begins (i.e $x+{\mu}$) is exactly the
same node as the node $\mu$ nodes away from the index at which tortoise and hare meet
(i.e. $x_i$).

!!!note
    The proof can be much shorter once we have $x_{2i} = x_i$. By \ref{eqn:1}, we
    also have $x_{i+k\lambda} = x_{2i}$, which leads to $k\lambda = i$. Since
    $x_\mu$ also meets the condition of \ref{eqn:1}, we have $x_{\mu + k\lambda} = x_\mu$.
    Substitutes $i = k\lambda$ in and get $x_{\mu+i} = x_\mu$. The conclusion follows.

[^1]: $x_{2i} = x_i$ immediately follows this statement. Then, if we let  
$l$ be the number of laps by which hare is ahead, then $2i = i + l \cdot \lambda$
and we have $i = l\lambda$. Then we set $k=l$ in \ref{eqn:1} and reach the same
conclusion. This way we don't need to define $y$,$m$,$n$, which can make proof
a little simpler notation-wise. 

## Two problems

### 142. Linked List Cycle II

The first problem is a straightforward application of the algorithm: 
Given a linked list, return the node where the cycle begins. If there is no cycle, return `NULL`.
The code is following

```c
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */
struct ListNode *detectCycle(struct ListNode *head) {
    if(head == NULL || head->next == NULL)
        return NULL;
    
    struct ListNode *tortoise;
    struct ListNode *hare;
    struct ListNode *curr;
    
    tortoise = hare = curr = head;
    
    while(hare != NULL && hare->next != NULL)
    {
        hare = hare->next->next;
        tortoise = tortoise->next;
        if (hare == tortoise)  // there is a cycle
        {
            while(curr != tortoise)
            {
                curr = curr->next;
                tortoise = tortoise->next;
            }
            return curr;  // find the entry location
        }
    }
    return NULL; // there is no cycle
}
```

### 287. Find the Duplicate Number

This problem is a lot tricker than a previous one: we need identify this problem
can also be solved by the Floyd's Tortoise and Hare algorithm, which is not obvious
at first glance

> Given an array nums containing $n + 1$ integers where each integer is 
> between $1$ and $n$ (inclusive), prove that at least one duplicate number 
> must exist. Assume that there is only one duplicate number, find the duplicate one.
> note: There is only one duplicate number in the array, but it could be repeated more than once.

The key point is to identify that the problem description is another way of 
describing a linked list, which requires somewhat deeper understanding of the
algorithm itself.

The algorithm is, in fact, used to find a cycle in a sequence of 
[iterated function](https://en.wikipedia.org/wiki/Iterated_function) values:

$$
x_0, x1 = f(x_0), x_2 = f(x_1), \dots, x_i = f(x_{i-1}), \dots
$$

For example, the sequence $1,3,4,2,1$ can be considered as a sequence of 
iterated function values with $x_0 = 1, x_1 = f(1) = 3, x_2 = f(3) = 4,
x_3 = f(4) = 2, x_4 = f(2) = 1$. Let's try another representation:

```
| index | 0 | 1 | 2 | 3 | 4 |
|-------|---|---|---|---|---|
| value | 1 | 3 | 4 | 2 | 1 |
```

Surprisingly, the function $f$ simply map the index to the corresponding values.
With this table, the above sequence can be converted as a linked list:

```
0 -> 1 -> 3 -> 2 -> 4
     ^              |
     |--------------|
```

This list is constructed by the definition of a sequence of iterated function values.
The arrow (`->`) is the function $f$. Then, we can apply our algorithm to solve 
this problem:

```c
int findDuplicate(int* nums, int numsSize) {
  int tortoise;
  int hare;
  tortoise = nums[0];
  hare = nums[nums[0]];
  while (tortoise != hare)
  {
    tortoise = nums[tortoise];
    hare = nums[nums[hare]];
  }
  hare = 0;
  while (tortoise != hare)
  {
    tortoise = nums[tortoise];
    hare = nums[hare];
  }
  return hare;
}
```

This implementation slightly deviates from the algorithm description above:

1. Tortoise and hare don't start from the same place at the beginning. This doesn't
matter really because eventually they will be in the loop.

2. We use `tortoise = nums[tortoise]` instead of `tortoise++` for advancing tortoise,
for example. This is the place where "a sequence of iterative function values" idea
appears. In fact, this is also how we constructed our linked list.

3. `hare = 0` not `hare = nums[0]` can be confusing. We can think about this from our linked
list representation: our list starts from $0$ (required by $f$, which maps index to value)
and if we starts from `hare = nums[0]`, that violates our algorithm.


[//]: # (http://mitchellkember.com/blog/post/tortoise-and-hare/)
[//]: # (This is due to the nature of our function $f$. The question says that there are $n+1$ integers with values between $1$ and $n$. Another way to think about this is that if there $n$ integers with values between $1$ and $n$, we'll not have duplicates (it's a permutation). However, we have extra one slot and we have to pick its value from $1$ to $n$, which leads to the duplicate.)