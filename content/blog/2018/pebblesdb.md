Title: "PebblesDB: Building Key-Value Stores using Fragmented Log-Structured Merge Trees"
Date: 2018-03-30 0:45
Category: system
Tags: papers, storage, LSM, 
Summary: "PebblesDB: Building Key-Value Stores using Fragmented Log-Structured Merge Trees" paper reading

[TOC]

## Introduction

- One fundamental problem is the high write amplification of key-value stores for write-intensive workloads. 

- Write amplification = the ratio of total write IO performed by the store to the total user written

- High write amplification is bad

    - increases the load on storage devices such as SSDs, which have limited write cycles before the bit error rate becomes unacceptable
    - results in frequent device wear out and high storage 
    - reduces write throughput

        RocksDB write throughput is 10% of read throughput thanks to write amplifcation

!!!note
    虽然LSM的写放大最近被研究很多，但是就写放大本身而言，是一个很古老的问题。在计算机体系中，如果相邻两层的处理单元不一致或者应用对一致性等有特殊的需求，就很可能出现写放大问题。比如CPU cache和内存cell，文件系统block和磁盘扇区，数据库block和文件系统block，数据库redo/undo，文件系统journal等.

- Reduce write amplification inuition: log-structured merge trees (LSM) data structures is the root cause to the write amplification

    LSM stores maintain data in sorted order on storage, enabling efficient querying of data. However, when new data is inserted into an LSM-store, existing data is rewritten to maintain the sorted order, resulting in large amounts of write IO.

- Key idea to reduce write amplification:

    - Combine LSM with skip list: fragmenting data into smaller chunks that are organized using guards on storage. Guards allow FLSM to find keys efficiently. [^1]

- Why the idea can improve write throughput intuitively:

    - Write operations on LSM stores are often stalled or blocked while data is compacted (rewritten for better read performance); by drastically reducing write IO, FLSM makes compaction signi￿cantly faster, thereby increasing write throughput.

## Background

### Key-Value Store Operations

- The `get(key)` operation returns the latest value associated with key.

- The `put(key, value)` operation stores the mapping from key to value in the store. If key was already present in the store, its associated value is updated.

- Some key-value stores such as LevelDB provide an iterator over the entire key-value store. `it.seek(key)` positions the iterator `it` at the smallest key 
`>= key`. The `it.next()` call moves `it` to the next key in sequence. The `it.value()` call returns the value associated with the key at the current iterator position.

- The `range_query(key1, key2)` operation returns all key-value pairs falling within the given range. Range queries are often implemented by doing a `seek()` to `key1` and doing `next()` calls until the iterator passes `key2`.

### LSM

- LSM [^2] is treated as a replacement for B+ Tree

- Why not B+ Tree:

    - low write throughput: B+ Trees are a poor fit for write-intensive workloads: updating the tree requires multiple random writes (10-100X slower than sequential writes).
    - high write amplification (61X write amplification)

- The log-structured merge trees (LSM) data structure takes advantage of high sequential bandwidth by only writing sequentially to storage. 
Writes are batched together in memory and written to storage as a sequential log (termed an __sstable__). Each sstable contains a sorted sequence of keys.

    ![sstable]({filename}/images/sstable.png) 

!!!note
    A "Sorted String Table" then is exactly what it sounds like, it is a file which contains a set of arbitrary, sorted key-value pairs inside. Duplicate keys are fine, there is no need for "padding" for keys or values, and keys and values are arbitrary blobs. Read in the entire file sequentially and you have a sorted index. Optionally, if the file is very large, we can also prepend, or create a standalone `key:offset` index for fast access. That's all an SSTable is: very simple, but also a very useful way to exchange large, sorted data segments.

- Sstables on storage are organized as hierarchy of __levels__. Each level contains multiple sstables, and has a maximum size for its sstables.

    In a 5-level LSM, Level 0 is the lowest level and Level 5 is the highest level. The amount of data (and the number of sstables) in each level increases as the levels get higher. The last level in an LSM may contain hundreds of gigabytes. Application data usually flows into the lower levels and is then compacted into the higher levels. The lower levels are usually cached in memory.

- LSM maintains the following invariant at each level: all sstables contain disjoint sets of keys.

    For example, a level might contain three sstables: $[1 \dots 6], [8 \dots 12]$, and $[100 \dots 105]$. Each key will be present in exactly one sstable on a given level. As a result, locating a key requires only two binary searches: one binary search on the starting keys of sstables (maintained separately) to locate the correct sstable and another binary search inside the sstable to find the key. If the search fails, the key is not present in that level.

