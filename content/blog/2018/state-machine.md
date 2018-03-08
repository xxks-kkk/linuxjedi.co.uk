Title: State Machine Replication Approach
Date: 2018-03-07 20:24
Category: system
Tags: distributed systems, system concepts, system design principle
Summary: State Machine Replication Approach

[TOC]

## State Machine Replication

- State Machine Replaction system properties:

    - [Available]({filename}/blog/2018/380-02.md)
    - Fault tolerant
    - Appear to behave like a single machine

- t fault tolerant: A system consisting of a set of distinct components is *t fault tolerant*
if it satisfies its specification provided that no more than *t* of those components become 
faulty during some interval of interest.

- t fault-tolerant state machine implementation:  replicating that state machine and running
a replica on each of the processors in a distributed system. Provided each replica being run
by a nonfaulty processor starts in the same initial state and executes the same requests in 
the same order, then each will do the same thing and produce the same output.

- When processors can experience Byzantine failures, an ensemble implementing a 
t fault-tolerant state machine must have at least $2t + 1$ replicas, 
and the output of the ensemble is the output produced by the majority of the replicas. 
(因为Byzantine failures可以产生错误的结果，因此需要大多数replica的结果正确。由于我们是t fault-tolerant,
因此有t replicas可以产生Byzantine failures，因此我们需要额外t+1产生正确结果的replica,也就是2t+1 total replicas)

- If processors experience only fail-stop failures, then an ensemble containing $t + 1$ replicas suffices, 
and the output of the ensemble can be the output produced by any of its members.
(Fail-stop failures的话，replica产生错误就停止工作了，因此我们总共只需要t+1 replicas因为只要保证有一个replica工作就可以了)

- Implementing Replication:

    - Agreement: Every nonfaulty state machine replica receives every request.
    
        - Implemented by clients
        - When a client makes a request, it broadcasts the request to all servers in the system

    - Order: Every nonfaulty state machine replica processes the requests it receives in the same relative order.
      
        - Implemented by servers
        - Define a total order of requests in the system and execute requests in that order
        - Process a request with the lowest timestamp that has been received by that replica
        - __Stability__: The replica can never receive an event with a lower timestamp

            - Implementing stability: Receive requests from a client in increasing order (Given by FIFO channels and logical clocks)
            - A request is stable once a request has been received from each client with a greater timestamp

## Applications

