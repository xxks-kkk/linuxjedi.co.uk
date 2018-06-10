Title: How to write binary search correctly
Date: 2018-01-12 16:24
Category: Data Struct & Algo
Tags: algorithm, leetcode
Summary: How to write a binary search correctly on the first try

[TOC]

## Introduction

Binary search is a straightforward algorithm to understand but it is hard to code it right.
This is especially true given the forms of implementation on binary search can take on many.
In addition, there are many problems can be solved by binary search with slight adjustment.
Thus, it is not feasible to simply memorize the template of implementation without understanding.
In this post, We illustrate how we can use the loop invariant in combination with pre and
postcondition to code binary search correctly. One thing to note is that this post is drafted for 
practical purpose and it may not be theoretical rigorous.

## Term explanation

### Invariant

[Mike's post](https://reprog.wordpress.com/2010/04/25/writing-correct-code-part-1-invariants-binary-search-part-4a/) 
has an excellent description of [invariant](https://en.wikipedia.org/wiki/Invariant_(computer_science)), which I 
directly paste below:

> An invariant is a property that remains true throughout the execution of a piece of code.  It’s a statement about the state of a program — primarily the values of variables — that is not allowed to become false.  (If it does become false, then the code is wrong.)  Choosing the correct invariant — one that properly expresses the intent of an algorithm — is a key part of the design of code (as opposed to the design of APIs); and ensuring that the invariant remains true is a key part of the actual coding.  Roughly speaking, if your invariant properly expresses the intent of the algorithm, and if your code properly maintains the invariant, then that is enough for you to be confident that the code, if it terminates, yields the correct answer.  (Ensuring that it does in fact terminate is the job of the bound function.)

In short, an invariant is a condition that can be relied upon to be true during execution of a program, or during some portion of it. 
In practice, we formalize that invariant in terms of specific variables and values that appeared in the algorithm.

### Bound function

Again, [Mike's post](https://reprog.wordpress.com/2010/04/27/writing-correct-code-part-2-bound-functions-binary-search-part-4b/) has a nice
explanation of [bound function](https://en.wikipedia.org/wiki/Loop_variant):

> The bound function of a loop is defined as an upper bound on the number of iterations still to perform.  More generally, you can think of it as an expression whose value decreases monotonically as the loop progresses.  When it reaches zero (or drops below), you exit the loop.

### Precondition and postcondtion

We borrow definition from [Mike's post](https://reprog.wordpress.com/2010/04/30/writing-correct-code-part-3-preconditions-and-postconditions-binary-search-part-4c/) once again:

> When you invoke a function — or, all right, a method — you have a sense of what needs to be true when you invoke it, and what it guarantees to be true when it returns.  For example, when you call a function oneMoreThan(val), you undertake to ensure that val is an integer, and the function undertakes to ensure that the value it returns is one more than the one you passed in.  These two promises — the precondition and postcondition — constitute the contract of the function.  So:

> - The precondition is the promise that you make before running a bit of code;
> - The postcondition is the promise that the code makes after it’s been run.

## Binary search

### Problem statement

Before we actually implement our algorithm, we first need to make sure we understand the problem correctly. By understanding, we need to make
sure we understand the given input and the expectation of the output. Those will be translated into the precondition and postcondition for our algorithm.
Precondition helps us to design the algorithm and postcondition helps us to make sure we get the intended result.

Binary search problem is following: given an integer $X$ and integers $A_0, A_1, \dots, A_{N-1}$, which are presorted in ascending order, find
$i$ such that $A_i = X$, or return $i = -1$ if $X$ is not in the input. There might be multiple of $i$ with $A_i = X$.

### Implementation

The invariant for our binary search algorithm is: "if the target value $X$ is present in the array, then the target value is present in the current range."
As mentioned above, invariant is formalized using specific variables and values. Here, we need to decide the representation of "current range". This is
the place where the binary search has many ways of implementation. We use `low` and `high` to define the range and we use `n` to denote the length of array.
There are several popular formalization of the "current range":

```
1. A[low] <  A[i] <  A[high]
2. A[low] <= A[i] <  A[high]
3. A[low] <  A[i] <= A[high]
4. A[low] <= A[i] <= A[high]
```

Number 2 and 4 are the invariants that behind two most popular implementation of binary search you can find on the internet. 

#### Implementation 1

For 2, the equation means that $i \in [\text{low}, \text{high})$. Thus, `low` is initialized to `0` and `high` initialized to `n`. Thus, the invariant
for this is "If $X$ is at any position $i$ in $A$ (i.e., $A_i = X$) then `low <= i < high`". The implementation represents this invariant is below:

```python
def binarySearch(A, X):
    low, high = 0, len(A)
    while low < high:
        i = low + (high - low) // 2
        if X == A[i]:
            return i
        elif X > A[i]:
            low = i + 1
        else: # X < A[i]
            high = i
    return -1
```

In order to show the correctness of the above implementation, we need to make sure that we maintain the invariant through the execution of the function:

- The first thing is to establish the invariant that’s going to hold true for the rest of the function, so we set the variables `low` and `high` to appropriate values (i.e. the lowest and one pass the highest indexes of the whole $A$).
- We have ensured that the invariant is true when we first enter the loop. To show that stays true throughout the running of the function, we need to show that whenever it’s true at the top of the loop, it’s also true at the bottom. Here, our invariant is also the loop invariant.
- The first statement of the loop (assigning to `i`) does not affect any of the variables referenced by the invariant, so it can’t possibly cause the invariant to stop being true.
- What follows is a three-way `if` statement: we need to show that each of the three branches maintains the invariant.

    - The first branch (i.e., `X == A[i]`) covers the case where we have found the target. At this point, we’re returning from the function (and therefore breaking out of the loop) so we don’t really care about the invariant any more; but for what it’s worth, it remains true, as we don’t change the values of `low` or `high`.
    - The second branch (i.e., `X > A[i]`) is the first time we need to use non-trivial reasoning.  If we’re in this branch, we know that the condition guarding it was true, i.e., `X < A[i]`.  But because `A` is sorted in ascending order, we know that for all $j < i, A[j] <= A[i]$. 
    This means that $X$ > all A[j] with $j <= i$. Thus, the lowest position the target can be at is `A[i+1]`. In addition, since our invariant is $i \in [low, high)$,
    we can set `low` to `i+1`. 
    - The third branch follows the same form as the second: since we know that `X < A[i]` and that $A[j] >= A[i] \forall j > i$, we know the highest position the 
    target can be at is `A[i-1]`. However, our invariant insists that $i \in [low, high)$ with `high` being exclusive brace. Thus, we cannot set `high` to be `i-1`
    and instead, we set it to `i`. Doing so, we maintain our invariant unchanged.

- Since we’ve verified that all three branches of the `if` maintain the invariant, we know that the invariant holds on exiting that `if`. That means the invariant is
true at the bottom of the loop, which means it will be true at the start of the next time around the loop. And by induction we deduce that it always remains true.
- Finally, we break out of the loop when `low < high` is false, which means that the candidate range is empty (i.e. `low == high`). At this point, we know that the condition of the invariant (“If $X$ is at any position $i$ in $A$”) does not hold, so the invariant is trivially true; and we return the out-of-band value `-1`. [^1]

[^1]: The rigorous analysis on this binary search implementation can be found from [Frank's lecture notes on binary search](https://www.cs.cmu.edu/~rjsimmon/15122-s13/06-binsearch.pdf). He encodes [contract](https://www.cs.cmu.edu/~rjsimmon/15122-s13/02-contracts.pdf) 
directly into the implementation, which displays the loop invariant, precondition, and postcondition directly.

#### Implementation 2

For 4, the equation means that $i \in [\text{low}, \text{high}]$. Thus, `low` is initialized to `0` and `high` initialized to `n-1`. Thus, the invariant
for this is "If $X$ is at any position $i$ in $A$ (i.e., $A_i = X$) then `low <= i <= high`". The implementation represents this invariant is below:

```python
def binarySearch(A, X):
    low, high = 0, len(A) - 1
    while low <= high:
        i = low + (high-low) // 2
        if X == nums[i]:
            return i
        elif X > nums[i]:
            low = i + 1
        else:
            high = i - 1
    return -1
```

[Mike's post](https://reprog.wordpress.com/2010/04/25/writing-correct-code-part-1-invariants-binary-search-part-4a/) has done the similar invariant unchanged
analysis, which I'll skip for this implementation. Until now, we haven't touched on the concept of "bound function" and "postcondition" in our analysis. However,
that doesn't mean these two concepts are not important. Usually, "bound function" is used to prove our loop terminates (Mike's post talks about how to use 
"bound function" to show above implementation terminates; TopCoder link gives an example of why we need to show algorithm actually terminates). 
Next section, we'll see an example of checking postcondition is important to make sure we have correct return result.

## Binary search variations

In this section, we'll talk about two examples that use binary search and see how we can implement the binary search correctly if we are able to maintain the
invariant. 

### Example 1

The first example is [LC153. Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/description/).
Here, we are asked to find the minimum element given the rotated array. Suppose we have array `[0,1,2,4,5,6,7]` and there are seven ways of rotation:

```
0,1,2,4,5,6,7
7,0,1,2,4,5,6
6,7,0,1,2,4,5
5,6,7,0,1,2,4
4,5,6,7,0,1,2
2,4,5,6,7,0,1
1,2,4,5,6,7,0
```

The key observation is that if the middle value is greater than the left value, then the minimum value appears on the righthand-side of the middle value
(i.e., for `[4,5,6,7,0,1,2]`, the middle value is `7` and the minimum value `0` appears on the righthand-side of `7`).
Otherwise, the minimum value appears on the lefthand-side of the middle value. Like the previous section, we need to define `left` and `right` and then our invariant.
Here, we define the `left` as the `0` index of the array and `right` as the last index of the array. Then, our invariant can be formulated as: "the index of minimum
value (i.e., $i$) is always contained in the subarray denoted by `left` and `right` (i.e., $i \in [\text{left}, \text{right}]$)". In addition, our precondition
is: an array sorted in ascending order is rotated at some pivot unknown. Our postcondition is: the minimum value. Then, our implementation is:

```python
def findMin(self, nums):
    left = 0
    right = len(nums) - 1
    while left < right:
        if nums[left] < nums[right]:
            return nums[left]
        mid = left + (left - right) // 2
        if nums[mid] >= nums[left]:
            left = mid + 1
        else: # nums[mid] < nums[left]
            right = mid
    return nums[left]
```

We verify our invariant unchanged as follows:

- The invariant is unchanged before the first `if` when `nums[left] < nums[right]`. Here, we know that there is no rotation in the array (i.e.,
`[0,1,2,3,4,5,6,7]`) and we return `nums[left]`, which keeps invariant and satisfy the postcondition.
- For the second `if`: when `nums[mid] >= nums[left]`, by our observation, we know that the minimum value appears 
on the righthand-side of the middle value. `mid` value cannot be the minimum because `nums[mid] >= nums[left]`. Thus, we can set `left` to `mid + 1`
and still maintains our invariant unchanged.
- For the case when `nums[mid] < nums[left]`, we know that the minimum value appear on the lefthand-side of the middle value. However, `mid` value 
can be the minimum value and thus we set `right` to `mid` to maintain the invariant.
- The loop exit when `left == rigt`. Our invariant is $i \in [\text{left}, \text{right}]$, which is different from postcondition requires: 1. postcondition
asks us to return the actual minimum value instead of the index 2. We still haven't found the minimum value yet. The invariant states that
$i \in [\text{left}, \text{right}]$, which is $i \in [\text{left}, \text{left}]$ given `left == right`. Thus, minimum value can only appear on index pointed by
`left` and to meet the postcondition requirement, we `return nums[left]`.

Usually, for the iterative algorithm, the invariant is the same as the loop invariant. However, this example also shows the power of the postcondition. In the 
basic binary search above, maintaining the invariant naturally gives us the result that meets the postcondition requirement. However, for this example, our invariant
doesn't give us the required result. By checking the postcondition, we know what's the expected return is and it also indicates how we can find one.

### Example 2

The second example we are asked to find the index of the first number that is greater than the given target number in the array. Like basic binary search problem,
the array is sorted in ascending order. As always, let's consider some examples for this problem. Suppose we are given an array `[0,1,5,7,8,10,12,15]`, if the
target number is `3`, we should return `2`, which is the index of the first number that is greater than `3` (i.e., `5`). What about the target number is `16`?
In this case, there is no number in the array is greater than the target number, and we should return `-1`.

What's the invariant for this problem? Similar to the other binary search problem, the invariant is "the index $i$ of the first number that is greater than
the given target number in the array is in $[\text{low}, \text{high}]$". Thus, we can initialize `low` to be `0` and `high` to be `n`. Here, we set `high` to 
`n` because we need to maintain the invariant. For the case when there is no number in the array that is greater than the target number, we can think about
the first number that is greater than the target number happens one past the last index. Then, by our invariant, we need to include that number and thus, we set
our `high` to `n` instead of `n-1`. Then, the implementation follows:

```python
def findFirstGreaterTo(nums, target):
    low, high = 0, len(nums)
    while low < high:
        mid = low + (high - low) // 2
        if nums[mid] <= target:
            low = mid + 1
        else: # nums[mid] > target
            high = mid
    return -1 if high == len(nums) else high
```

The invariant is maintained as follows:

- Invariant is unchanged until the first `if`: `nums[mid] <= target`. There are two cases here: when `nums[mid] < target`, since the array is sorted in
ascending order and we are looking for the number that is greater than the target number, thus we can set `low` to `mid + 1` without breaking the invariant.
When `nums[mid] == target`, again we are looking for the first number that is greater than the target number, thus we can set `low` to `mid + 1`.
- When `nums[mid] > target`, we can set `high` to `mid` to maintain our invariant.
- The loop exit when `low == high`, since our invariant is the index of the first number greater than the target number is in $[\text{low}, \text{high}]$, which
is $[\text{high}, \text{high}]$ in this case. Our invariant still holds.

Once we exit the loop, we need to check our postcondition once again. Our postcondition asks us the index of the first number that is greater than the target number
if it is in the array and `-1` otherwise. However, during the initialization of `high`, we consider `n` represents the case when no such number exists and at the same
time, satisfies our invariant. Thus, before returning the result, we need to check whether `high` within the index range of the given array to satisfy the
postcondition constraint.

## Conclusion

In this post, we take a look at the technique that helps us implement the binary search correctly: maintain the invariant. Also, we emphasize the importance
of the postcondition to help us get the returen result correctly. We haven't empahsized the importance of bound function in the post but we should consider
it as well. There are two ways to check the loop indeed terminates: one is through reasoning similar what we have done in invariant analysis 
([Mike's post](https://reprog.wordpress.com/2010/04/27/writing-correct-code-part-2-bound-functions-binary-search-part-4b/) and 
[Paul's post](http://coldattic.info/post/95/) give us examples on how to do that); another way is by considering some special cases like there are only two 
elements in the array suggested by the TopCoder article below.[^2] Some details are left out in this post: 1. why use `mid = low + (high - low)//2` instead of
`mid = (low + high) // 2` [^3] 2. Use `A[low] <= A[i] <  A[high]` as an invariant is better than `A[low] <= A[i] <= A[high]`. [^4]

[^2]: Topcoder article offers an equivalent thought of thinking about invariant: predicate inquiry. For example, our last example invariant can be translated
into the predicate: "Is `nums[i]` greater than the target number?" Then, each element is tagged with either "yes" or "no". Then, the problem asks us to find
out the first element has tag "yes". The two elements special case shown in the article is "no,yes" array. Details see the article.

[^3]: The explanation can be found on [Rosettacode page](https://rosettacode.org/wiki/Binary_search) and 
[Frank's lecture notes on binary search on page L6.12](https://www.cs.cmu.edu/~rjsimmon/15122-s13/06-binsearch.pdf).

[^4]: [A comment on Mike's post](https://reprog.wordpress.com/2010/04/21/binary-search-redux-part-1/#comment-2178) sheds some insights.

## Reference

- [StackOverflow - What are the pitfalls in implementing binary search?](https://stackoverflow.com/questions/504335/what-are-the-pitfalls-in-implementing-binary-search) (has a short explanation of the importance of invariant with an example)
- [StackOverflow - Binary search and invariant relation](https://stackoverflow.com/questions/26564658/binary-search-and-invariant-relation) (has a nice example)
- [TopCoder - Binary Search](https://www.topcoder.com/community/data-science/data-science-tutorials/binary-search/) (think about binary search through predicate inquiry)
- [Loop Invariants and Binary Search](https://www.eecs.yorku.ca/course_archive/2013-14/W/2011/lectures/09%20Loop%20Invariants%20and%20Binary%20Search.pdf) 
(Nice illustration (i.e., "safe place") between precondition, loop invariant, postcondition)
- [Invariants and Proofs of correctness](http://www-inst.cs.berkeley.edu/~cs170/fa14/tutorials/tutorial1.pdf) (Gives relative formalization of our invariant
analysis in the post. Essentially, invariant is the same as the inductive hypothesis.)
- [Binary search and loop invariants](http://www.cs.cornell.edu/courses/cs2110/2014sp/L12-Sorting/L12cs2110BSearchInvariants.pdf) (Slide 6 is good: it tells us how 
to setup the terminate condition of the loop. Loop terminates when the invariant looks like the postcondition. This slide also gives example of writing terminate
condition as `while(low != high - 1)`).
- [Loop invariants](http://www.cs.cornell.edu/courses/cs2112/2015fa/lectures/lec_loopinv/index.html)