#### LSM Operations

- `get()` returns the latest value of the key

    Since the most recent data will be in lower levels, the key-value store searches for the key level by level, starting from Level 0; if it finds the key, it returns the value. Each key has a sequence number that indicates its version. Finding the key at each level requires reading and searching exactly one sstable.

- `seek()` and `next()` require positioning an iterator over the entire key-value store. 

    implemented using multiple iterators (one per level); each iterator is first positioned inside the appropriate sstable in each level, and the iterator results are merged. The `seek()` requires finding the appropriate sstables on each level, and positioning the sstable iterators. The results of the sstable iterators are merged (by identifying the smallest key) to position the key-value store iterator. The `next()` operation simply advances the correct sstable iterator, merges the iterators again, and re-positions the key-value store iterator.

- `put()` writes the key-value pair, along with a monotonically increasing sequence number, to an in-memory skip list called the __memtable__. When the memtable reaches a certain size, it is written to storage as a sstable at Level 0. When each level contains a threshold number of files, it is compacted into the next level. 

    Assume Level 0 contains `[2, 3]` and `[10, 12]` sstables. If Level 1 contains `[1,4]` and `[9, 13]` sstables, then during compaction, Level 1 sstables are rewritten as `[1, 2, 3, 4]` and `[9, 10, 12, 13]`, merging the sstables from Level 0 and Level 1. Compacting sstables reduces the total number of sstables in the key-value store and pushes colder data into higher levels. The lower levels are usually cached in memory, thus leading to faster reads of recent data.

!!!note
    Think about *memtable* as in-memory SSTable.

- Updating or deleting keys in LSM-based stores does not update the key in place, since all write IO is sequential. Instead, the key is inserted once again into the memtable with a higher sequence number; a delete key is inserted again with a special flag (often called a __tombstone__ flag). Due to the higher sequence number, the latest version of the flag will be returned by the store to the user.

### Write Amplification: Root Cause

![sstable]({filename}/images/lsm-root-cause.png) 

- The root cause for write amplification: multiple rewrites of sstables during compaction. In other words, sstables can be rewritten multiple
times when new data is compacted into them.

    For example, when compaction happens from $t_1$ to $t_2$, sstable with `[1,100]` has to be rewritten to `[1,10,100]` and
    sstable with `[200,400]` has to be rewritten as `[200,210,400]` (i.e., We have to read `[10,210]`, `[1,100]`, `[200,400]` out of levels, merge sort them, and write them back.)

    L0文件里面包含的key同时在L1层的多个文件（甚至全部文件）被包含，所以如果想把L0下推到L1，那么就需要将整个L0/L1文件内的key读出来重新排序写入到L1。典型情况下，L0数据量是L1的1/10，为了这么点数据量重写所有数据显然不划算。L1...Ln道理类似

!!!note
    放大问题的本质是一个系统对“随时全局有序"的需求有多么的强烈。所谓随时，就是任何的写入都不能导致系统无序；所谓全局，即系统内任意元单位之间都要保持有序。B-Tree系列是随时全局有序的典型代表，而Fractal tree打破了全局的约束，允许局部无序，提升了随机写能力；LSM系列进一步打破了随时的约束，允许通过后台的compaction来整理排序。在LSM这种依靠后台整理来保序的系统里面，系统对序的要求越强烈，写放大越严重。PebblesDB针对写放大提出的解决方案是弱化全局有序的约束，其将每一层进行分段，每个段称为一个guard，guard之间没有重叠的key，且每层的guard之间要求保序，但是guard内部可以无序。

## Fragmented Log-Structured Merge Tree (FLSM) 

- FLSM counters mutlple rewrites of sstables by fragmenting sstables into smaller units. Instead of rewriting the sstable, FLSM’s compaction simply appends a new sstable fragment to the next level. Doing so ensures that data is written exactly once in most levels

!!!note
    Here, I'm guessing "append" really means pointer change from one node to another. Thus, the only time IO is performed when the data is first written
    to sstable at a level.

### Guards

- In the classical LSM, each level contains sstables with disjoint key ranges (i.e., each key will be present in exactly one sstable). Maintaining this invariant is the root cause of write amplification, as it forces data to be rewritten in the same level.

