Title: "Existential Consistency: Measuring and Understanding Consistency at Facebook"
Date: 2018-03-08 20:24
Category: system
Tags: papers, distributed systems
Summary: "Existential Consistency: Measuring and Understanding Consistency at Facebook" paper reading

[TOC]

## Overview

- Facebook Study

    - Analyzed a small portion of the Facebook traffic to the TAO graph system 
    - Analyzed what consistency models hold
    - Analyzed when readers get anomalous results

## Facebook’s Replicated Storage

- Facebook Data Model

    - Graph Data Model
    - Vertex: unique ID + data
    - Edges: between two vertexes, contains data, indexed by source vertex

- Database

    - Horizontally (i.e., row) sharded, geo-replicated database
    - Each region has a full copy
    - Each shard has a master which asynchronously updates the other regions

- Two-Level Cache

    - Root cache sits in front of the database
    - Leaf caches sit in front of the root caches
    - Write-through caches
    - Reads:
        - progress down the stack in their local region on cache misses from leaf cache to root cache, and then to local database. 
          The cache-hit ratios are very high, so reads are typically served by the leaf caches.
    - Writes:
        - They are synchronously routed through their leaf cache (1) to their local root cache (2) to the root-master cache (3), and to the master database shard (4) and back (5–8).
        - Each of those caches applies the write when it forwards the database’s acknowledgment back towards the client.
        - The root caches in the master ($6'$) and originating regions ($7'$) both asynchronously invalidate the other leaf caches in their region
        - The database master asynchronously replicates the write to the slave regions ($5'$). When a slave database in a region that did not originate the write receives it, the database asynchronously invalidates its root cache ($6''$) that in turn asynchronously invalidates all its leaf caches ($7''$).

    <img src="/images/fb-storage.png" alt="facebook replicated storage"/>

## Consistency Models

- Local Consistency Models

    - __Local__: A consistency model, C, is local if the system as a whole provides C whenever each individual object provides C

- Linearizability

    - Linearizability is the strongest consistency model for non-transactional systems. 
    - Intuitively, linearizability ensures that each operation appears to take effect instantaneously at some point between when the client invokes the operation and it receives the response. 
    - More formally, linearizability dictates that there exists a total order over all operations in the system, and that this order is consistent with the real-time order of operations. 
        - If operation A completes before operation B begins, then A will be ordered before B. 
    - Linearizability avoids anomalies by ensuring that writes take effect in some sequential order consistent with real time, and that reads always see the 
    results of the most recently completed write.

- Per-Object Sequential Consistency

    - Per-object sequential consistency requires that there exists a legal, total order over all requests to each object that is consistent with client’s orders. 
    - Intuitively, there is one logical version of each object that progresses forward in time. 
    - Clients always see a newer version of an object as they interact with it. 
    - Different clients, however, may see different versions of the object.
        - One client may be on version 100 of an object, while another client may see version 105.

- Read-After-Write Consistency

    - when a write request has committed, all following read requests to that cache always reflect this write or later writes.
    - Region read-after-write consistency applies the constraint for reads in the same region as a write. Global read-after-write consistency applies the constraint for all reads.

- Eventual Consistency

    - Eventual consistency requires that replicas “eventually” agree on a value of an object, i.e., when they all have received the same set of writes, they will have the same value.
    - Eventual consistency allows replicas to answer reads immediately using their current version of the data, while writes are asynchronously propagated in the background. While writes are propagating between replicas, different replicas may return different results for reads.
    - A client can update any replica of an object and all updates to an object will eventually be applied, but potentially in different orders at different replicas.

- Facebook’s Consistency

    - per-object sequential consistency (per-cache) + read-after-write (per-cache) + eventual consistency (across caches)
    - User sessions are typically handled exclusively by one leaf cache, and thus we expect most of them to receive per-object sequential and read-after-write consistency.
    - User sessions spread across multiple leaf caches receive eventual consistency.

## Reference

- https://www.cs.utexas.edu/~vijay/cs380D-s18/feb6-fb.pdf
- https://www.allthingsdistributed.com/2008/12/eventually_consistent.html