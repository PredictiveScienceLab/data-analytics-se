(uncertainty-propagation-problem)=
# The Uncertainty Propagation Problem

Suppose you have some random vector $X$.
(I won't bother making the random vector bold, because I'm lazy. But you can assume that $X$ takes values in $\mathbb{R}^d$.)
Maybe it represents the unknown parameters of a physical model, or maybe it represents the initial conditions of a simulation.
Let $g(x)$ denote the result of some computation that depends on $x$.
The function $g(x)$ may also be a vector, but for now let's assume it's a scalar.
For example, $g(x)$ might be the solution of a differential equation with initial condition $x$ at a particular time.
Or, $g(x)$ might be the maximum stress found by solving a boundary value problem using the finite element method with physical parameters $x$.
The uncertainty propagation problem is to compute the expected value of $g(x)$, i.e.,

$$
\mathbb{E}[g(X)] = \int_{\mathbb{R}^d} g(x) p(x) dx,
$$

as well as higher statistics of $g(X)$, such as its variance,

$$
\mathbb{V}[g(X)] = \mathbb{E}[(g(X) - \mathbb{E}[g(X)])^2] = \int_{\mathbb{R}^d} (g(x) - \mathbb{E}[g(X)])^2 p(x) dx.
$$

Or even the cumulative distribution function of $g(X)$,

$$
F(y) = p[g(X) \leq y] = \int_{\mathbb{R}^d} 1_{(-\infty, y]}(g(x)) p(x) dx,
$$

where $1_A(x)$ is the indicator function of the set $A$, i.e., $1_A(x) = 1$ if $x \in A$ and $1_A(x) = 0$ if $x \notin A$.

```{note}
Observe that all the statistics of $g(X)$ are defined in terms of integrals over $\mathbb{R}^d$.
So, we need to be able to compute integrals over $\mathbb{R}^d$ in order to solve the uncertainty propagation problem.
And it turns out that doing these integrals when $d$ is large is very hard.
This is known as the curse of dimensionality.
```

(curse-of-dimensionality)=
## The Curse of Dimensionality

To make things simpler, take $X$ to be a uniform random variable in $[0,1]^d$.
The the PDF of $X$ is:

$$
p(x) = \begin{cases}
1 & \text{if } x \in [0,1]^d \\
0 & \text{otherwise}
\end{cases}
$$

Take any function $g(x)$.
We want to estimate the expected value of $g(X)$, i.e.,

$$
\mathbb{E}[g(X)] = \int_{[0,1]^d} g(x) dx.
$$

The simplest way to estimate this integral is to use the midpoint rule.
Divide $[0,1]^d$ into $n^d$ subintervals of length $1/n$ in each dimension.
Then, the midpoint rule says that

$$
\int_{[0,1]^d} g(x) dx \approx \frac{1}{n^d} \sum_{i_1=1}^n \cdots \sum_{i_d=1}^n g\left(\frac{i_1}{n}, \ldots, \frac{i_d}{n}\right).
$$

This is just a Riemann sum.
The number of terms in the sum is $n^d$.
This is the curse of dimensionality.
As the dimension $d$ increases, the number of terms in the sum increases exponentially.

Let's make it concrete.
Suppose that the evaluation of $g(x)$ takes one milisecond.
And let's say we take $n=10$ points in each dimension.
Then, the number of terms in the sum is $10^d$.
If $d=2$, then the number of terms is 100, and we need 0.1 seconds to evaluate the sum.
If $d=3$, then the number of terms is 1000, and we need 1 second to evaluate the sum.
If $d=5$, then the number of terms is 100,000, and we need 100 seconds to evaluate the sum.
If $d=10$, then the number of terms is 10 billion, and we need 10 million seconds to evaluate the sum.
This is 115 days!
For $d=20$, we need 3.1 billion years!

So clearly, we need a better way to estimate the expected value of $g(X)$.
This is what the Monte Carlo method is all about.