- The FLSM data structure discards this invariant: each level can contain multiple sstables with overlapping key ranges, so that a key may be present in multiple sstables. To quickly find keys in each level, FLSM organizes the sstables into guards (similar to level concept in skip list)

- Each level contains multiple guards. Guards divide the key space (for that level) into disjoint units. Each guard $G_i$ has an associated key $K_i$, chosen from among keys inserted into the FLSM. Each level in the FLSM contains more guards than the level above it; the guards get progressively more fine-grained as the data gets pushed deeper and deeper into the FLSM. As in a skip-list, if a key is a guard at a given level $i$, it will be a guard for all levels $> i$.

- Each guard has a set of associated sstables. Each sstable is sorted. If guard $G_i$ is associated with key $K_i$ and guard $G_{i+1}$ with $K_{i+1}$, an sstable with keys in the range $[K_i,K_{i+1})$ will be attached to $G_i$ . Sstables with keys smaller than the first guard are stored in a special sentinel guard in each level. The last guard$G_n$ in the level stores all sstables with keys $\ge K_n$ . Guards within a level never have overlapping key ranges. Thus, to find a key in a given level, only one guard will have to be examined.

- In FLSM compaction, the sstables of a given guard are (merge) sorted and then fragmented (partitioned), so that each child guard receives a new sstable that fits into the key range of that child guard in the next level.

![guards]({filename}/images/guards.png) 

!!!note
    Some observations about Figure 3:

    - A `put()` results in keys being added to the in-memory memtable (not shown). Eventually, the memtable becomes full, and is written as an sstable to Level 0. Level 0 does not have guards, and collects together recently written sstables.
    
    - Each level has a sentinel guard that is responsible for sstables with keys < than the first guard.
    
    - Data inside an FLSM level is partially sorted: guards do not have overlapping key ranges, but the sstables attached to each guard can have overlapping key ranges.（In level 3 Guard: 5, `[5,35,40]` and `[7]` are overlapping)

#### Selecting Guards

- In the worst case, if one guard contains all sstables, reading and searching such a large guard (and all its constituent sstables) would cause an un-acceptable increase in latency for reads and range queries

- guards are not selected statically; guards are selected probabilistically from inserted keys, preventing skew.

- Current selection policy: 

    - if the guard probability is 1/10, one in every 10 inserted keys will be randomly selected to be a guard.
    - The guard probability is designed to be lowest at Level 1 (which has the fewest guards), and it increases with the level number (as higher levels have more guards)

- if a key $K$ is selected as a guard in level i, it becomes a guard for all higher levels $i + 1, i + 2$ etc. The guards in level $i + 1$ are a strict superset of the guards in level $i$ (in Figure 3, key 5 is chosen as a guard for Level 1; therefore it is also a guard for levels 2 and 3.)

#### Inserting and Deleting Guards

- Guards are inserted asynchronously into FLSM

- When guards are selected, they are added to an in-memory set termed the *uncommitted guards*. Sstables are not partitioned on storage based on (as of yet) uncommitted guards; as a result, FLSM reads are performed as if these guards did not exist. At the next compaction cycle, sstables are partitioned and compacted based on both old guards and uncommitted guards; any sstable that needs to be split due to an uncommitted guard is compacted to the next level. At the end of compaction, the uncommitted guards are persisted on storage and added to the full set of guards. Future reads will be performed based on the full set of guards.

- guard deletion was not required

- Guard deletion is also performed asynchronously similar to guard insertion. Deleted guards are added to an in-memory set. At the next compaction cycle, sstables are re-arranged to account for the deleted guards. Deleting a guard G at level i is done lazily at compaction time. During compaction, guard G is deleted and sstables belonging to guard G will be partitioned and appended to either the neighboring guards in the same level i or child guards in level i + 1. Compaction from level i to i + 1 proceeds as normal (since G is still a guard in level i + 1). At the end of compaction, FLSM persists metadata indicating G has been deleted at level i. If required, the guard is deleted in other levels in a similar manner. Note that if a guard is deleted at level i, it should be deleted at all levels < i; FLSM can choose whether to delete the guard at higher levels > i.

### FLSM Operations

