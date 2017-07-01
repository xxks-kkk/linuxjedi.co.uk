Title: Mergesort
Date: 2017-07-01 23:33
Category: Data Struct & Algo
Tags: sorting, maw
Summary: summary for mergesort

We continue our journey in sorting. Specifically, we'll study
the mergesort in this post.

## Concept

The fundamental idea in the mergesort is merging two sorted lists into one. 
Because the lists are sorted, this can be done in one pass through the input, if 
the output is put in a third list. The basic merging algorithm takes two input
arrays $A$ and $B$, an output array $C$, and three counters, `Aptr`, `Bptr`, and
`Cptr`, which are initally set to the beginning of their respective arrays.
The smaller of `A[Aptr]` and `B[Bptr]` is copied to the next entry in $C$, and
the appropriate counters are advanced. When either input list is exhausted, the 
remainder of the other list is copied to $C$. 

The running time for merging is $O(N)$, because at most $N-1$ comparisons are made,
where $N$ is the total number of elements. To see this, note that every comparison
adds an element to $C$, except the last comparison, which adds at least two. 

Once we have this idea in mind, we can now describe our mergesort algorithm:

1. If $N=1$, there is only one element to sort, and we are done.
2. Otherwise, we recursively mergesort the first half and the second half. This gives
two sorted halves, which can then be merged together using the merging algorithm.

As you can see, our mergesort is a classic example of  divide-and-conquer strategy.
The problem is *divided* into smaller problems and solved recursively. The *conquering*
phase consists of patching together the answers.

The mergesort algorithm can be implemented as follows:

```c
void
merge(int A[],
      int tmpArray[],
      int lpos, // start of left half
      int rpos, // start of right half
      int rightEnd)
{
  int i, leftEnd, numElements, tmpPos;

  leftEnd = rpos - 1;
  tmpPos = lpos;
  numElements = rightEnd - lpos + 1;

  // main loop
  while(lpos <= leftEnd && rpos <= rightEnd)
    if(A[lpos] <= A[rpos])
      tmpArray[tmpPos++] = A[lpos++];
    else
      tmpArray[tmpPos++] = A[rpos++];

  while(lpos <= leftEnd) // Copy rest of first half
    tmpArray[tmpPos++] = A[lpos++];
  while(rpos <= rightEnd) // Copy rest of second half
    tmpArray[tmpPos++] = A[rpos++];

  for(i = 0; i < numElements; i++, rightEnd--) // copy tmpArray back
    A[rightEnd] = tmpArray[rightEnd];
}

void
msort(int A[],
      int tmpArray[],
      int left,
      int right)
{
  int center;
  if(left < right)
  {
    center = (left + right)/2;
    msort(A, tmpArray, left, center);
    msort(A, tmpArray, center+1, right);
    merge(A, tmpArray, left, center+1, right);
  }
}

void
mergeSort(int A[], int N)
{
  int *tmpArray;
  tmpArray = malloc(N*sizeof(int));
  assert(tmpArray);
  msort(A, tmpArray, 0, N-1);
  free(tmpArray);
}
```

Note that we use `tmpArray` working as array $C$ in our merging algorithm
to hold the merge result from our two input sorted arrays. One naive implementation
is that we declare a temporary array locally each time we call `Merge`. This can
be problematic because there could be $\log N$ temporary arrays active at any point.
This could be fatal on a machine with small memory and at the same time, we will
spend quite a lot time calling `malloc`. 

The trick for our implementation is that we declare a global temporary array
`tmpArray` of size $N$ at the very beginning. Then, we use `lpos`, `rpos`, `rightEnd`
to control the fraction of `tmpArray` will be used for merge step. This is a common
implementation trick, which will visit again immediately.

Like many other recursive algorithm, mergesort can also be implemented as
non-recursive algorithm as follows:

```c
void
mergeSortNonRecursive(int A[], int N)
{
  int *tmpArray;
  int subListSize, part1Start, part2Start, part2End;

  tmpArray = malloc(sizeof(int) * N);
  for(subListSize = 1; subListSize < N; subListSize *= 2)
  {
    part1Start = 0;
    while(part1Start + subListSize < N - 1)
    {
      part2Start = part1Start + subListSize;
      part2End = min(N - 1, part2Start + subListSize - 1);
      merge(A, tmpArray, part1Start, part2Start, part2End);
      part1Start = part2End + 1;
    }
  }
}
```

Let's take a look at an example for better understanding of the implementation
above. Suppose we want to sort the following list using mergesort: 
$31, 41, 59, 26, 53, 58, 97$. We start from very basic case: merge two sorted
list of one element, into a sorted list of two elements. For example,
`part1Start = 0`, `part2Start = 1`, `part2End = 1` for the first iteration
of while loop when `subListSize = 1`. Then, we call `merge` function and
use the fraction of `tmpArray` from `0` to `1` to hold the merge result.
We can print out the value `part1Start`, `part2Start`, and `part2End` to help
us better understand the flow of the program:

```
Before mergeSort: 31, 41, 59, 26, 53, 58, 97,
part1Start: 0
part2Start: 1
part2End: 1
part1Start: 2
part2Start: 3
part2End: 3
part1Start: 4
part2Start: 5
part2End: 5
part1Start: 0
part2Start: 2
part2End: 3
part1Start: 0
part2Start: 4
part2End: 6
After mergeSort: 26, 31, 41, 53, 58, 59, 97,
```

## Analysis  

The running time of mergesort is $O(N \log N)$, which can be obtained
by [solving the recurrence relation]({filename}/blog/2017/05/31/recurrence-relation-more.md):

$$
\begin{eqnarray*} 
T(1) &=& 1 \\
T(N) &=& 2T(N/2) + N 
\end{eqnarray*}
$$

One thing to notice that we assume $N = 2^k$ when solve the above recurrence relation.
The answer is almost identical even if $N$ is not a power of $2$.

## Final remarks

We hardly use mergesort for main memory sorts. The main problem is that merging two
sorted lists requires linear extra memory, and the additional work spent coping to the temporary
array and back, throughout the algorithm, has the effect of slowing down the sort considerably.
Thus, for serious internal sorting applications, we use quicksort instead.
Nevertheless, the merging routine is the cornerstone of most external sorting algorithms.

## Links to resources

Here are some of the resources I found helpful while preparing this article:

1. MAW Chapter 7

