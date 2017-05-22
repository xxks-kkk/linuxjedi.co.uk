Title: Andrew Ng's ML Week 04-05
Date: 2017-05-05 16:18
Category: Machine Learning
Tags: ml, coursera
Summary: neural network

Week 4 and 5 mainly talks about one important learning technique called "Neural Networks".
It is especially heplful when there are many features and hence, many combinations
for the [linear or logistic regressions]({filename}/blog/2017/04/21/andrew-ml-01.md). 
Interestingly, I have studied neural networks
[previously](https://www.dropbox.com/s/hkym4s135amgmxv/HU.pdf?dl=0) 
when I was a student at college. It may feel different when we revisit old friend.

[TOC]

## Model

### Representations

Below picture shows a typical neural network (I'll use NN as a shorthand). 

![]({filename}/images/nn2.png) 

- $L = \text{total number of layers in network}$ (i.e. $L = 4$ for the above NN)

- $S_l = \text{number of units (not counting bias unit) in layer $l$}$ 
(i.e., $S_1 = 3$, $S_2 = S_3 = 5$, $S_4 = S_L = 4$)

- $a_i^(l) = \text{"activation" of unit $i$ in layer $l$}$. In fact, input features
$x_0, x_1, x_2, x_3$ can also be represented as $a_0^(1), a_1^(1), a_1^(2), a_1^(3)$
respectively.

- $\Theta^(l) = \text{matrix of weights controlling function mapping from layer $l$ to layer $l+1$}$.
For example,

```
$$
\Theta^(1) = \begin{bmatrix} 
\theta_{10}^(1) && \theta_{11}^(1) && \theta_{12}^(1) && \theta_{13}^(1) \\
\theta_{20}^(1) && \theta_{21}^(1) && \theta_{22}^(1) && \theta_{23}^(1) \\
\vdots \\
\theta_{50}^(1) && \theta_{51}^(1) && \theta_{52}^(1) && \theta_{53}^(1) \\
\end{bmatrix}
$$ [^1]

[^1]: Notation here may look confusing. One example to help understand is
$\theta_{10}^{1}$ means weight from $x_0$ in layer $1$ to $a_1$ in layer $2$. In other words,
$\theta_{ji}^{l}$ means weight from $a_i^{l}$ to $a_j^{l+1}$. Then the rows in the
matrix can be thought of as the weights for each corresponding $a_j$.



## Implementation details

