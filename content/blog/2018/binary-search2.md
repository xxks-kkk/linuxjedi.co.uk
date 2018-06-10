Title: Generalized binary search idea
Date: 2018-06-10 1:24
Category: Data Struct & Algo
Tags: algorithm, leetcode
Summary: Binary search idea can be generalized to other problems

[TOC]

## Introduction

In the [earlier post]({filename}/blog/2018/binary-search.md), we introduce the invariant concept to enable us
to solve the binary search problem on the very first try. In this post, we further elaborate the binary
search idea and introduce how we can use predicate + main theorem to solve more generalized binary search problem.

## Example

Let's consider an example, which utilizes the generalized idea of binary search mentioned in [TopCoder's article](https://www.topcoder.com/community/data-science/data-science-tutorials/binary-search/). The problem we look at is 
[Leetcode 658. Find K Closest Elements](https://leetcode.com/problems/find-k-closest-elements/description/): 
Let $A$ be a sorted array of $N$ values. We want to find the index $j$ such that the elements $A_j,A_{j+1},\dots,A_{j+k−1}$ 
have the $k$ closest values to the given target value $T$. 

The generalization of binary search is done by formalizing how we reduce the search space by half: binary search can be used
if and only if for all $x$ in the search space $S$ (i.e., the ordered set), $p(x)$ implies $p(y)$ for all $y > x$ ($p$ stands
for some predicate over $S$). TopCoder article calls this formalization as *main theorem*. We use this theorem to discard
the second half of search space. For example, in the most basic binary search problem in the ascending order array, our predicate $p$ 
is defined as: is the value at `i` smaller than `X`? If answer is yes, we discard the first half of the array (i.e., any values 
with index smaller than $i$) because the array is sorted in ascending order, any value before `A[i]` is also smaller than
`X`. By the same reasoning, if the answer is no, we discard the second half. Couple of observations we can make here:

- As you may have noticed, predicate is exactly what we check in the if-statement (e.g. `X > A[i]`).
- If `X < A[i]`, then for any $y > i$, we have `X < A[y]`, which exactly matches the main theorem and that's how we can discard
the second half of the array (i.e., search space).

Now, let's consider our example. What does it mean a selected subrange is optimal (i.e., $k$ closest values to $T$)? That means
that we can neither move the subrange to the right ($|A_{j+k} - T| > |A_j - T|$) nor move the subrange to the left 
($|A_{j+k-1} - T| > |A_{j-1} - T|$). In details, since the subrange includes $k$ closest values to $T$ and by moving it to right,
we exclude $A_{j}$ and include $A_{j+k}$. Since the selected subrange is optimal, we must have $|A_{j+k} - T| > |A_j - T|$.
Thus, we can formalize our predicate as: for a given index $j$, does $|A_{j+k} - T| > |A_j - T|$ hold? Another piece of information
we need for binary search is the invariant. From the question description we can see that the key to this question is finding
$j$. Thus, our invariant is: the index of the first number that is among the k closest values for the given target $T$ 
(i.e., $j$) is in $[\text{left}, \text{right}]$.

Now, we have to show that *main theorem* holds given our predicate formalization. Let's discuss this point
in details:

- When $|A_{j+k} - T| > |A_j - T|$ is true:

    - If $A$ is sorted in ascending order, then we have three possible cases:

        - $T < A_j < A_{j+k}$. In this case, we have $A_{j+k} - T > A_j - T$. Let $d$ be an integer with range
        $0 < d < k$, then we have
        $A_{j+k+d} - T > A_{j+k} - T > A_{j+d} - T > A_{j} - T$. In other words, for any index $i > j$, our predicate
        holds ($|A_{i+k} - T| > |A_i - T|$). Thus, we can directly discard the second half of the array. Note that
        we still want to keep $j$ because it might be the optimal $j$ we are looking for.
        - $A_j < T < A_{j+k}$. In this case, we have $A_{j+k} - T > T - A_j$. Then, we have 
        $A_{j+k+d} - T > A_{j+k} - T > T - A_j > T - A_{j+d}$. Then the predicate still holds for $i > j$.
        - $A_j < A_{j+k} < T$. This is impossible given our predicate condition.

    - If $A$ is sorted in descending order, we also have three possible cases:

        - $T > A_j > A_{j+k}$. In this case, we have $T - A_{j+k} > T - A_j$, which leads to 
        $T - A_{j+k+d} > T - A_{j+k} > T - A_{j+d} > T - A_j$. Again, our predicate holds for any index $i > j$ and
        we can discard the second half of the array.
        - $A_j > T > A_{j+k}$. In this case, we have $T - A_{j+k} > A_j - T$. We have
        $T - A_{j+k+d} > T - A_{j+k} > A_j - T > A_{j+d} - T$. Predicate holds.
        - $A_j > A_{j+k} > T$. Impossible.

!!!note
    The reason we have $0 \le d \le k$ is that in the extreme case, we have $j = N - k$ (otherwise, we won't have $k$ elements)
    and it is unnecessary to have $d$ goes beyond $k$.

- When $|A_{j-1} - T| > |A_{j+k-1} - T|$ is true:

    - If $A$ is sorted in ascending order, then we have three possible cases:

        - $T < A_{j-1} < A_{j+k-1}$. Impossible.
        - $A_{j-1} < T < A_{j+k-1}$. In this case, we have $T - A_{j-1} > A_{j+k-1} - T$. Then, let $d$ be an integer with
        range between 0 and $j-1$. We have $T - A_{j-1-d} > T - A_{j-1} > A_{j+k-1} - T > A_{j+k-1-d} - T$. Thus, for any
        index $i <= j$, we have $|A_{i-1} - T| > |A_{i+k-1} - T|$. This suggests that we can discard first half of the array.
        - $A_{j-1} < A_{j+k-1} < T$. We have $T - A_{j-1} > T - A_{j+k-1}$, which implies 
        $T - A_{j-1-d} > T - A_{j-1} > T - A_{j+k-1-d} > T - A_{j+k-1}$, which again the predication holds.

    - If $A$ is sorted in descending order, then we have three possible cases:

        - $T > A_j > A_{j+k}$. Impossible.
        - $A_j > T > A_{j+k}$. In this case, we have $A_{j-1} - T > T - A_{j+k-1}$, which implies that 
        $A_{j-1-d} - T > A_{j-1} - T > T - A_{j+k-1} > T - A_{j+k-1-d}$. Predication holds: for all index $i <= j$,
        we have $|A_{i-1} - T| > |A_{i+k-1} - T|$, which means we can discard first half of the array and move subrange to the right.
        - $A_j > A_{j+k} > T$. In this case, we have $A_{j-1} - T > A_{j+k-1} - T$, which imples that
        $A_{j-1-d} - T > A_{j-1} - T > A_{j+k-1-d} - T > A_{j+k-1} - T$. Predication holds.

Once we verify the predication satisifies the *main theorem*, the only thing we left is to build the connection between the
invariant and predication, and make sure the invariant holds during the loop execution. Let's first list out the code:

```cpp
class Solution {
public:
    vector<int> findClosestElements(vector<int>& arr, int k, int x) {
        int left = 0;
        int right = arr.size() - k;
        while (left < right)
        {
            int mid = left + (right - left) / 2;
            if (fabs(x - arr[mid]) <= fabs(arr[mid+k] - x))
            {
                right = mid;
            }
            else if (fabs(x - arr[mid-1]) > fabs(x - arr[mid+k-1]))
            {
                left = mid + 1;
            }
        }
        return vector<int>(arr.begin() + left, arr.begin() + left + k);
    }
};
```

$|A_{j+k} - T| > |A_j - T|$ means we cannot move the subrange to the right to obtain the optimal subrange. We also show that
under the condition, we can discard the second half of the array. `mid` represents $j$ in our condition and by not moving
subrange to right, we are saying that the optimal $j$ has to be the left of `mid`. This implies that we can safely move
set $\text{right}$ to `mid` and still maintains the invariant during the loop. On the other hand, $|A_{j-1} - T| > |A_{j+k-1} - T|$
means that we cannot move the subrange to the left to obtain the optimal subrange. We also show that the inequality allows us
to discard the first half of the array. Since for given $j$ (`mid`), we have $|A_{j-1} - T| > |A_{j+k-1} - T|$. We cannot
move subrange (indicating by $j$ or `mid`) to the left; we have to move to right. Thus, we set
$\text{left}$ to `mid+1` to narrow down the search space while maintainng the invariant unchanged.

!!!note
    Notice that in the code we actually use $|A_{j+k} - T| \ge |A_j - T|$ instead of $|A_{j+k} - T| > |A_j - T|$. The reason
    is because whenever there is a tie, the smaller elements are always preferred. Consider `[1,2,3,4,5]` with $k = 4$ and $
    T = 3$. Then, both `[1,2,3,4]` and `[2,3,4,5]` are the closest $k$ elements to the $T$ and sum of the elements to $T$ distance
    are the same, which is a tie. In this case, we prefer `[1,2,3,4]`. If we strictly follow the predicate, we end up with
    `[2,3,4,5]`. Switching $|A_{j+k} - T| > |A_j - T|$ to $|A_{j+k} - T| \ge |A_j - T|$ still maintains the invariant in the loop
    because when $|A_{j+k} - T| = |A_j - T|$, shifting the subrange to the right doesn't give any improvement and by set `right`
    to mid, we still ensure that the optimal $j$ falls inside $[\text{left}, \text{right}]$.

One thing to note that `while(left < right)` means we haven't found the optimal $j$ yet, which implies that we have to
either move the subrange to left or move the subrange to right. This provides us the further opportunity to optimize the above
code:

```cpp
class Solution {
public:
    vector<int> findClosestElements(vector<int>& arr, int k, int x) {
        int left = 0;
        int right = arr.size() - k;
        while (left < right)
        {
            int mid = left + (right - left) / 2;
            if (fabs(x - arr[mid]) <= fabs(arr[mid+k] - x))
            {
                right = mid;
            }
            else
            {
                left = mid + 1;
            }
        }
        return vector<int>(arr.begin() + left, arr.begin() + left + k);
    }
};
```

In the first version, we check two conditions explicitly and do nothing if both conditions are not true. However,
as we state in the previous paragraph, since we are still in the `while` loop, that means one of those two conditions will be true. 
In other words, there is no such case that both conditions are false and we are still in the loop. Thus, we can get rid of 
one of the conditions and use `else` instead. Another way of thinking is that we do nothing if both conditions are failed
and thus this third do-nothing case can be combined with the second `else if (fabs(x - arr[mid-1]) > fabs(x - arr[mid+k-1]))` condition to form a `else` statement.

In fact, we can even get rid of the `fabs` and finally optimize our code into

```cpp
class Solution {
public:
    vector<int> findClosestElements(vector<int>& arr, int k, int x) {
        int left = 0;
        int right = arr.size() - k;
        while (left < right)
        {
            int mid = left + (right - left) / 2;
            if (x - arr[mid] <= arr[mid+k] - x)
            {
                right = mid;
            }
            else
            {
                left = mid + 1;
            }
        }
        return vector<int>(arr.begin() + left, arr.begin() + left + k);
    }
};
```

To see why this one is correct, we have to resort back to our predicate proof. In the second optimization, we get 
rid of $|A_{j-1} - T| > |A_{j+k-1} - T|$ and focus ourselves on $|A_{j+k} - T| > |A_j - T|$ only. Then, we
get rid of the absolute sign and rewrite the inequalities based on the sorted order of the given array, which
are the same inequalities from our previous predicate proof:

| Sorted Order | Inequalities                                                                               |
|--------------|--------------------------------------------------------------------------------------------|
| ascending    | $$\begin{eqnarray*}A_{j+k} - T & > & A_j - T \\A_{j+k} - T & > & T - A_j\end{eqnarray*}$$  |
| descending   | $$\begin{eqnarray*}T - A_{j+k} & > & T - A_j \\ T - A_{j+k} & > & A_j - T\end{eqnarray*}$$ |

Let's first consider the ascending case. One can observe that the left-hand side of the inequalities are the same:
$A_{j+k} - T$ and only right-hand side of the inequalities are different. If $T > A_j$, that means
$T - A_j < 0$ and thus $A_{j+k} - T > T - A_j$ implies $A_{j+k} - T > A_j - T$ 
(a number that is greater than a positive number must be greater than a negative number) and we only need to check
$A_{j+k} - T > T - A_j$ in the code. If $T < A_j$, that means we should move the subrange to the left (to get
$j$ closer to the index of $T$), which is exactly the same thing we are going to do when $T > A_j$: `right = mid`.

For the descending case, we have to realize that descending is just the reverse of the ascending. Mathematically,
this means that $A_{j+k}$ and $A_{j}$ are swapped. For example, consider `[1,2,3,4,5]` with $A_j = 1$ and $A_{j+k} = 5$.
However, for the descending `[5,4,3,2,1]`, $A_j = 5$ and $A_{j+k} = 1$. Thus, the `if` condition is
really checking $A_{j} - T > A_{j+k} - T$, which is equivalent as $T - A_{j} < T - A_{j+k}$, which is one of the inequalities
listed in the table above. Like the ascending case, if $T > A_j$,
then $T - A_{j+k} > T - A_j$ entails $T - A_{j+k} > A_j - T$; if $T < A_j$, we necessarily want to shift the subrange to left.

Thus, $|A_{j+k} - T| > |A_j - T|$ can be further simplified to $A_{j+k} - T > T - A_j$ and that leads to our final optimized
solution.

## Conclusion

We give one example showing the essence of the binary search: main theorem, which is a formalization of how we discard values. 
Predicate helps us to find what to write in the `if` statement and invariant helps us to make sure we find the correct value. 
In this post, we go through a relative formal proof of the correctness of our predicate. One thing to note that, the proof
is in fact induction: we use $d$ to show inequalities hold for any index $i > j$. A nicer but equivalent way we can do is simply use
the induction and show $p(j+1)$ holds given $p(j)$ is correct (we actually do $p(j+d)$ holds given $p(j)$ is correct). Another point 
we should point out that we can derive the invariant
from predicate: we try to find the index of the first number that is among the k closest values for the given target $T$. This is 
the exact same number that will **first** give "yes" response to our predicate.

## Reference

- [TopCoder's post](https://www.topcoder.com/community/data-science/data-science-tutorials/binary-search/)
- [Stackexchange post: Searching a sorted array to find the k closest values to a target value T](https://cs.stackexchange.com/questions/77364/searching-a-sorted-array-to-find-the-k-closest-values-to-a-target-value-t?rq=1)