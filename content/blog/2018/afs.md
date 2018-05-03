Title: "The Andrew File System (AFS)"
Date: 2018-05-02 23:30
Category: system
Tags: papers, distributed systems, 
Summary: "The Andrew File System (AFS)" paper reading

[TOC]

## Problem

Design a distributed file system that can scale: a server can support as many clients as possible?

## Design assumptions

- Most files were not frequently shared, and accessed sequentially in their entirety.
- System is used for casual usage (e.g., when a user logs into a different client, they expect some reasonable version of their files to show up there.)
    - Not for concurrent access & updates scenario

## Design

- Cache:
    - whole-file caching:
        - AFS is whole-file caching on the local disk of the client machine that is accessing a file

            `open()` a file, the entire file (if it exists) is fetched from the server and stored in a file on your local disk. Subsequent application `read()` and `write()` operations are redirected to the local file system where the file is stored; thus, these operations require no network communication and are fast.

    - Use client memory to cache blocks of file when access locally
    - Contact the server (use TestAuth protocol) for future access of the file to see if client can use cache (i.e., no modification to the local cached file)
        - Advantage: no network transfer of the file
        - Disadvantge: too many contacts to server for cached file no-modification verification
            - sol: use callback
    - cache both directories and file contents
        - motivation: server spends much CPU time traversing directories
        - client caches and requests callback to directories along the way to the target file
        - Sequential access assumption makes this technique works (e.g., access files within the same cached directory)
        - Much effort spent on the client side (path traversing & cache) alleviates the load for server

- Callback:
    - a way to reduce number of client/server interactions (mainly for TestAuth message verification)
    - A callback is simply a promise from the server to the client that the server will inform the client when a file that the client is caching has been modified
    - client assumes cached files are valid until the server tells it otherwise

!!!note
    The idea of callback vs. TestAuth message is analogous to interrupt vs. polling

- Cache consistency:
    - consistency between processes on different machines:
        - update visibility sol: flush-on-close
        - cache staleness sol: server-initiated cache invalidation ("break" callback)
    - consistency between processes on the same machine:
        - update visibility sol: writes to a file are immediately visible to other local processes (i.e., a process does not have to wait until a file is closed to see its latest updates) (same as UNIX semantics: tail a log file and can see the writes
        in real time)

- Last writer wins (i.e., last closer wins) for concurrent modification of the same file
    - The result is a file that was generated in its entirety either by one client or the other (unlike NFS, a file can contain
    blocks from different clients)

- Load balancing:
    - use volumes, which an administrator could move across servers to balance load

- Building the server with thread instead of process per client to reduce the overhead (e.g. context switching)

- Crash Recovery:
    - Clients:
        - Client send out TestAuth message to validate its cache after recovery
    - Servers:
        - callbacks are kept in memory -> need to validate the cached file
        - sol:
            - having the server send a message to each client after recovery to let clients start to validate their cache
            - clients send heartbeat message periodically to server

- Even the cache is on disk, AFS can use client-side OS memory caching infrastructure to improve performance

- AFS provides a true global namespace to clients, thus ensuring that all files were named the same way on all client machines.
    - clients in NFS can mount NFS server anyway -> hard to administer

- AFS has security and access-control lists

## NFS vs. AFS

- For large-file (greater than memory) sequential re-read, AFS > NFS:
    - AFS use local disk to cache entire file 
    - NFS can cache blocks in memory and have to refetch the file for re-read
- For access small subset of data within large files, NFS > AFS:
    - AFS has to fetch entire file and send it back after modification
    - NFS only read the blocks that need to be modified
    - AFS is not good for append information to log periodically (little log writes that add small amounts of data to an existing large file)

|                                    | NFS                             | AFS                                     |
|------------------------------------|---------------------------------|-----------------------------------------|
| Cache unit                         | block of a file                 | whole file                              |
| Cache location                     | memory                          | local disk                              |
| Cache strategy                     | cache block only                | cache directories and files             |
| Cache invalidation                 | callback                        | polling (issue GETATTR)                 |
| Concurrent update of the same file | Last Writer Wins                | Blocks flushed to servers during update |
| Crash Recovery                     | server crash is unnoticeable    | complex crash recovery                  |
| Namespace                          | single namespace to all clients | namespace is arbitrary across clients   |

## Remarks

- Several commonly-seen design techniques:
    - Force the clients to spend much more effort (cache directory and request callback) to reduce load on server
        - techniques to avoid DDOS attack in security
        - Mining in Bitcoin

- Cache consistency in file system is incapable of handling a file access from multiple clients (i.e., concurrent access)
    - Need to implement explicit file-level locking on top of file system
    - Need extra mechnaism to handle conflicts (e.g., concurrent updates):
        - Google doc use git-like [operational transformation](https://www.quora.com/How-is-collaborative-document-editing-implemented-in-Google-Docs-How-are-infinite-undo-redo-implemented-separately-for-each-user-What-tasks-are-offloaded-to-the-client-and-which-are-done-at-the-server-itself) to resolve conflict

## Reference

- [The Andrew File System (AFS)](http://pages.cs.wisc.edu/~remzi/OSTEP/dist-afs.pdf)