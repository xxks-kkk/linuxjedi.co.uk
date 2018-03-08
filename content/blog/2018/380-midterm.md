Title: Distributed System Reference Guide
Date: 2018-03-06 16:24
Category: system
Tags: papers, distributed systems, protocol, system design principle, system concepts
Summary: 

This post is reference guide that points to the concepts, system design principles, system concepts
mentioned in my posts.

[TOC]

## System Concepts

- [Logical Clocks, Vector Clocks]({filename}/blog/2018/clocks.md)
- __State Machine__: A process whose state depends entirely on the starting state and sequence of operations
- __Replication__: All servers exhibit the same behavior
- __Sharding__: Different data on different servers; Partitioned via some function on keys 
- __Clock Skew__: the same sourced clock signal arrives at different components at different times

## Protocol

- [Pub/Sub Mechanism from PNUTS]({filename}/blog/2018/pnuts.md)


## System Designs

- [State Machine Replication]({filename}/blog/2018/state-machine.md)


## System Principles

- Scability: sharding + replication

    - Usually, shard then replicate 
    - Each piece of data lives on one replicated shard

- Stronger consistency models are easier to reason about (and program for), but more expensive to obtain 
- Weaker consistency models provide more performance, but hard to understand and program for

