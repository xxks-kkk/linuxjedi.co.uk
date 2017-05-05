Title: Andrew Ng's ML Week 01 - 03
Date: 2017-05-05 16:18
Category: Machine Learning
Tags: ml, coursera
Summary: ML overview, Linear regression, Logistic regression, Regularization 

In my [introducing post]({filename}/blog/2017/04/20/andrew-ml-00.md), I mention that
I decide to write summary post weekly for the course. However, in practice, I find
it is very hard to do. This is mainly because I want to keep the progress in MAW 
reading while meet the coursework deadlines. So, I decide to do the summary post
based upon the module of the material itself.

In addition, like MAW reading posts, I will focus on the reflection and the post itself
may not be self-contained. However, this may happen rarely.

\* ---- Note ---- *

> Coursera has really well-designed programming assignment that really helps to understand
> both concepts and its actual implementation. All the code snippets listed in the below
> and upcoming posts are availabe [in my code-for-blog repo](https://github.com/xxks-kkk/Code-for-blog/tree/master/2017/andrew-ng-ml).

## ML overview

### What is ML?

The biggest take-away for me is that ML is to solve the problems that
cannot be easily solved by the programming. As mentioned by Prof. Andrew, we
know how to program the shortest path from A to B but we may have hard time
to program a solution to do image tagging, email spam checking, and so on.
The way we solve those problems is by teaching computers to do things like us
through learning algorithms.

There are a lot of examples about ML mentioned in the video:

- Database mining: large datasets from growth of automation/web (i.e. web click data,
medical records, biology, engineering)

- Applications can't program by hand. (i.e. autonomous helicopter, 
handwriting recognition, most of NLP, CV)

- Self-customizing programs (i.e. Amazon, Netflix product recommendations)

- Understanding human learning (brain, real AI)

There are two definitions for ML: 

- Arthur Samuel: the field of study that gives computers the ability to learn
without being explicitly programmed. (older, informal definition)

- Tom Mitchell: A computer program is said to learn from experience $E$ with respect
to some class of tasks $T$ and performance measure $P$, if its performance at tasks in $T$,
as measured by $P$, improves with experience $E$.

Take playing checkers as an example. $E = \text{the experience of playing many games of checkers}$;
$T = \text{the task of playing checkers}$; $P = \text{the probability that the program will win the next game}$.

### Types of ML problems

There are two general types:  Supervised learning and Unsupervised learning.

- Supervised learning: 'right' answer given

    - Regression: predict continuous valued output
        
        - EX1: given data about the size of houses on the real estate market, try to predict their price.
        - EX2: given a picture of a person, we predict their age on the basis of the given picture.
      
    - Classification: predict results in a discrete output (categories)

        - EX1: predict whether the house sells for more or less than the asking price.
        - EX2: given a patient with a tumor, we predict whether the tumor is malignant or benign.

- Unsupervised learning: little or no idea what our resuls should look like. We can
derive structure from data where we don't necessarily know the effect of the variables.

    - Clustering: take a collection of 1,000,000 different genes, and find a way to automatically group
    these genes into groups that are somehow similar or related by different variables (i.e. lifespan, location, roles)

    - Non-clustering: the "cocktail party algorithm" allows you to find structure in a 
    chaotic environment (i.e. identifying individual voices and music from a mesh of sounds at a cocktail party)

    - Other application fields: organize computing clusters, social network analysis, market segmentation, 
    astronomical data analysis

## Notation

A few notation used throughout the course:

- $n = \text{number of features}$
- $m = \text{number of training examples}$
- $x^{(i)} = \text{input (features) of }i\text{th training example}$
- $x_j^{(i)} = \text{value of feature }j \text{ in }i\text{th training example}$

## Linear regression

### In theory
For linear regression, our hypothesis is 

$$
h_\theta(x) = \theta_0 x_0 + \theta_1 x_1 + \dots + \theta_n x_n = \theta^T x  
$$

where 

$$
\begin{align*}
& x = \begin{bmatrix} x_0 \\ x_1 \\ \vdots \\ x_n \end{bmatrix} \in \mathbb{R} ^{n+1} \label{eq:1} &
& \theta = \begin{bmatrix} \theta_0 \\ \theta_1 \\ \vdots \\ \theta_n \end{bmatrix} \in \mathbb{R} ^{n+1}
\end{align*}
$$

and our cost function is 

$$
J(\theta) = \frac{1}{2m} \sum_{i=1}^m(\theta^T x^{(i)}-y(i))^2 \label{eq:2}
$$

In order to find $\theta$ that minimizes our cost function $J(\theta)$. Two methods are available for us:

- Gradient Descent

$$
\begin{align*} 
\text{Repeat\{ } && \\
&& \theta_j := \theta_j - \alpha \times \frac{1}{m} \sum_{i=1}^m(h_\theta(x^{(i)})-y^{(i)})x_j^{(i)} &&
\text{(simultaneously update $\theta_j$ for $j = 0, 1, \dots, n$)}  \label{eq:3}\\
\text{\}}
\end{align*}
$$

