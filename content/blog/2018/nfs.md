Title: "Sun's Network File System (NFS)"
Date: 2018-05-01 2:20
Category: system
Tags: papers, distributed systems
Summary: "Sun's Network File System (NFS)" paper reading

[TOC]

## Problem

Design a distributed file system with transparent access to files from clients

## System designs


<img src="/images/nfs-architecture.png" alt="nfs architecture"/>

- the server stores the data on its disks, and clients request data through well-formed protocol messages

- Architecture advantages:
    - easy sharing of data across clients
    - centralized administration (backup done on multiple servers instead of many clients)
    - security (put server behind firewall)

- Transparency:
    - Location transparency: file name does not include name of the server where the file is stored
    - Implemented using NFS Mount Protocol:
        - Mount remote directories as local directories
        - Maintain a Mount table with (directory, server) mapping

<img src="/images/distributed-file-system-architecture.png" alt="distributed file system architecture"/>

- Clients talk to server using RPC:
    - Use RPC to forward every file system request; remote server executes each request as a local request; server
    responds back with result (Example: Figure 49.5 in Remzi's chapter)
    - Advantage: server provides a consistent view of the file system to clients
    - Disadvantage: performance (use cache)

- Crash Recovery:
    - goal: simple and fast server crash recovery
    - Use a stateless Protocol (NFSv2): the server doesn't keep track of anything about what is happening at each client
    - Stateful: server maintain a filedescriptor(an integer) to actual file relationship (unknown after recovery)
    - Stateless: file handle (a unique identifier for each directory and file). 
        - Every client RPC call needs to pass a file handle
        - Server returns file handle whenever needs (e.g., mkdir)

- Server failure & Message loss:
    - Client retries the request (READ, WRITE are idempotent in NFS)

- Cache:
    - Client side:
        - cache file data and metadata by block that is read from server in local memory
        - Cache serves as a temporary buffer for writes (allow asyncronous write)
        - Advantage: reduce network usage, improve performance
        - Disadvantage: write lost in memory after crash (safety vs. performance tradeoff)
    - Server side:
        - server can buffer the write in memory and write to disk asychronously 
        - Problem: write in memory can lost
        - Sol: 
            - battery-backed memory
            - commit each WRITE to stable storage before ack WRITE success to clients

- Cache consistency problem:
    - Update visibility: when do updates from one client become visible at other clients?
        - sol: flush-on-close (write-back cache):
            - when a file is written to and subsequently closed by a client application, the client flushes all updates (i.e., dirty pages in the cache) to the server.
    - Stale cache: once the server has a new version, how long before clients see the new version instead of an older cached copy?
        - sol: issue GETATTR to get file stats (last modified date), if the time-of-modification is more recent than the time that the file was fetched into the client cache, the client invalidates the cache and subsequent reads will go to the server.
        - Use attribute cache to reduce GETATTR requests (update attribute cache periodically)
        - Still has problem: can still read stale value (polling interval, cache update/invalidation delayed by network)

!!!note
    You may think the solution to cache consistency problems look a lot like [write-back + invalidation]({filename}/blog/2018/cache.md). The geenral idea is the same. However, the solution here takes client's perspective. However, the definitions in my previous
    post takes server's perspective. More formally, we call client's perspective "client-initiated consistency protocol" and
    server's perspective "server-initiated consistency protocol".

## Remarks

- NFS issues:
    - multiple clients update the same file may get inconsistent view of the file (depends on cache update/invalidation, attribute
    cache polling frequency)
    - Clients crash may lose data in buffer (cache)
- NFS Key features:
    - Location-transparent naming
    - Client-side and server-side caching for performance
    - Stateless architecture
    - Client-initiated consistency protocol
- Good in NFS:
    - Simple
    - Highly portable (open protocol)
- Bad in NFS:
    - Lack of strong consistency

## Reference

- [Sun’s Network File System (NFS)](http://pages.cs.wisc.edu/~remzi/OSTEP/dist-nfs.pdf)
- [CS439 Alison's slide "Other File Systems"](https://www.cs.utexas.edu/users/ans/classes/cs439/schedule.html)