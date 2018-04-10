Title: "Fast Crash Recovery in RAMCloud"
Date: 2018-04-09 22:00
Category: system
Tags: papers, storage,  
Summary: "Fast Crash Recovery in RAMCloud" paper reading

[TOC]

## Problem, Motivation

RAMCloud is a large-scale general-purpose DRAM storage system for datacenters. 
The system is motivated by the fact that Large-scale apps struggle with utilizing
DRAM to its full potential:

- DRAM is still majorly used as a cache for some other storage system
- Developers have to manage consistency between caches in DRAM and its storage system
- Cache misses and backing store overheads

<img src="/images/RAMCloud-datacenter.png" alt="RAMCloud concept" style="height 300px"/>

It has four design goals:

- Scalbility: 1000-10000 commodity servers with 32-64 GB DRAM/server
- Low latency: uniform low-latency access (5-10 μs round-trip times for small read operations)
- High throughput: 1M ops/sec/server
- High durability and availability

This paper focuses on the "high durability and availability". Replicating all data (x3) in DRAM fix
some availability issue but triple the cost and energy usage of the system. Thus, RAMCloud only 
stores a single copy of data in DRAM, which brings the problem of availability: what happens when server
crashes? RAMCloud’s solution to the availability problem is fast crash recovery. Then the problem 
becomes how to recover from crash within 1s~2s for 64GB or more DRAM data?

## Challenges

- Durability: RAM is lack of durability. Data is unavailable on crashed nodes.
- Availability: How to recover as soon as possible?
    
    - Fast writes: Synchronous disk I/O’s during writes?? Too slow 
    - Fast crash recovery: Data unavailable after crashes?? No!

- Large scale: 10,000 nodes, 100TB to 1PB

## Architecture

<img src="/images/RAMCloud-architecture.png" alt="RAMCloud main architecture"/>

- Each storage server contains a master and a backup. A central coordinator [^1] manages the server pool and [tablet]({filename}/blog/2018/pnuts.md) configuration. Client applications run on separate machines and access RAMCloud using a client library that makes remote procedure calls.

    - master: manages RAMCloud objects in its DRAM and services client requests
    - backup: stores redundant copies of objects from other masters using its disk or flash memory
    - coordinator: manages configuration information such as the network addresses of the storage servers and the locations of objects
    - tablets: consecutive key ranges within a single table

- Data model: object consists of [identifier(64b), version(64b), Blob(<=1MB)]

[^1]: The coordinator will use ZooKeeper to store its configuration information, which consists of a list of active storage servers along with the tablets they manage. ZooKeeper本身是一个非常牢靠的记事本，用于记录一些概要信息。Hadoop依靠这个记事本来记录当前哪些节点正在用，哪些已掉线，哪些是备用等，以此来管理机群。

## Durability and Availability

- Durability: 1 copy in DRAM; Backup copies on disk/flash: durability ~ free!
- Availiability: 

    - Fast writes: Buffered Logging
    - Fast crash recovery: Large-scale parallelism to reconstruct data (similar to MapReduce)

### Buffered Logging

<img src="/images/buffered-logging.png" alt="Buffered Logging"/>

- When a master receives a write requests, it updates its in-memory log and forwards the new data to several backups, which buffer the data in their memory. Master maintains a hash table to record locations of data objects. The data is eventually written to disk or flash in large batches. Backups must use an auxiliary power source to ensure that buffers can be written to stable storage after a power failure.

    - No disk I/O during write requests
    - Master’s memory also log-structured
    - Log cleaning ~ generational garbage collection
    - master's log is divided into 8MB segments
    - Hash table is used for quickly lookup object in log

!!!note
    This part idea borrows from [log-structured file system](http://pages.cs.wisc.edu/~remzi/OSTEP/file-lfs.pdf).

### Fast Recovery

<img src="/images/fast-recovery-overview.png" alt="Fast Recovery Overview"/>

- Three different recovery schemas:

    - One recovery master, small backup servers (disk bandwidth bottleneck)
    - One recovery master, large backup servers (network bandwidth bottleneck)
    - Several recovery masters, large backup servers (good!)

<img src="/images/recovery.png" alt="Recovery Overview"/>

- Divide each master’s data into partitions

    - Partition and scatter log data to more backups randomly. So backup data can be read in parallel when the master crashed.
    - Recover each partition on a separate recovery master
    - Partitions based on tables & key ranges, not log segment
    - Each backup divides its log data among recovery masters

- Each mater computes the strategy to form partitions and upload the strategy to coordinator as *will*. Coordinator follows crashed master's will to 
divide crashed master's data into partitions and assign the recoverying work to recovery masters (see section 3.5.3)

<img src="/images/log-distribution.png" alt="log distribution"/>

<img src="/images/recovery-ops.png" alt="recovery ops"/>

<img src="/images/recovery-ops-details.png" alt="recovery ops details"/>

## Remarks & Thoughts

The authors use the log-structured storage instead of synchronous disk write to preserve durability. 
And the availability is achieved via data parallelism. The design harness the scale well and has exceptional performance.

## Reference

- [Fast Crash Recovery in RAMCloud](https://web.stanford.edu/~ouster/cgi-bin/papers/ramcloud-recovery.pdf), [slides](https://ramcloud.atlassian.net/wiki/spaces/RAM/pages/6848659/RAMCloud+Presentations), [video on paper](https://www.youtube.com/watch?v=lcUvU3b5co8),
[videos on details of paper](https://www.youtube.com/channel/UCqnEwnxxNoHwCwY5W5kfGVA/videos). 
- [Tian Pan's Blog on RAMCloud](http://www.puncsky.com/blog/2012/12/13/fast-crash-recovery-in-ramcloud/)
- [The RAMCloud Storage System](https://ongardie.net/var/blurbs/pubs/ramcloud-tocs15.pdf)