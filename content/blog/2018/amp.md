Title: On Write/Read/Space Amplification 
Date: 2018-04-05 0:45
Category: system
Tags: storage, LSM, 
Summary: Notes on write amplification, read amplification, space amplification
Status: Draft

[TOC]

In this post I'll try my best to explain three concepts *read amplification*, *write amplification*,
and *space amplification* from both theoretical and practical point of view. I'm new to storage area
and the post will inevitably have holes. Please help to patch if you find one.

## Definition

We borrow the definitions from paper ["Designing Access Methods: The RUM Conjecture"](https://stratos.seas.harvard.edu/files/stratos/files/rum.pdf) [^1]:

We define two types of data that appears in the storage system (i.e., data management system): *base data* and *auxiliary data*.

- *base data*: the main data stored in the system that we want to read or update.
- *auxiliary data*: auxiliary data (e.g., indexes) for performance improvements on reading/updating of *base data*.

For example, in a LSM-based key-value store, the key and its corresponding value are *base data*, and bloom filters that are used to improve read performance
is the *auxiliary data* (guards in PebblesDB is also *auxiliary data*). For a $B^+-$tree, the tree structure is the *auxiliary data* and the data pointed by the 
leaves of the tree is the *base data*. Now. let's take a look at the all three amplifications:

- **Read Amplification** (Read Overhead): the ratio between the total amount of data read including auxiliary and base data, divided by
the amount of retrieved data.

    Example: when traversing a $B^+-$Tree to access a tuple, the amplification is given by the ratio between the total data accessed (including the data read to traverse the tree and the base data) and the base data intended to be read.

- **Write Amplifcation** (Update Overhead): the ratio of the amount of update applied to the auxiliary data in addition to the updates to the base data to the
amount of update to the base data only. In other words, write amplification is the ratio between the size of the physical updates performed for one logical update, divided by the size of the logical update.

    Example: 1. Write amplification is calculated by dividing the updated data size (both base and auxiliary data) by the size of the updated base data.
    2. We update 2kb data but we actually perform 4kb write IO, and write amplification is 2.

- **Space Amplification** (Memory Overhead): the ratio between the space utilized for auxiliary and base data, divided by the space utilized for base data.

    Example: Space amplification is computed by dividing the overall size of the $B^+-$Tree by the base data size.

!!!note
    To see the difference between write amplification and the space amplification, let's consider a simple example. Consider memtable in LSM, when we
    add new key-value pair, we append them to the end of the memtable. Here, the write amplification is 1. However, since we never update the key in-place
    in LSM, we have space amplification greater than 1. For example, we append {2:3} pair first and then we update key 2 with value 4 {2:4}. In memtable,
    we only need to have {2:4} ideally but now we store both {2:3} and {2:4}. Thus, space amplification is 2 in this case. Same argument can be applied
    when we delete a key by appending *tombstone* flag. For another example, if we update a key-value pair in-place, both write amplification and 
    space amplification are 1.

## How to measure them





## Case Study: PebblesDB


## Further Reading


## Reference

- [Designing Access Methods: The RUM Conjecture](https://stratos.seas.harvard.edu/files/stratos/files/rum.pdf), [website](http://daslab.seas.harvard.edu/rum-conjecture/)
- [RocksDB Tuning Guide](https://github.com/facebook/rocksdb/wiki/RocksDB-Tuning-Guide)
- Mark Callaghan's talk at Highload [video](https://www.youtube.com/watch?v=6QfCCe-vgko), [slides](https://www.slideshare.net/profyclub_ru/mark-calla)
- [A Brief History of Log Structured Merge Trees](https://www.ristret.com/s/gnd4yr/brief_history_log_structured_merge_trees)

[^1]: The paper offers an intuitive view of the data structures presented in research about accessing methods (i.e., B-Tree, LSM, BW-Tree) that 
concern about the tree amplification factors. The paper can be used as a map to survey the research literature on the matter.