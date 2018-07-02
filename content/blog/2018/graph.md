Title: Graph basics + Topological Sort
Date: 2018-06-30 22:30
Tags: graph, sorting, maw
Summary: Basic graph concepts
Status: draft

[TOC]

## Introduction

In this post, we breifly summarize the basic concepts related to graph algorithm. Then, we study topological sort to make
the graph concepts into practice.

## Graph Basics

### Definitions

- A **graph** $G = (V,E)$ consists of a set of **vertices** $V$, and a set of **edges** $E$.
- Each edge (i.e., **arcs**) is a pair $(v,w)$, where $v,w \in V$.
- Given an edge $e = (u,v)$, the vertex $u$ is its **source**, and $v$ is its **sink**.
- If the pair is ordered, then the graph is **directed** (i.e., **digraphs**).
- Vertex $w$ is **adjacent** to $v$ iff $(v,w) \in E$.

!!!note
    In digraph, $(v,w)$ is not the same as $(w,v)$. Thus, if $(v,w) \in E$ and $(w,v) \not\in E$, $v$ is
    adjacent to $w$ but $w$ is NOT adjacent to $v$. However, for the undirected graph, if $(v,w) \in E$, then
    $(w,v) \in E$. Thus, if $v$ is adjacent to $w$, then $w$ is adjacent to $v$ in undirected graph.

- A **path** in a graph is a sequence of vertices $w_1, w_2, w_3, \dots, w_N$ such that $(w_i, w_{i+1}) \in E$ for
$1 \le i < N$. The **length** of such path is the number of edges on the path, which is equal to $N - 1$.

!!!note
    - We allow a path from a vertex to itself
        - If this path contains no edge, then the path length is 0
        - If the graph contains an edge $(v,v)$ from a vertex to itself, then the path $v,v$ is referred to as a **loop**

- A **simple path** is a path such that all vertices are distinct, except that the first and last could be the same.
- If there is a path from $u$ to $v$, $v$ is said to be **reachable** from $u$.
- A **cycle** in a graph:
    - For directed graph, a cycle is a path of length at least 1 such that vertices $w_1 = w_N$.
    - For undirected graph, we require edges to be distinct
        - reasoning: the path $u,v,u$ in an undirected graph should be considered a cycle because $(u,v)$ and $(v,u)$
        are the same edge.
- A **directed acyclic graph (DAG)** is a directed graph in which there are no cycles (i.e., paths which contain one or
more edges and which begin and end at the same vertex)
    - Vertices in a DAG which have no incoming edges are referred to as **sources**
    - Vertices which have no outgoing edges are referred to as **sinks**
- **connected**:
    - An undirected graph is **connected** if there is a path from every vertex to every other vertex.
    - A directed graph is **connected** if it contains a directed path from $u$ to $v$ or a directed path
    from $v$ to $u$ for every pair of vertices $u$ and $v$.
- A directed graph is **strongly connected** if it contains a directed path from $u$ to $v$ and a directed
path from $v$ to $u$ for every pair of vertices $u$ and $v$.
- If a directed graph is not strongly connected, but the underlying graph (without direction to the arcs)
is connected, then the graph is said to be **weakly connected**.
- For a graph $G$, a **connected component** is a maximal set of vertices $C$ such that each pair of vertices in $C$ is connected
in $G$. Every vertex belongs to exactly one connected component.
- A **complete graph** is a graph in which there is an edge between every pair of vertices.

### Representation


## Topological Sort

### Definition

### BFS Approach

### DFS Approach

## Reference

- "Data Structures and Algorithm Analysis in C++, 4th Edition" by Mark A. Weiss (we use
*MAW (cpp)* for short in the future)
- "Elements of Programming Interviews: The Insiders' Guide" by Adnan Aziz,
Tsung-Hsien Lee, and Amit Prakash, p.342 - 346 (we use *ATA* for short in the future)
- [Topological Sort on Coursera](https://www.coursera.org/learn/algorithms-graphs-data-structures/lecture/yeKm7/topological-sort)

- MAW (cpp) p.

- graph basics
- topological sort (coursera + maw)
- BFS (MAW)
- DFS (Coursera one)