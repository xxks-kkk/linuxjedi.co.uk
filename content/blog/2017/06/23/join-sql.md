Title: join in SQL
Date: 2017-06-23 21:23
Category: DB
Tags: db, sql, relational-algebra, leetcode
Summary: A study on join statement in SQL

In this post, I'll provide a summary on the usage of `join` statement in SQL
and use [Leetcode 175](https://leetcode.com/problems/combine-two-tables/) as 
a concrete example to show several equivalent `join` statement usage.

To be honest, this is my third time visiting this material. The very first time
happened when I took DB course in college, and the second time was when I joined
the federation team at IBM and learned about DB2. Unfortunately, I didn't keep
my study notes well in the first two tries and I don't write SQL a lot during my
day to day work. Things, again, get rusty very quickly. This time I want to do a
better job by, at least, saving my notes in a good place. 

!!!note
    *teaches*, *instructor* table DDL and its actual data appeard in this post 
    are from the 
    [supplementary resources](http://db-book.com/) of the 
    [Database System Concepts](https://www.amazon.com/Database-System-Concepts-Computer-Science/dp/0073523321) book.

[TOC]

## TL;DR

- `natural join` produces a relation from two relations by considering only those pairs of tuples
with the same value on those attributes that appear in the schemas of both relations.

- `join ... using` specifies a subset of common attributes to join.

- `join ... on` specifies a predicate to use on join.

- `outer join` is used when we want to preserve the tuples that may have null value on
the common attributes of one of the relations that we want to join on.

## Motivation

Before we directly jump into the SQL, I want to briefly talks about the motivation
for the `join` statement. Specifically, why do we need it?

To retrieve data from multiple relations (i.e. more than one table), we can either
use a cartesian product or join of columns of the same data type.

The cartesian product happens to the relations listed in the `from` clause of a SQL.
The end result of cartesian product is a relation that has all attributes from
all the relations in the `from` clause. The following iterative process shows
how the cartesian product of the relations in the `from` clause get generated

```
for each tuple t1 in relation r1
  for each tuple t2 in relation r2
    . . .
    for each tuple tm in relation rm
      Concatenate t1, t2, . . . , tm into a single tuple t
      Add t into the result relation
```

Another perspective to understand cartesian product is from relation algebra cross-product
$R \times S$, which is defined as: returns a relation instance whose schema
contains all the fields of $R$ (in the same order as they appear in $R$) followed 
by all the fields of $S$ (in the same order as they appear in $S$). The result of
$R \times S$ contains all tuples $(r,s)$ (the concatenation of tuples $r$ and $s$)
for each pair of tuples $r \in R$, $s \in S$.

To see a concrete example, let's consider the following SQL

```sql
select * from teaches, instructor;
```

The *teaches* and *instructor* table look like below

```
sqlite> select * from teaches;
ID|course_id|sec_id|semester|year
10101|CS-101|1|Fall|2009
10101|CS-315|1|Spring|2010
10101|CS-347|1|Fall|2009
12121|FIN-201|1|Spring|2010
15151|MU-199|1|Spring|2010
22222|PHY-101|1|Fall|2009
32343|HIS-351|1|Spring|2010
45565|CS-101|1|Spring|2010
45565|CS-319|1|Spring|2010
76766|BIO-101|1|Summer|2009
76766|BIO-301|1|Summer|2010
83821|CS-190|1|Spring|2009
83821|CS-190|2|Spring|2009
83821|CS-319|2|Spring|2010
98345|EE-181|1|Spring|2009

sqlite> select * from instructor;
ID|name|dept_name|salary
10101|Srinivasan|Comp. Sci.|65000
12121|Wu|Finance|90000
15151|Mozart|Music|40000
22222|Einstein|Physics|95000
32343|El Said|History|60000
33456|Gold|Physics|87000
45565|Katz|Comp. Sci.|75000
58583|Califieri|History|62000
76543|Singh|Finance|80000
76766|Crick|Biology|72000
83821|Brandt|Comp. Sci.|92000
98345|Kim|Elec. Eng.|80000
```

*teaches* table has 15 rows; *instructor* table
has 12 rows. Then, if we run our SQL above, we get our result looks like

```
sqlite> select * from instructor, teaches limit 20;
ID|name|dept_name|salary|ID|course_id|sec_id|semester|year
10101|Srinivasan|Comp. Sci.|65000|10101|CS-101|1|Fall|2009
10101|Srinivasan|Comp. Sci.|65000|10101|CS-315|1|Spring|2010
10101|Srinivasan|Comp. Sci.|65000|10101|CS-347|1|Fall|2009
10101|Srinivasan|Comp. Sci.|65000|12121|FIN-201|1|Spring|2010
10101|Srinivasan|Comp. Sci.|65000|15151|MU-199|1|Spring|2010
10101|Srinivasan|Comp. Sci.|65000|22222|PHY-101|1|Fall|2009
10101|Srinivasan|Comp. Sci.|65000|32343|HIS-351|1|Spring|2010
10101|Srinivasan|Comp. Sci.|65000|45565|CS-101|1|Spring|2010
10101|Srinivasan|Comp. Sci.|65000|45565|CS-319|1|Spring|2010
10101|Srinivasan|Comp. Sci.|65000|76766|BIO-101|1|Summer|2009
10101|Srinivasan|Comp. Sci.|65000|76766|BIO-301|1|Summer|2010
10101|Srinivasan|Comp. Sci.|65000|83821|CS-190|1|Spring|2009
10101|Srinivasan|Comp. Sci.|65000|83821|CS-190|2|Spring|2009
10101|Srinivasan|Comp. Sci.|65000|83821|CS-319|2|Spring|2010
10101|Srinivasan|Comp. Sci.|65000|98345|EE-181|1|Spring|2009
12121|Wu|Finance|90000|10101|CS-101|1|Fall|2009
12121|Wu|Finance|90000|10101|CS-315|1|Spring|2010
12121|Wu|Finance|90000|10101|CS-347|1|Fall|2009
12121|Wu|Finance|90000|12121|FIN-201|1|Spring|2010
12121|Wu|Finance|90000|15151|MU-199|1|Spring|2010
```

The result relation has 180 rows, which exactly equal to $12 \times 15$. Notice that
the order of appearance of relations appeard in the `from` clause matters. If you 
take a look at our SQL result, we get there are $15$ rows with "name" called 
"Srinivasan" and then we expect another $15$ rows with "name" called "Wu" and so on.
This matches the description of relational algebra perfectly.

Quite often, we use `where` clause to restrict the combinations created by the 
cartesian product to those that are meaningful for the desired answer. One common 
scenario is like the following SQL

```sql
select name, course id
from instructor, teaches
where instructor.ID = teaches.ID;
```

In this query, we combine information from the *instructor* and *teaches* table
and the matching condition requires `instructor.ID` to be equal to `teaches.ID`. 
In fact, these are the only attributes in the two relations that have the same name. 
In general, we may often find us writing SQLs that requires all attributes with
matching names to be equated in the `where` clause. This case is so common that
we use `join` to save us some effort.

## join

In this section, I'll talk about `join` from SQL perspective, and then I'll also
present how `join` is actually defined in relational algebra.

### SQL perspective

There are two basic types of join: **inner join** and **outer join**. **inner** keyword
is optional. In other words, if only `join` appears in the SQL statement, we usually
assume it to be **inner join**. Under **outer join**, we can further specify whether
it is **left outer join**, **right outer join**, or **full outer join**. Here 
is a graphic summary for the text above

```
- (inner) join
- outer join
   |- left outer join
   |- right outer join
   |- full outer join
```

In addition, there are join conditions that we can use in combination with
the join form mentioned above. In other words, any form of join (inner, left outer,
right outer, or full outer) can be combined with any join condition (natural, using, or on).
The table below provides a summary of join types and join conditions

| Join types           | Join conditions |
|----------------------|-----------------|
| **inner join**       | natural         |
| **left outer join**  | on <predicate>  |
| **right outer join** | using ($A_1, A_2, \dots, A_n$)        |
| **full outer join**  |                 |

#### inner join

##### natural join

We start this section by considering **natural join**. The natural join works
on two relations and produces a relation as the result. Unlike the cartesian
product of two relations, which concatenates each tuple of the first relation
with every tuple of the second, natural join considers only those pairs of tuples
with the same value on those attributes that appear in the schemas of both relations.

```sql
select name, course_id from instructor natural join teaches;
```

Consider the query above, computing *instructor* `natural join` *teaches* considers
only those pairs of tuples where both the tuple from *instructor* and the tuple
from *teaches* have the same value on the common attribute, "ID".

```
sqlite> select name, course_id from instructor natural join teaches;
name|course_id
Srinivasan|CS-101
Srinivasan|CS-315
Srinivasan|CS-347
Wu|FIN-201
Mozart|MU-199
Einstein|PHY-101
El Said|HIS-351
Katz|CS-101
Katz|CS-319
Crick|BIO-101
Crick|BIO-301
Brandt|CS-190
Brandt|CS-190
Brandt|CS-319
Kim|EE-181
```

!!!note
    1. The query result set is exactly the same as the
    result set given by ``select name, course id from instructor, teaches where instructor.ID = teaches.ID;``
  
```
sqlite> select * from instructor natural join teaches;
ID|name|dept_name|salary|course_id|sec_id|semester|year
10101|Srinivasan|Comp. Sci.|65000|CS-101|1|Fall|2009
10101|Srinivasan|Comp. Sci.|65000|CS-315|1|Spring|2010
10101|Srinivasan|Comp. Sci.|65000|CS-347|1|Fall|2009
12121|Wu|Finance|90000|FIN-201|1|Spring|2010
15151|Mozart|Music|40000|MU-199|1|Spring|2010
22222|Einstein|Physics|95000|PHY-101|1|Fall|2009
32343|El Said|History|60000|HIS-351|1|Spring|2010
45565|Katz|Comp. Sci.|75000|CS-101|1|Spring|2010
45565|Katz|Comp. Sci.|75000|CS-319|1|Spring|2010
76766|Crick|Biology|72000|BIO-101|1|Summer|2009
76766|Crick|Biology|72000|BIO-301|1|Summer|2010
83821|Brandt|Comp. Sci.|92000|CS-190|1|Spring|2009
83821|Brandt|Comp. Sci.|92000|CS-190|2|Spring|2009
83821|Brandt|Comp. Sci.|92000|CS-319|2|Spring|2010
98345|Kim|Elec. Eng.|80000|EE-181|1|Spring|2009
```

From above query result we can note that

1. we do not repeat those attributes that appear in the schemas of both relations;
rather they appear only once.

2. the order in which the attributes are listed: first the attributes common to the schemas
of both relations, second those attributes unqiue to the schema of the first relation, and
finally, those attribute unique to the schema of the second relation.

In addition, natural join will consider ALL the attributes that appear in the 
schemas of both relations. Consider the following query

```sql
select *
from instructor natural join teaches natural join course;
```

*course* table looks like the following

```
sqlite> select * from course;
course_id|title|dept_name|credits
BIO-101|Intro. to Biology|Biology|4
BIO-301|Genetics|Biology|4
BIO-399|Computational Biology|Biology|3
CS-101|Intro. to Computer Science|Comp. Sci.|4
CS-190|Game Design|Comp. Sci.|4
CS-315|Robotics|Comp. Sci.|3
CS-319|Image Processing|Comp. Sci.|3
CS-347|Database System Concepts|Comp. Sci.|3
EE-181|Intro. to Digital Systems|Elec. Eng.|3
FIN-201|Investment Banking|Finance|3
HIS-351|World History|History|3
MU-199|Music Video Production|Music|3
PHY-101|Physical Principles|Physics|4
```

*instructor* has attributes (`ID|name|dept_name|salary`); 
*teaches* has attributes (`ID|course_id|sec_id|semester|year`);
*course* has attributes (`course_id|title|dept_name|credits`). The first `natural join`
will first do cartesian product of *instructor* and *teaches* and 
keep the tuples that have the same value on "ID". Then, the resulting relation
will do the second `natural join` with *course* and 
will keep the tuples that have the same value on "course_id" and "dept_name".

```
sqlite> select * from instructor natural join teaches natural join course;
ID|name|dept_name|salary|course_id|sec_id|semester|year|title|credits
10101|Srinivasan|Comp. Sci.|65000|CS-101|1|Fall|2009|Intro. to Computer Science|4
10101|Srinivasan|Comp. Sci.|65000|CS-315|1|Spring|2010|Robotics|3
10101|Srinivasan|Comp. Sci.|65000|CS-347|1|Fall|2009|Database System Concepts|3
12121|Wu|Finance|90000|FIN-201|1|Spring|2010|Investment Banking|3
15151|Mozart|Music|40000|MU-199|1|Spring|2010|Music Video Production|3
22222|Einstein|Physics|95000|PHY-101|1|Fall|2009|Physical Principles|4
32343|El Said|History|60000|HIS-351|1|Spring|2010|World History|3
45565|Katz|Comp. Sci.|75000|CS-101|1|Spring|2010|Intro. to Computer Science|4
45565|Katz|Comp. Sci.|75000|CS-319|1|Spring|2010|Image Processing|3
76766|Crick|Biology|72000|BIO-101|1|Summer|2009|Intro. to Biology|4
76766|Crick|Biology|72000|BIO-301|1|Summer|2010|Genetics|4
83821|Brandt|Comp. Sci.|92000|CS-190|1|Spring|2009|Game Design|4
83821|Brandt|Comp. Sci.|92000|CS-190|2|Spring|2009|Game Design|4
83821|Brandt|Comp. Sci.|92000|CS-319|2|Spring|2010|Image Processing|3
98345|Kim|Elec. Eng.|80000|EE-181|1|Spring|2009|Intro. to Digital Systems|3
```

##### join ... using

Automatically equate all the attributes with the same name from both schemas of 
relations may be too strong. Quite often, we may want to do `natural join` on 
specific subsets of the common-shared attributes. This leads to our join condition
grammar: `join ... using (`$A_1, A_2, \dots, A_n$`)`. The operation requires 
a list of attribute names to be specified. Both inputs must have attributes with the specified
names. Consider the operation $r_1$ `join` $r_2$ `using (` $A_1, A_2$ `)`. The operation
is similar to $r_1$ `natural join` $r_2$, execpt that a pair of tuples $t_1$ from
$r_1$ and $t_2$ from $r_2$ match if $t_1.A_1 = t_2.A_1$ and $t_1.A_2 = t_2.A_2$;
even if $r_1$ and $r_2$ both have an attribute named $A_3$, it is *not* required
that $t_1.A_3 = t_2.A_3$. 

An example query look like

```sql
select name, title
from (instructor natural join teaches) join course using (course_id);
```

##### join ... on

Another form of join condition is the **on** condition, which allows a general 
predicate over the relations being joined. The predicte is written like a **where**
clause predicate except for the use of the keyword **on** rahter than **where**.

For example, the below two queries are equivalent with each other (i.e. gives the 
same result)

```sql
select * from student join takes on student.ID = takes.ID;

select * from student, takes where student.ID = takes.ID;
```

!!!note
    The query is almost the same as using `student natural join takes`, except that
    the "ID" columns twices in the result set. 

One question we may ask is why do we need this **on** operation if it may look
like working exactly the same as **where** clause? The answer is

1. **on** conditions behaves different from **where** conditions when we work with
**outer join**.

2. SQL query is often more readable by humans if the join condition is specified in the 
**on** clause and the rest of the conditions appear in the **where** clause. 

#### outer join

##### Motivation

Let's consider *student* and *takes* tables look like the below

```
sqlite> select * from student;
ID|name|dept_name|tot_cred
00128|Zhang|Comp. Sci.|102
12345|Shankar|Comp. Sci.|32
19991|Brandt|History|80
23121|Chavez|Finance|110
44553|Peltier|Physics|56
45678|Levy|Physics|46
54321|Williams|Comp. Sci.|54
55739|Sanchez|Music|38
70557|Snow|Physics|0
76543|Brown|Comp. Sci.|58
76653|Aoi|Elec. Eng.|60
98765|Bourikas|Elec. Eng.|98
98988|Tanaka|Biology|120

sqlite> select * from takes;
ID|course_id|sec_id|semester|year|grade
00128|CS-101|1|Fall|2009|A
00128|CS-347|1|Fall|2009|A-
12345|CS-101|1|Fall|2009|C
12345|CS-190|2|Spring|2009|A
12345|CS-315|1|Spring|2010|A
12345|CS-347|1|Fall|2009|A
19991|HIS-351|1|Spring|2010|B
23121|FIN-201|1|Spring|2010|C+
44553|PHY-101|1|Fall|2009|B-
45678|CS-101|1|Fall|2009|F
45678|CS-101|1|Spring|2010|B+
45678|CS-319|1|Spring|2010|B
54321|CS-101|1|Fall|2009|A-
54321|CS-190|2|Spring|2009|B+
55739|MU-199|1|Spring|2010|A-
76543|CS-101|1|Fall|2009|A
76543|CS-319|2|Spring|2010|A
76653|EE-181|1|Spring|2009|C
98765|CS-101|1|Fall|2009|C-
98765|CS-315|1|Spring|2010|B
98988|BIO-101|1|Summer|2009|A
98988|BIO-301|1|Summer|2010|
```

Suppose we wish to display a list of all students along with the courses they have
taken. We come up a query that looks like

```sql
select *
from student natural join takes;
```

This query actually is not right for our purpose because it will not show
the student who takes no course. This is because his "ID" will only appear
in *student* table not in *takes* table. If we do `natural join`, the value
of "ID" will not equal (one is a number and the other is NULL), which will
not show up in our final result set. Example in our case will be student Snow
with "ID" 70557, who has not taken any course. 

```
sqlite> select * from student natural join takes;
ID|name|dept_name|tot_cred|course_id|sec_id|semester|year|grade
00128|Zhang|Comp. Sci.|102|CS-101|1|Fall|2009|A
00128|Zhang|Comp. Sci.|102|CS-347|1|Fall|2009|A-
12345|Shankar|Comp. Sci.|32|CS-101|1|Fall|2009|C
12345|Shankar|Comp. Sci.|32|CS-190|2|Spring|2009|A
12345|Shankar|Comp. Sci.|32|CS-315|1|Spring|2010|A
12345|Shankar|Comp. Sci.|32|CS-347|1|Fall|2009|A
19991|Brandt|History|80|HIS-351|1|Spring|2010|B
23121|Chavez|Finance|110|FIN-201|1|Spring|2010|C+
44553|Peltier|Physics|56|PHY-101|1|Fall|2009|B-
45678|Levy|Physics|46|CS-101|1|Fall|2009|F
45678|Levy|Physics|46|CS-101|1|Spring|2010|B+
45678|Levy|Physics|46|CS-319|1|Spring|2010|B
54321|Williams|Comp. Sci.|54|CS-101|1|Fall|2009|A-
54321|Williams|Comp. Sci.|54|CS-190|2|Spring|2009|B+
55739|Sanchez|Music|38|MU-199|1|Spring|2010|A-
76543|Brown|Comp. Sci.|58|CS-101|1|Fall|2009|A
76543|Brown|Comp. Sci.|58|CS-319|2|Spring|2010|A
76653|Aoi|Elec. Eng.|60|EE-181|1|Spring|2009|C
98765|Bourikas|Elec. Eng.|98|CS-101|1|Fall|2009|C-
98765|Bourikas|Elec. Eng.|98|CS-315|1|Spring|2010|B
98988|Tanaka|Biology|120|BIO-101|1|Summer|2009|A
98988|Tanaka|Biology|120|BIO-301|1|Summer|2010|
```

More generallyy, some tuples in either or both of the relations being joined 
may be "lost" in this way. The **outer join** operation works in a manner similar
to the join operations we studied above, but preserve those tuples that would be
lost in a join, by creating tuples in the result containing null values.

##### outer join

There are three forms of outer join:

- The **left outer join** preserves tuples only in the relation named before
(to the left of) the `left outer join` operation.

- The **right outer join** preserves tuples only in the relation named after
(to the right of) the `right outer join` operation.

- The **full outer join** preserves tuples in both relations.

For our example, the actual query should be

```sql
select * 
from student natural left outer join takes;
```

which returns result that includes student Snow with nulls for the
attributes that appear only in the schema of the *take* relation

```
sqlite> select * from student natural left outer join takes;
ID|name|dept_name|tot_cred|course_id|sec_id|semester|year|grade
00128|Zhang|Comp. Sci.|102|CS-101|1|Fall|2009|A
00128|Zhang|Comp. Sci.|102|CS-347|1|Fall|2009|A-
12345|Shankar|Comp. Sci.|32|CS-101|1|Fall|2009|C
12345|Shankar|Comp. Sci.|32|CS-190|2|Spring|2009|A
12345|Shankar|Comp. Sci.|32|CS-315|1|Spring|2010|A
12345|Shankar|Comp. Sci.|32|CS-347|1|Fall|2009|A
19991|Brandt|History|80|HIS-351|1|Spring|2010|B
23121|Chavez|Finance|110|FIN-201|1|Spring|2010|C+
44553|Peltier|Physics|56|PHY-101|1|Fall|2009|B-
45678|Levy|Physics|46|CS-101|1|Fall|2009|F
45678|Levy|Physics|46|CS-101|1|Spring|2010|B+
45678|Levy|Physics|46|CS-319|1|Spring|2010|B
54321|Williams|Comp. Sci.|54|CS-101|1|Fall|2009|A-
54321|Williams|Comp. Sci.|54|CS-190|2|Spring|2009|B+
55739|Sanchez|Music|38|MU-199|1|Spring|2010|A-
70557|Snow|Physics|0|||||
76543|Brown|Comp. Sci.|58|CS-101|1|Fall|2009|A
76543|Brown|Comp. Sci.|58|CS-319|2|Spring|2010|A
76653|Aoi|Elec. Eng.|60|EE-181|1|Spring|2009|C
98765|Bourikas|Elec. Eng.|98|CS-101|1|Fall|2009|C-
98765|Bourikas|Elec. Eng.|98|CS-315|1|Spring|2010|B
98988|Tanaka|Biology|120|BIO-101|1|Summer|2009|A
98988|Tanaka|Biology|120|BIO-301|1|Summer|2010|
```

We mention earlier that **on** and **where** behave differently
for outer join. Let's consider the following example

```sql
select *
from student left outer join takes on true
where student.ID = takes.ID
```

This gives the following result [^1]

[^1]: `on true` is equivalent to `student left outer join takes`. 

```
sqlite> select * from student left outer join takes where student.ID = takes.ID;
ID|name|dept_name|tot_cred|ID|course_id|sec_id|semester|year|grade
00128|Zhang|Comp. Sci.|102|00128|CS-101|1|Fall|2009|A
00128|Zhang|Comp. Sci.|102|00128|CS-347|1|Fall|2009|A-
12345|Shankar|Comp. Sci.|32|12345|CS-101|1|Fall|2009|C
12345|Shankar|Comp. Sci.|32|12345|CS-190|2|Spring|2009|A
12345|Shankar|Comp. Sci.|32|12345|CS-315|1|Spring|2010|A
12345|Shankar|Comp. Sci.|32|12345|CS-347|1|Fall|2009|A
19991|Brandt|History|80|19991|HIS-351|1|Spring|2010|B
23121|Chavez|Finance|110|23121|FIN-201|1|Spring|2010|C+
44553|Peltier|Physics|56|44553|PHY-101|1|Fall|2009|B-
45678|Levy|Physics|46|45678|CS-101|1|Fall|2009|F
45678|Levy|Physics|46|45678|CS-101|1|Spring|2010|B+
45678|Levy|Physics|46|45678|CS-319|1|Spring|2010|B
54321|Williams|Comp. Sci.|54|54321|CS-101|1|Fall|2009|A-
54321|Williams|Comp. Sci.|54|54321|CS-190|2|Spring|2009|B+
55739|Sanchez|Music|38|55739|MU-199|1|Spring|2010|A-
76543|Brown|Comp. Sci.|58|76543|CS-101|1|Fall|2009|A
76543|Brown|Comp. Sci.|58|76543|CS-319|2|Spring|2010|A
76653|Aoi|Elec. Eng.|60|76653|EE-181|1|Spring|2009|C
98765|Bourikas|Elec. Eng.|98|98765|CS-101|1|Fall|2009|C-
98765|Bourikas|Elec. Eng.|98|98765|CS-315|1|Spring|2010|B
98988|Tanaka|Biology|120|98988|BIO-101|1|Summer|2009|A
98988|Tanaka|Biology|120|98988|BIO-301|1|Summer|2010|
```

Here, `left outer join` esentially returns a cartesian product of two relations.
Since there is no tuple in *take* with ID = 70577, every time a tuple appears in the outer
join with name = "Snow", the values for student.ID and takes.ID must be different, and
such tuples would be eliminated by the `where` clause predicate. Thus, student
Snow never appears in the result of the latter query.

### Relational algebra perspective

In the previous section, we spend quite some time understanding `join` from SQL
perspective. In this section, we try to under the clause from relational algebra
perspective.

In relational algebra, a operator accepts (one or two) relation instances as argument
and returns a relation instance as the result: $f(R_1, R_2) \to R_3$. We have 
the following operators:

- $\sigma$: select rows from a relation  (i.e. $\sigma_{\text{grade} < B}(takes)$)
- $\pi$: extract columns from a relation (i.e. $pi_{\text{ID, name}}(student)$)

Then, for join we have following definitions:

- condition joins: $R \bowtie_c S = \sigma_c (R \times S)$ 
(i.e. $\text{student} \bowtie_{\text{student.id < takes.id}} \text{takes}$)

Does this look familar to you? Yes, this exactly corresponds to `join ... on ...` usage.

- equijoin: $R \bowtie_c S$ ( $c$ consists **solely** of equalities)
(i.e. $\text{student} \bowtie_{\text{student.id = takes.id}} \text{takes}$)

This is equivalent to `join ... using (...)` usage.

- natural join: $R \bowtie S$ (equijoin where equalities are specified on all fields having the same 
name in $R$ and $S$) (i.e. $$\text{student} \bowtie \text{takes}$).

Well, this is exactly the `natural join` usage.

In fact, this perspective is acutally how people explain `join` to others. There
are two excellent pages offer graphical explaination to this concept. Their links
are attached in the "Links to resources" section.

## A leetcode example

Now, let's take a look at [leetcode 175. Combine Two tables](https://leetcode.com/problems/combine-two-tables/#/description)
for practice. 

The problem ask us to 

> Write a SQL query for a report that provides the following information
> (FirstName, LastName, City, State) 
> for each person in the Person table, regardless if there is an address for each of those people.

"regardless if there is an address for each of those people" is a clear indicator
for us to use `outer join` because we still want to keep all the person even 
they may not appear in the "Address" table. There are several queries we can write

```sql
# Solution 1
select FirstName, LastName, City, State from Person natural left outer join Address

# Solution 2
select FirstName, LastName, City, State from Person left outer join Address on Person.PersonId = Address.PersonId

# Solution 3
select FirstName, LastName, City, State from Person left outer join Address using (PersonId)

# Solution 4
select FirstName, LastName, City, State from Address right outer join Person using (PersonId)

# Solution 5
select FirstName, LastName, City, State from Address right outer join Person on Address.PersonId = Person.PersonId

# Solution 6
select FirstName, LastName, City, State from Address natural right outer join Person
```

We should have no trouble to understand these queries now. 

## Links to resources

Here are some of the resources I found helpful while preparing this article:

- [Database System Concepts](https://www.amazon.com/Database-System-Concepts-Computer-Science/dp/0073523321)
Chapter 3, 4
- [DB2 10.1 fundamentals certification exam 610 prep, Part 4](https://www.ibm.com/developerworks/data/tutorials/db2-cert6104/index.html)
- [Database Management Systems](http://pages.cs.wisc.edu/~dbbook/) Chapter 4
- [Code project page](https://www.codeproject.com/Articles/33052/Visual-Representation-of-SQL-Joins) and
[SO post](https://stackoverflow.com/questions/38549/what-is-the-difference-between-inner-join-and-outer-join) have
nice graphic explanation to this concept that is worth checking out.
- [What is natural join in SQLite?](http://www.w3resource.com/sqlite/sqlite-natural-join.php)
