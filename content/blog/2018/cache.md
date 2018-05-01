Title: Cache, Lease, Consistency, Invalidation
Date: 2018-03-07 20:24
Category: system
Tags: distributed systems, system concepts
Summary: Cache, Lease, Consistency, Invalidation

[TOC]

## Concepts

### Cache

- Cache is built on client side
- Write-through:

    - Writes go to the server 
    - No modified caches

- Write-back:

    - Writes go to cache
    - Dirty cache written to server when necessary

- Invalidations:

    - Track where data is cached
    - When doing a write, invalidate all (other) locations
    - Data can live in multiple caches for reading

- Write-through invalidations:

    - Track all reading caches 
    - On a write: 

        - Server send invalidations to all caches 
        - Each cache invalidates, responds 
        - Server waits for all invalidations, do update
        - Server return
    - Reads can proceed:
        -  If there is a cached copy and if no write waiting at server

- Write-back invalidations:

    - Track all reading and writing caches
    - On a write:
        - Server send invalidations to all caches
        - Each cache invalidates, responds (possibly with updated data)
        - Wait for all invalidations
        - Return
    - Reads can proceed when there is a local copy
    - Order requests carefully at server 
        - Enforce processor order, avoid deadlock
        - Write-through invalidation不用在server order requests因为所有writes直接在server端写，根据request来的order写就可以了。
        但是Write-back invalidation需要在server端order因为写写在cache里，那么requests写的order就没有了，因此在cache把更新好的data
        return给server端时，需要在server端重新排序。

- Leases:

    - Permission to serve data for some time period
    - Wait until lease expires before applying updates
    - Must account for clock skew!

- Strong Leases:

    - The term "Lease" referred in Jim Gray's paper
    - Read request: key, TIL (time to live)
        - When server returns, he server won't accept writes to the key for TIL seconds after reply sent
        - Client invalidates its cache after TTL seconds from when request was sent

- Write-through strong leases:

    - Server queues writes until all leases expire (after all leases expire, the cache got invalidated and server then can write)
    - Avoid starvation: don’t accept new reads

- Write-back strong leases:

    - Cache can get a write lease (exclusive) 
    - Server queues read requests until lease expires

- Strong leases vs. Invalidations

    - Strong leases potentially slower
    - What if a cache fails when it has a key? Strong leases provide better availability 
    - Can combine techniques:
        - Short lease on entire cache, periodically revalidated 
        - All keys invalidated on failure (after lease)

- Weak leases

    - Cache values until lease expires
    - Allow writes, other reads simultaneously
    - Advantages:
        - Stateless at server (don’t care who is caching) 
        - Reads, writes always processed immediately
    - Disadvantages:
        - Consistency model
        - Overhead of revalidations
        - Synchronized revalidations

!!!note
    The key idea is that cache can become stale and we need to have a policy
    for validating the a cached data item before using it. Thus, we have invalidations
    and leases to answer the question: If we cache data, how do we make sure it reflects
    writes of other nodes while maintaining performance? This question implies how we implement
    consistency. For example, to ensure sequential consistency, we need to make sure all operations 
    to a single key are serialized (as if all the operations go to a single copy), which is done
    with the help of invalidations / leases.


### Consistency model 

- __Anomaly__: some sequence of operations (reads and writes) that “shouldn’t” be allowed 
- Consistency model:  which anomalies are possible

    - __Linearizability (Strict Consistency, Strong Consistency)__:
    
        - matches the ideal system
        - Talks about single operations on single objects
        - Literally means: “did the operations happen in a straight line (one after the other)?” 
        - Reads always reflect latest write (i.e. Once a read returns value V1, all reads have to return V1 or later values)
        - Concurrent operations can be executed in any order

    - __Serializability (Sequential Consistency)__:

        - Execution always equivalent to some interleaving
        - Each node’s operations done in order 
        - Guarantees execution of a set of operations (usually each a transaction) is equivalent to some serial execution order 
        - Given operations A1, and A2 serializability only demands that the execution order is A1 followed by A2 or A2 followed by A1 
        - Serializability makes it seem as if there are no concurrent operations, everything happened one after another
        - Relaxation of linearizability 
        - Instead of conforming to a real-time partial order, we use a client-observed partial order

    !!!note
        “The result of any execution is the same as if the operations of all the processes were executed in some sequential order and the operations of each individual process appear in this sequence in the order specified by its program” (Lamport, 1979)
        There is a order on all the processes and operations in each process are ordered in the way sent out by its program.

    - __Strict Serializability__:

        - Combines linearizability and serializability
        - Transactions need to happen in real-time order
        - T1 and T2 are executing concurrently 
            - T1 writes object A, and later T2 reads object A
            - Strict Serializability: T1 before T2 
            - Serializability: T2 before T1 also valid (In this case, T2 will read old value of object A)

    - Weaker models (could have anomalies):

        - Read Your Writes + Eventual Consistency (anomalies are “temporary”)

            - Facebook model, approximately 
            - Clients will always see their own writes 
            - Clients will eventually see everyone’s writes 
            - Eventually the order will be consistent

        - Causal consistency 

            - Causal order (Lamport happens-before) observed everywhere 
            - Concurrent events can have arbitrary and inconsistent order 

        - Transactional models (e.g. Snapshot reads)

            - Some other consistency model + atomicity of transactions

!!!note
    Another angle to look at consistency model is: a contract between the data store and its clients that
    specifies the results that clients can expect to obtain when accessing the data store.

- Why different models?

    - Tradeoff between:

        - Performance: consistency requires sync 
        - Availability: want to operate when disconnected 
        - Programmability: weaker consistency makes applications harder to write (i.e., harder to provide app-level guarantees) 

    - If you want availability, must give up consistency (by CAP (Consistency, availability, partition tolerance))


## Reference

- https://courses.cs.washington.edu/courses/cse452/17sp/slides/Caching.pdf (Examples on different consistency models)
- https://courses.cs.washington.edu/courses/cse452/17sp/slides/ImplementingCaches1
- https://www.cs.utexas.edu/~vijay/cs380D-s18/feb6-fb.pdf
- [CS439 Alison's slide "Other File Systems"](https://www.cs.utexas.edu/users/ans/classes/cs439/schedule.html)