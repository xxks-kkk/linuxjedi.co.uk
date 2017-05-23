Title: Andrew Ng's ML Week 04 - 05
Date: 2017-05-23 17:18
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

- $L =$ total number of layers in network (i.e. $L = 4$ for the above NN)

- $S_l =$ number of units (not counting bias unit) in layer $l$ 
(i.e., $S_1 = 3$, $S_2 = S_3 = 5$, $S_4 = S_L = 4$)

- $a_i^l =$ "activation" of unit $i$ in layer $l$. In fact, input features
$x_0, x_1, x_2, x_3$ can also be represented as $a_0^{(1)}, a_1^{(1)}, a_1^{(2)}, a_1^{(3)}$
respectively.

- $\Theta^{(l)} =$ matrix of weights controlling function mapping from layer $l$ to layer $l+1$.
For example, [^1]

```
$$
\Theta^{(1)} = \begin{bmatrix} 
\theta_{10}^{(1)} && \theta_{11}^{(1)} && \theta_{12}^{(1)} && \theta_{13}^{(1)} \\
\theta_{20}^{(1)} && \theta_{21}^{(1)} && \theta_{22}^{(1)} && \theta_{23}^{(1)} \\
\dots \\
\theta_{50}^{(1)} && \theta_{51}^{(1)} && \theta_{52}^{(1)} && \theta_{53}^{(1)} \\
\end{bmatrix}
$$ 

[^1]: Notation here may look confusing. One example to help understand is
$\theta_{10}^{1}$ means weight from $x_0$ in layer $1$ to $a_1$ in layer $2$. In other words,
$\theta_{ji}^{l}$ means weight from $a_i^{l}$ to $a_j^{l+1}$. Then the rows in the
matrix can be thought of as the weights from neurons in layer $l$ to corresponding $a_j$ in layer $l+1$ 
(i.e., 1st row in the above example means weights from layer $1$ to $a_1$ in layer $2$).

- $k =$ number of neurons in the output layer (i.e. $S_L = k$). In other words, $k$ represents the number of classes
in multi-class classification. This indicates that $h_\theta(x) = \mathbb{R}^k$. [^2]

[^2]: Usually, in our training sets {$(x^{(1)}, y^{(1)}), \dots, (x^{(m)}, y^{(m)})$}, we are given actual label (i.e. 
$y^{(9)} = 10$ for handwritten digit recognition). However, we need to transform those labels into $\mathbb{R}^k$ by doing,for instance, create $\mathbb{R}^{10}$ vector with last position being $1$ and rest being $0$
as the representation for $y^{(9)} = 10$.

With the above notations, we have the following property:

- If NN has $S_l$ units in layer $l$, $S_{l+1}$ units in layer $l+1$, then $\Theta^{(l)}$ will be dimension 
$S_{l+1} \times (S_l + 1)$. $+1$ comes from the bias unit (shown in yellow in above NN picture). 

### Train a neural network

#### 1. Pick a network architecture

The first step is to pick a network architecture. Specifically, the connectivity patterns between neurons. Prof. Ng 
says a reasonable default is to either have $1$ hidden layer, or if $>1$ hidden layer, have the same number of 
hidden units in every layer. Usually, the more hidden units the better. 

#### 2. Randomly initialize weights

Zero initialization is considered bad for NN (i.e. $\theta_{ij}^{l}$ for all $i,j,l$) because our activation output and
gradient will all be identical and essentially we comput one feature in this network. That's why we need to randomly 
initialize the weights for symmetry breaking. 

One effective strategy is to randomly select values for $\theta_{ij}^{l}$ uniformly in the range 
[$-\epsilon_\text{init}$,$\epsilon_\text{init}$]. You can choose $\epsilon_\text{init}$ based upon
the number of units in the network. A good choice of $\epsilon_\text{init}$ is 
$\epsilon_\text{init} = frac{\sqrt{6}}{\sqrt{L_\text{in} + L_\text{out}}}$, where
$L_\text{in} = S_l$ and $L_\text{out} = S_{l+1}$, which are the the number of units
in the layers adjacent to $\Theta_{(l)}$. Take above NN as an example, our 
$\epsilon_\text{init}$ will be $0.87$, which is calculated from $\frac{\sqrt{6}}{\sqrt{3+5}}$.

## Implementation details