$\alpha$ is called learning rate, which determines "the step we take downhill" and the part afterwards decides
which direction we want to go (derived by taking partial derivatives against $\theta_j$).

\* ---- Note ---- *

> We may need to do feature scaling & pick up learning rate $\alpha$ wisely when we work with gradient descent.

- Normal Equation

We just directly calculate the partial derivatives for every $\theta_j$ and set it equals to zero 
(i.e $\frac{\partial}{\partial \theta_j}J(\theta) = 0$ for every $j$) and we get:

$$
\theta = (X^TX)^{-1}X^Ty \label{eq:4}
$$

where $X$ is called *design matrix*, and it has form

$$
\begin{align*} 
& x = \left[\begin{array}{ccc} - & (x^{(1)})^T & - \\ - & (x^{(2)})^T & - \\ & \vdots & \\ - & (x^{(m)})^T & -\end{array} \right] &
x^{(i)} = \begin{bmatrix}x_0^{(i)} \\ \vdots \\ x_n^{(i)} \end{bmatrix} \in \mathbb{R} ^{n+1}
\end{align*}
$$

### In practice

One tricky thing I find out when I work through quiz and programming problems 
is the gap between the mathematical representation and the actual implementation.

For the cost function \ref{eq:2}, we implement it in Octave as following:

```{octave}
J = 1/(2*m) * (X*theta-y)' * (X*theta - y); 
```

where 

$$
X = \begin{bmatrix} 
x_0^{(1)} && x_1^{(1)} && \dots && x_n^{(1)} \\
x_0^{(2)} && x_1^{(2)} && \dots && x_n^{(2)} \\
\vdots \\
x_0^{(m)} && x_1^{(m)} && \dots && x_n^{(m)}
\end{bmatrix}
$$

Note that $X$ here is different from \ref{eq:1} because $X$ here is to faciltate
the vectorized cost function calculation in program (i.e Octave) and it is natural
fit with how the data actually loaded into the program.

Also, if you take a look at our octave calculation above, we explictly avoid doing
summation in \ref{eq:2}. We can put both vectorized form used in octave and mathematical
definition side by side to see the pattern:

$$
J(\theta) = \frac{1}{2m}(X\theta-y)^T(X\theta-y) = \frac{1}{2m} \sum_{i=1}^m(\theta^T x^{(i)}-y(i))^2
$$

Matrix transpose times matrix itself is a commonly-seen technique that is used to
avoid explictly summation.

For gradient descent, we can calculate like the following in octave:

```{octave}
theta = theta - alpha * 1/m * (X'*(X*theta - y));
```

Let me use an example to illustrate why we can calculate \ref{eq:3} like above.
Suppose $m = 4$ with $h_\theta(x) = \theta_0x_0+\theta_1x_1$.
Then, we have

$$
\begin{align*} 
X = \begin{bmatrix}
x_0^{(1)} && x_1^{(1)} \\
x_0^{(2)} && x_1^{(2)} \\
x_0^{(3)} && x_1^{(3)} \\
x_0^{(4)} && x_1^{(4)} \\
\end{bmatrix} &&
\theta = \begin{bmatrix} \theta_0 \\ \theta_1 \end{bmatrix} &&
h_\theta(x^{(i)}) - y^{(i)} = \begin{bmatrix}
theta_0 + theta_1x_1^{(1)} - y^{(1)} \\
\vdots \\
theta_0 + theta_1x_1^{(4)} - y^{(4)}
\end{bmatrix}
\end{align*}
$$

so now we can show why:

$$
\begin{eqnarray*}
\sum+{i=1}^{m}(h_theta(x^{(i)})-y^{(i)})x_j^{(i)} \text{for all $j$} &=&
(theta_0 + theta_1x_1^{(1)} - y^{(1)}) \begin{bmatrix} x_0^{(1)} \\ x_1^{(1)} \end{bmatrix} + 
\dots + (theta_0 + theta_1x_1^{(4)} - y^{(4)}) \begin{bmatrix} x_0^{(4)} \\ x_1^{(4)} \end{bmatrix} \\
&=& \begin{bmatrix} x_0^{(1)} && x_0^{(2)} && x_0^{(3)} && x_0^{(4)} \\
x_1^{(1)} && x_1^{(2)} && x_1^{(3)} && x_1^{(4)}
\end{bmatrix} 
\begin{bmatrix}
theta_0 + theta_1x_1^{(1)} - y^{(1)} \\
\vdots \\
theta_0 + theta_1x_1^{(4)} - y^{(4)}
\end{bmatrix}
\end{eqnarray*}
$$

For normal equation, we can calculate like the following in octave:

```{octave}
theta = pinv(X'*X)*X'*y;
```

This is no different than \ref{eq:4} we mentioned above.