-  `get()` operation first checks the in-memory memtable. If the key is not found, the search continues level by level, starting with level 0. During the search, if the key is found, it is returned immediately; To check if a key is present in a given level, binary search is used to find the single guard that could contain the key. Once the guard is located, its sstables are searched for the key. Thus, in the worst case, a `get()` requires reading one guard from each level, and all the sstables of each guard.

- Range queries require collecting all the keys in the given range. FLSM first identifies the guards at each level that intersect with the given range. Inside each guard, there may be multiple sstables that intersect with the given range; a binary search is performed on each sstable to identify the smallest key overall in the range. Identifying the next smallest key in the range is similar to the merge procedure in merge . When the end of range query interval is reached, the operation is complete, and the result is returned to the user.

- `put()` adds data to an in-memory memtable. When the memtable gets full, it is written as a sorted sstable to Level 0. When each level reaches a certain size, it is compacted into the next level. 

- Similar to LSM, updating or deleting a key involves inserting the key into the store with an updated sequence number or a deletion flag respectively. the deletion of the key does not result in deletion of the related guard; deleting a guard will involve a signi￿cant amount of compaction work. Thus, empty guards are possible.

- Compaction:

    - The sstables in the guard are first (merge) sorted and then partitioned into new sstables based on the guards of the next level; the new sstables are then attached to the correct guards. 

        Assume a guard at Level 1 contains keys `[1, 20, 45, 101, 245]`. If the next level has guards 1, 40, and 200, the sstable will be partitioned into three sstables containing `[1, 20]`, `[45, 101]`, and `[245]` and attached to guards 1, 40, and 200 respectively.

    - New sstables are simply added to the correct guard in the next level.

    - Two exceptions to no-rewrite rule:

        - at the highest level (e.g,. Level 5) of FLSM, the sstables have to be rewritten during compaction; there is no higher level for the sstables to be partitioned and attached to.
        - for the second-highest level (e.g,. Level 4), FLSM will rewrite an sstable into the same level if the alternative is to merge into a large sstable in the highest level 

### Limitations

- Since `get()` and range query operations need to examine all sstables within a guard, the latency of these operations is increased in comparison to LSM.

## Building PebblesDB over FLSM

Due to the limitation of FLSM, several existing techniques are applied to improve read performance (i.e., `put()` and range query operations)

### Improving Read Performance

- Cause: `get()` in FLSM causes all the sstables of one guard in each level to be examined. In contrast, in LSM, exactly one sstable per level needs to be examined.

- Improvement technique:

    - Sstable Bloom Filters:

        - A Bloom filter is a space-efficient probabilistic data structure used to test whether an element is present in a given set in constant time
        - A bloom filter can produce false positives, but not false negatives (i.e., the key is in sstables but bloom filters say no)
        - PebblesDB attaches a bloom filter to each sstable to e￿ciently detect if a given key could be present in the sstable. 

### Improving Range Query Performance

- Cause: require examining all the sstables of a guard for FLSM. Since LSM stores examine only one sstable per level, FLSM stores have significant overhead for range queries

- Improvement technique:

    - Seek-Based Compaction
    - Parallel Seek

## Reference

- [PebblesDB: Building Key-Value Stores using Fragmented Log-Structured Merge Trees](http://www.cs.utexas.edu/~vijay/papers/sosp17-pebblesdb.pdf)

- [SSTable and Log Structured Storage: LevelDB](https://www.igvita.com/2012/02/06/sstable-and-log-structured-storage-leveldb/)

- [PebblesDB读后感](https://zhuanlan.zhihu.com/p/32225460)

## Further Reading

- [PebblesDB Slides](https://www.cs.utexas.edu/~vijay/papers/pebblesdb-sosp17-slides.pdf)
- [RocksDB Tuning Guide](https://github.com/facebook/rocksdb/wiki/RocksDB-Tuning-Guide)

[^1]: [CMU slides](https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/skiplists.pdf), [this post](http://igoro.com/archive/skip-lists-are-fascinating/), and
[UCI reading](https://www.ics.uci.edu/~pattis/ICS-23/lectures/notes/Skip%20Lists.pdf) give an intuitive introduction to skip list.

[^2]: [This post](http://www.benstopford.com/2015/02/14/log-structured-merge-trees/) contains a plenty of good pointers to get familiar with LSM. Also,
[cLSM paper](http://webee.technion.ac.il/~idish/ftp/clsm.pdf) (section 2.3 and Figure 2) also provides a good summary. 
