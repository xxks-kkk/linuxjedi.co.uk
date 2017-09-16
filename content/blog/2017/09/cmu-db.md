title: Watching log of CMU Database Systems course
date: 2017-09-08 12:30 
Category: Database
Tags: database
Summary: log book for CMU 15-445/15-645 Database Systems Fall 2017 course

## Motivation

There is a hobby I always want to develop but never gets into practice: watch lecture videos while I eat. The
reason because lecture videos are mostly not fun especially when the content of the video is entirely new to you.
However, this semester I want to actually start developing this habbit partly because I'm missing system side of computer science.
I miss the database knowledge I have picked up in the past three years and I don't want to lose the touch
in this field. So, I think why not start to watch database lecture videoes for fun when I eat? That leads to this post.

This post is a log of cool points I like when I watch [CMU Database Group Database Systems lecture video](https://www.youtube.com/channel/UCHnBsf2rH-K7pn09rb3qvkA).

## Log

--- 09/07/2017 UPDATE ---

- There are bunch of data models besides relational model: relational,
key/value, graph, document, column-family, array/matrix, hierarchical, network

- Thanks to Prof.Andy Pavlo, I finally understand the difference between
relational algebra and relational calculus in terms of their purpose:

    When we talk about using data manipulation language (DML) to store
    and retrieve information from a database, there are two categories:
    procedural and non-procedural, which corresponds to relational algebra
    and relational calculus respectively. For procedural language, the query specifies
    the (high-level) strategy the DBMS should use to find the desired result. For
    non-procedural lanaguages, the query specifies only what data is wanted and not how to
    find it. In fact, SQL is derived from relational calculus. In other words, 
    relational calculus is used when we try to come up with a different 
    query language to replace SQL.

- The fundamental operators in relational algebra need to be implemented
in the database system in order to manipulate tuples: $\sigma \text{(select)}, \pi \text{(projection)}, \cup \text{(union)},
\cap \text{(intersection)}, - \text{(difference)}, \times \text{(product)}, \bowtie \text{(join)}$. 
