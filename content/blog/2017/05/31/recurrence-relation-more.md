Title: Solving recurrence relations (part 2)
Date: 2017-06-12 17:20
Category: Mathematics
Tags: recursion, math
Summary: Additional ways to solve recurrence relation

[Several months ago]({filename}/blog/2017/02/01/recurrence-relation.md), 
I breifly summarize the ways to solve recurrence relations. At the end of that post,
I indicate that different types of recurrence relation may require different kinds 
of treatments to solve them. Thus, this post will be the first "Downloadable Content (DLC)"
with the aim to solve the recurrence relation: $T(N) = 2T(N/2) + N$.

This recurrence relation comes from merge sort and the algorithm itself represents
a classic divide-and-conquer strategy: in order to sort $N$ elements, we can
sort $N/2$ elements first 
(i.e., *divide* the problem into smaller problems and solve recursively),
and then we merge two sorted $N/2$ elements back into one $N$ sorted array
(i.e., we patch toghter the answer in *conquer* phase.)

The exactly recurrence relation we try to solve is the following with assumption
that $N$ is a power of 2:

$$
\begin{eqnarray*} 
T(1) &=& 1 \\
T(N) &=& 2T(N/2) + N 
\end{eqnarray*}
$$

There are two ways to solve this recurrence relation:

## Method 1: Construct a telescoping sum

The goal of this method is to construct a telescoping sum (i.e see
[telescope series](https://en.wikipedia.org/wiki/Telescoping_series) to get a sense
of *telescoping*) with the aim
to find a relation between $T(N)$ and $T(1)$ (or the base cases, in general). 

Let's work through our example above to demonstrate this method. We divide the
recurrence relation through by $N$ and repeatively doing so for every possible $N$
(i.e. $N, N/2, N/4, \dots, 2, 1$) and see what we can get:

$$
\begin{eqnarray*} 
\frac{T(N)}{N} &=& \frac{T(N/2)}{N/2} + 1 \\
\frac{T(N/2)}{N/2} &=& \frac{T(N/4)}{N/4} + 1 \\
\frac{T(N/4)}{N/4} &=& \frac{T(N/8)}{N/8} + 1 \\
\vdots \\
\frac{T(2)}{2} &=& \frac{T(1)}{1} + 1 \\
\end{eqnarray*}
$$

We add up all the equations: we add all of the terms on the left-hand side and set
the result equal to the sum of all of the terms on the right-hand side. This leads
to a *telescoping* sum: all the terms that appear on both sides get cancelled. 
For example, the term $T(N/2)/(N/2)$ appears on both sides and thus cancels.
After everything is added, the final result is:

$$
\frac{T(N)}{N} = \frac{T(1)}{1} + \log N \cdot 1
$$

because all of the other terms cancel and there are $\log N$ equations, and so all
the $1$s at the end of these equations add up to $\log N$.

!!!note
    for this recurrence relation, it is necessary to divide through $N$ in order
    to get telescoping sum. However, how to construct telescoping sum is case by case.
    For instance, for a recurrence relation $NT(N) = (N+1)T(N-1) + 2cN$, we need to 
    divide $N(N+1)$. For a recurrence relation $T(N) = T(N-1) + cN$ [^1], we don't need to 
    do any division. We just need to use the recurrence relation repeatively for different
    $N$ to construct the telescoping sum (i.e. $T(N-1) = T(N-2) + c(N-1)$, 
    $T(N-2) = T(N-3) + c(N-2)$, and so on.)

[^1]: This recurrence relation is acutally a linear nonhomogeneous recurrence 
relation with constant coefficients. However, it cannot be solved by the method
I write up in the last post. I have no clue why. This recurrence relation is taken 
from MAW p243.

## Method 2: Iteratively substitute

For this method, we continuely substitute the recurrence relation on the right-hand
side with the hope to find a pattern of the general solution to the recurrence relation.

We have

$$
\begin{eqnarray*} 
T(N) &=& 2T(N/2) + N \\
T(N/2) &=& 2T(N/4) + N/2 
\end{eqnarray*}
$$

Then, we substitute the second equation back into the first equation's right-hand side and 
we get:

$$
\begin{eqnarray}
T(N) &=& 2(2T(N/4)+N/2) + N \nonumber \\
     &=& 4T(N/4) + 2N \label{eqn:1}
\end{eqnarray}
$$

Now, we can substitute $N/4$ into the main equation, we see that

$$
\begin{eqnarray}
T(N) &=& 4(2T(N/8)+N/4) + 2N \nonumber \\
     &=& 8T(N/8) + 3N \label{eqn:2}
\end{eqnarray}
$$

We can continuing this substitution, and if we observe the \ref{eqn:1} and \ref{eqn:2}
we can obtain the following pattern:

$$
T(N) = 2^kT(N/2^k) + k \cdot N
$$

using $k = \log N$, we obtain

$$
T(N) = NT(1) + N \log N = N\log N + N
$$