## Linear regression with regularization

Quite often, we may face *overfitting* issue, which can be fixed by either reduce number of features or
regularization.

Regularization is to keep all the features, but reduce magnitude (values) of parameters $\theta_j$. By
doing so, we can make our hypothesis simpler and less prone to overfitting.

### In theory

With regularization, our new cost function becomes 

$$
J(\theta) = \frac{1}{2m}\lbrack \sum_{i=1}^m (h_theta(x^{(i)}) - y^{(i)})^2 + 
\underbrace{\lambda \sum_{j=1}^n \theta_j^2\rbrack}_\textrm{regularization term}
$$

The regularization parameter $\lambda$ controls the tradeoff between "fit the data well" and
"keep parameters small to avoid overfitting".  If $\lambda$ is set to an extremely large
value, then we may face "underfit" issue (i.e. all $\theta_j$ for $j = 1, \dots, n$ close to 0).

\* ---- Note ---- *

> We don't penalize $\theta_0$.

Since our cost function has changed, both gradient descent and normal equation have to adjust accordingly:

- Gradient Descent

$$
\begin{align*} 
\text{Repeat\{ } && \\
&& \theta_0 := \theta_0 - \alpha \times \frac{1}{m} \sum_{i=1}^m(h_\theta(x^{(i)})-y^{(i)})x_0^{(i)} && \\
theta_j := \theta_j - \alpha \times \lbrack \frac{1}{m} \sum_{i=1}^m(h_\theta(x^{(i)})-y^{(i)})x_j^{(i)} + 
\frac{\lambda}{m}\theta_j\rbrack && (j = 1,2,3, \dots, n) \\
\text{\}}
\end{align*}
$$

- Normal Equation

$$
\theta = (X^TX + \lambda
\begin{bmatrix} 
0 &&    &&   &&       \\
  && 1  &&   &&       \\
  &&    && \ddots &&  \\
  &&    &&   &&  1
\end{bmatrix}
)^{-1}X^Ty
$$

we want $\lmbda > 0$ so that the matrix is invertible.

### In practice

Linear regression regularization implementation doesn't differ from no-regularization
implementation in terms of matrices implementation technique. I'll show a code snippet
for logistic regression with regularization below as hint for this section.

## Logistic regression

### In theory

Logistic regression hypothesis is 

$$
h_\theta(x) = g(\theta^Tx) \text{ where $g(z) = \frac{1}{1+e^{-z}}}
$$

This hypothesis can be intrepreted as the probability that $y = 1$ given $x$ and $\theta$
(i.e. $h_\theta(x) = P(y = 0 | x;\theta)$)

Then the cost function $J(\theta)$ is

$$
J(\theta) = -\frac{1}{m}\sum_{i=1}^m \lbrack 
(y^{(i)}\logh_\theta(x^{(i)}) + (1-y^{(i)})\log(1-h_\theta(x^{(i)})))\rback
$$

To minimize cost function $J(\theta)$ we can of course use gradient descent. Surprisingly,
the gradient descent for logistic regression is exactly the same as the gradient descent
for linear regression. 

However, in the course, we directly use the `fminunc` from Octave to do the optimization.
Internally, the function use advanced optimization technique that can avoid manually picking
$\alpha$ in gradient descent and find the optimal $\theta$ faster than gradient descent.

### In practice

The implementation for cost function and gradient descent for logistic regression
should be no hard for us now:

```{octave}
% cost function for logistic regression
J = 1/m * sum( ...
                 -y'*log(sigmoid(X*theta))- ...       
                 (1-y)'*log(1-sigmoid(X*theta)) ...    
             );
            
% gradient descent for logist regression
grad = 1/m * X'*(sigmoid(X*theta) - y);
```

## Logistic regression with regularization

### In theory

The cost function for regualarized logistic regression is following:

$$
J(\theta) = -\frac{1}{m}\sum_{i=1}^m \lbrack 
(y^{(i)}\logh_\theta(x^{(i)}) + (1-y^{(i)})\log(1-h_\theta(x^{(i)})))\rback
+ \frac{\lambda}{2m}\sum_{j=1}^n\theta_j^2
$$

and the gradient descent looks exactly the same as the regualarized linear regression.

## In practice

The following code chunk shows the cost function and gradient descent for regularized
logistic regression:

```{octave}
m = length(y);     % number of training examples
t = size(theta);   % number of theta parameters

J = 0;
grad = zeros(t);

J = 1/m * sum( ...
               -y'*log(sigmoid(X*theta)) ...
               -(1-y)'*log(1-sigmoid(X*theta)) ...
             ) ...
          + lambda / 2 / m * theta(2: t)'*theta(2: t);

grad(1) = (1/m * X'*(sigmoid(X*theta) - y))(1);
grad(2:t) =  (1/m * X'*(sigmoid(X*theta) - y) + lambda/m * theta)(2: t);
```