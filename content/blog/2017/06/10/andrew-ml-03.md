Title: Andrew Ng's ML Week 06, 11
Date: 2017-06-27 16:18
Category: Machine Learning
Tags: ml, coursera
Summary: Advice on building a machine learning system from course

I actually [finished the course](https://www.coursera.org/account/accomplishments/verify/58VFP5LF4UXV) 
last Sunday. I will save the course review for a post later. In this page, I'll
summarize various advices and tips given by Prof. Andrew Ng on how to build
a effective machine learning system.

To be honest, I used to think this part of material may be not worth a post 
but as I dig deeper into the course I find out that this part is invaluable 
because it answers some commonly-seen questions when implementing a machine learning
system, which can be a huge time-saver. So, I think I need a post to record
those advices systematically. 

[TOC]

## Preface

One important question we may ask after implementing our machine learning algorithm
is that: how good is our learning algorithm? In addition, for instance, after
we have implemented regularized linear regression to predict housing prices 
and when we test our hypothesis on a new set of houses, we find that it makes
unacceptably large errors in the predictions, what we should try next? This post
aims to answer those questions.

---- TO BE MODIFIED
In this post, I will first take a look at the diagnostic to evaluate learning algorithm.
Then, I will define overfitting (high bias) and underfitting (high variance)
concepts and the concrete techniques to identify which is which. Afterwards, I will
talk about several ways to handle the problem and highlight some key points. Lastly,
we will take a look at some special cases when data is skewed or large.
---- TO BE MODIFIED

## Diagnostics

**Diagnostics** is a test that you can run to gain insight what is or isn't working
with a learning algorithm, and gain guidance as to how best to improve its performance.
We use **test set error** as our basic metrics to evaulate our learning algorithm (hypothesis).

We first shuffle our whole data set to eliminate the potential impact of data record
ordering. Then, we randomly choose $70%$ of data set as our training set and the rest
$30%$ as our test set. Mathematically, we denote training set: 
$(x^{(1)}, y^{(1)}), (x^{(2)}, y^{(2)}), \dots, (x^{(m)}, y^{(m)})$ and we denote
test set as $(x_{\text{test}}^{(1)}, y_{\text{test}}^{(1)}), (x_{\text{test}}^{(1)}, y_{\text{test}}^{(1)}) \dots (x_{\text{test}}^{(m_\text{test})}, y_{\text{test}}^{(m_\text{test})})$ with
$m_\text{test} = \text{no. of test examples}$.

- For linear regression, our test set error is calculated by the following steps:

    1. Learn parameters $\theta$ from training data (i.e. minimizing training error $J(\theta)$)
    2. compute the test set error as follows:

    $$
    J_\text{test}(\theta) = \frac{1}{2m_\text{test}}\sum_{i=1}^{m_{test}}(h_\theta(x_{\text{test}}^{(i)})-y_\text{test}^{(i)})^2
    $$

- For logistic regression, we can use similar way like linear regression to calculate
test set error but there is a way due to the nature of classification task. In this
case, we also call test set error as **misclassification error** or **(0/1 misclassification error)**:

$$
\text{err}(h_\theta(x),y)=\left\{
                \begin{array}{ll}
                  1 \text{ if } h_\theta(x) \ge 0.5, y = 0 \text{ or if } h_\theta(x) < 0.5, y = 1 \\
                  0 \text{ otherwise }
                \end{array}
              \right.
$$

This definition gives us a binary $0$ or $1$ error result based on a misclassification.
Then, we calculate test set error as 

$$
\text{Test error} = \frac{1}{m_\text{error}}\sum_{i=1}^{m_\text{test}}
\text{err}(h_\theta(x_\text{test}^{(i)}),y_\text{test}^{(i)})
$$

This gives us the proportion of the test data that was misclassified.

In addition to the test set error, we will define **cross validation set error**
as well. Instead of dividing the whole data set as training set and test set, 
we can divide it into three parts: training set, corss validation (cv) set, and
test set, with proportion of data set as $60%$, $20%$, and $20%$. Mathematically,
similar to the notation of test set, we have $(x_{\text{cv}}^{(1)}, y_{\text{cv}}^{(1)}), (x_{\text{cv}}^{(1)}, y_{\text{cv}}^{(1)}) \dots (x_{\text{cv}}^{(m_\text{cv})}, y_{\text{cv}}^{(m_\text{cv})})$ with
$m_\text{cv} = \text{no. of cv examples}$. The purpose
of dividing data set in this way will be clear in the next section. 

Now, we summarize our metrics (training error, cross validation error, and test set error)
as follows:

$$
\begin{eqnarray*}
J_\text{train}(\theta) &=& \frac{1}{2m}\sum_{i=1}^m (h_\theta(x^{(i)}) - y^{(i)})^2 \\
J_\text{cv}(\theta)    &=& \frac{1}{2m_\text{cv}}\sum_{i=1}^{m_{cv}}(h_\theta(x_{\text{cv}}^{(i)})-y_\text{cv}^{(i)})^2 \\
J_\text{test}(\theta)  &=& \frac{1}{2m_\text{test}}\sum_{i=1}^{m_{test}}(h_\theta(x_{\text{test}}^{(i)})-y_\text{test}^{(i)})^2
\end{eqnarray*}
$$

## Overfitting

In [week 01-03 post]({filename}/blog/2017/04/21/andrew-ml-01.md), we mention
the term *overfitting* when we talk about regularization. Now, we explain it
in details. **Overfitting** happens when we have too many features, the learning
hypothesis may fit the training set very well (i.e.
$J(\theta)=\frac{1}{2m} \sum_{i=1}^m(\theta^T x^{(i)}-y(i))^2 \approx 0$) but
fail to generalize to new examples (i.e. predict prices on a new set of house). 
Take a look at the following three graphs

![overfitting example: linear regression]({filename}/images/overfitting.PNG)

The first graph (leftmost) shows the result of fitting our training set
with a hypothesis: $h_\theta(x) = \theta_0 + \theta_1 x$. You can see that
the data doesn't really lie on straight line, and so the fit is not very good.
In this case, we call the scenario **underfitting**, which means the model doesn't
capture the data structure well. Another term for this is **high bias**. One way
to think of **high bias** is that the algorithm has strong preconception on
what the data should be, in our case, linear. In summary, underfitting, or high bias,
is when the form of our hypothesis function $h$ maps poortly to the trend of the data. 
It is usually caused by a function that is too simple or uses too few features.

At the other extreme, shown by the rightmost graph, is **overfitting**, or **high variance**.
**High variance** means that the function can almost fit any function: hypothesis
$h$ is too general and we don't have enough data to constrain it. The overfitting or 
high variance is usually caused by a complicated function that creates a lot of unnecessary
curves and angles unrelated to the data. 

There are a couple of ways to tackle the overfitting problem:

1. Reduce number of features

    - Manually select which feature to keep
    - Model selection algorithm

2. Regularization, which can keep all the features, but reduce magnitude/values of parameters $\theta_j$.
This way works well when we have a lot of features, each of which contributes a bit to predicting $y$.

### Model selection algorithm

Once parameters $\theta_0, \theta_1, \dots$ were fit to some set of data (training set),
the error of the parameters as measured on that data (i.e. $J_\text{train}\theta$) 
is likely to be lower than the actual generalization error. In other words, 
$J_\text{train}\theta$ will be a bad metric on predicting how well our hypothesis
will be generalized to new examples. So, how do we measure how well our hypothesis
will perform on new examples? In addition, how to select which model to use? Ideally,
we should pick the model that has the best performance on new examples. As you can tell,
these two questions are equivalent and are all centered around the metrics we 
use for reporting our model generalization error.

We can start with the following schemes to pick our model. We use
$d$ to denote the degree of polynomial of our model. For example,
$d = 1$ means $h_\theta(x) = \theta_0 + \theta_1 x$; $d=2$ means
$h_\theta(x) = \theta_0 + \theta_1 x + \theta_2 x^2$. Then, we can do:

1. Optimize the parameters in $\Theta$ using the training set for each polynomial
degree $d$.
2. Find the polynomial degree $d$ with the least error $J_\text{test}(\theta)$
using the test set. We pick the model with this $d$ and report our
test set error $J_\text{test}(\theta)$ as the metric for estimate of generalization error.

However, there is a problem with this scheme: we use our extra parameter $d$ to fit
the test set. In other words, we choose $d$, then we fit with $J_\text{test}(\theta)$.
Our estimate is likely optimistic and our model is likely do better on test set 
than on new examples hasn't seen before. This is similar to overfitting in training set.

In order to fix this problem, we introduce **cross validation set**. We modify
above scheme as follows:

1. Optimize the parameters in $\Theta$ using the training set for each polynomial degree
2. Find the polynomial degree $d$ with the least error using the cross validation set
3. Estimate the generalization error using the test set with $J_\text{test}(\theta^{(d)})$
($\theta^{(d)}$ is the parameter $\Theta$ from polynomial with the lowest error)

This way, our $d$ has not been trained using the test set. 

### Diagnosing bias vs. variance: which is which?

Once we have the metrics and the understanding of cross validation set, we can
now find out whether bias or variance is the problem contributing to bad predictions. 
We have the following picture to help us understand the relationship bewtween $d$
and the underfitting (high bias) or overfitting (high variance) of our hypothesis

![bias vs. variance]({filename}/images/bias-variance.PNG)

The training error will tend to decrease as we increase the degree $d$ of polynomial
because our hypothesis fitness to our training data becomes better and better. 
On the other hand, the cross validation error will tend to decrease
as we increase $d$ up to a point (because our model can generalize well), and
then it will increase as $d$ increased (because we now overfit the training data and
cannot be generalize well in cross validation set), forming a convex curve.
So now, based on the picture, we can answer the question: suppose the learning algorithm is
performing less well than you were hoping ($J_\text{cv}(\theta)$ or $J_\text{test}(\theta)$ is high).
is it a bias problem or a variance problem?

- High bias (underfitting): $J_\text{train}(\theta)$ will be high; 
$J_\text{cv}(\theta) \approx J_\text{train}(\theta)$

- High variance (overfitting): $J_\text{train}(\theta)$ will be low;
$J_\text{cv}(\theta) \gg J_\text{train}(\theta)$

#### Learning curves

### Regularization: how to choose $\lambda$?

In the overfitting section above, we know that regularization is another way
to handle the overfitting. There is a problem with regularization method: how
do we set $\lambda$ appeard in the $J_\theta(x)$? In general, when $\lambda$
is large, we tend to underfit (i.e. high bias) the data and when $\lambda$ is small,
we tend to overfit (i.e. high variance). In the course, the following method
is proposed:

1. Create a list of $\lambda$ (i.e. $\lambda = 0, 0.01, 0.02, 0.04, \dots, 10.24$ (multiple of 2))
2. Create a set of models with different degrees or any other variants
3. Iterate through $\lambda$s and for each $\lambda$, go through all the models
to learn some $\theta$.
4. Compute the cross validation error $J_{cv}(\theta)$ without regularization term (i.e. $\lambda = 0$)
using the learned $\theta$.
5. Select the best combo that produces the lowest error on the cross validation set
6. Using the best combo $\lambda$ and $\theta$, apply it on $J_{test}(\theta)$
to see if it has a good generalization.

!!!note
    In this selection scheme, 

## Links to resources

Here are some of the resources I found helpful while preparing this article:

- [机器学习笔记7 高偏差/低偏差，学习曲线，模型选择](http://nanshu.wang/post/2015-05-17/)