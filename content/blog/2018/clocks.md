Title: Lamport Clocks, Vector Clocks
Date: 2018-03-06 20:24
Category: system
Tags: distributed systems, system concepts
Summary: Lamport Clocks, Vector Clocks

## Lamport Clocks

- In a distributed system, there is **no global time** and **no global state** $\implies$ the clock of different nodes in a distributed system
can have different values.
- Happened-before Relationship:
    
    - Some events in a distributed system happened before other events and others are concurrent
    - Happened-before is a partial ordering on events in a distributed system:

        Given events $E1, E2, E3$ and $E1$ happens before $E2$ and $E1$ happens before $E3$, we have $E2$ and $E3$ are concurrent and
        $E1 < E3$ and $E1 < E3$.

- $\rightarrow$ relation satisfies the following conditions:

    1) If $a$ and $b$ are events in the same process, and $a$ comes before $b$, then $a \rightarrow b$

    2) If $a$ is the sending of a message by one process and $b$ is the receipt of the same message by another process, then $a \rightarrow b$

    3) If $a \rightarrow b$ and $b \rightarrow c$, then $a \rightarrow c$

- Two distinct events $a$ and $b$ are said to be concurrent if $a \not\rightarrow b$ and $b \not\rightarrow a$

- Logical Clocks:

    - Assigns a monotonically increasing number $C(x)$ for each event $x$ in a process 
    - If event $x$ happens before event $y$, $C(x) < C(y)$ (Note, $C(x) < C(y) \not\implies x < y$)
    - If $x$ and $y$ are in the same process, and $x < y$, then $C(x) < C(y)$
    - If $x$ is sending of message, and $y$ receipt of the message, then $x < y$ and $C(x) < C(y)$

- Implementing Logical Clocks:

    - Within a process $X$, increment $C(x)$ every time an event happens
    - When process $X$ receives a message with timestamp $T$, $C(x) = \max(T, C(x)) + 1$

- How do we break the tie of the concurrent events and achive total ordering of the events in the sytem:

    - If $x$ and $y$ in same process, and $x < y$, $C(x) < C(y)$
    - If $x$ and $y$ are concurrent ($x = y$), then $P(x) < P(y) \implies C(x) < C(y)$ ($P(\cdot)$ means process ID)

## Vector Clocks

- Limitation of Lamport Clocks:

    - If $C(x) < C(y)$, we cannot tell whether $x < y$
    - We can only say if $x < y$, then $C(x) < C(y)$

- Goal: to enable each process to have an **approximation of global time** at all processes (Every message propagates info
about state of whole system)

- Each process has a vector of clocks: 

    - Clock $C_i$ is time for process $i$ as seen by the owner of the vector 
    - $C_i$ in two different vectors may not be the same

- Implementing Vector Clocks:

    - Each process $P_i$ updates its component $C_i$ in its vector clock (This update happens for each internal event (e.g. on receiving a message))
    - Each message has a vector clock time stamp
    - On getting the message, for each field $x$ in the vector: $C[x] = \max(C[x], message\_time\_stamp[x])$

- Comparing Vector Timestamps:

    - Timestamp $X \le Y$ if all components of $X \le$ corresponding components in $Y$
    - Timestamp $X < Y$ if at least one component is strictly lesser, with all others being equal  
    - Otherwise, $X$ and $Y$ are concurrent