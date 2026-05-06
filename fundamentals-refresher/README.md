# Fundamentals Refresher

A focused refresher and practice set for the math that matters in ML, written for someone who already has an ECE background and just needs to **shake the dust off**, not learn from scratch.

Three areas, in order of importance for ML:
1. Linear algebra (most important)
2. Probability
3. Optimization (light pass — just enough to follow ML training)

For each area: a short topic list with the **ML hook** (why it matters), then a small set of practice problems. Hints/answers are in collapsible sections so you can try first.

## How to use this

- Skim the topic list. If a topic feels foreign, that's a flag — go read about it before doing the problem.
- Do problems on paper. Speed isn't the goal; recall is.
- Each problem is meant to take 5–15 minutes. If one takes much longer, the gap is real and worth addressing before moving on.
- After each section, write 2 sentences in your own words about what each ML hook means. If you can't, the refresh didn't take.

---

## 1. Linear Algebra

### Topics to refresh

| Topic | ML hook |
|---|---|
| Vectors, dot products, norms (L1, L2, L∞) | Distances, similarity, regularization |
| Matrix multiplication and properties | Every neural net forward pass |
| Linear transformations, change of basis | What a layer of a network actually does |
| Rank, null space, column space | When systems have unique / no / infinite solutions; why models can be over- or under-determined |
| Eigenvalues and eigenvectors | PCA, stability of iterative methods, spectral methods |
| Singular Value Decomposition (SVD) | PCA, low-rank approximation, recommender systems, LoRA |
| Projections and least squares | Linear regression closed-form, embedding geometry |
| Positive (semi)definite matrices | Covariance matrices, Gaussian distributions, second-order optimization |
| Matrix calculus (gradient, Jacobian, Hessian) | Backpropagation, gradient-based optimization |
| Matrix factorizations (QR, LU, Cholesky) | Numerical solvers under the hood |

### Practice problems

**LA1.** Let $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$. Compute its eigenvalues and eigenvectors by hand.

<details><summary>Answer</summary>

Characteristic polynomial: $(2-\lambda)^2 - 1 = 0 \Rightarrow \lambda = 1, 3$. Eigenvectors: $(1, -1)^T$ for $\lambda=1$, $(1, 1)^T$ for $\lambda=3$.
</details>

**LA2.** For a vector $x \in \mathbb{R}^n$ and a symmetric matrix $A \in \mathbb{R}^{n \times n}$, what is $\nabla_x (x^T A x)$? What about when $A$ is **not** symmetric?

<details><summary>Answer</summary>

Symmetric: $2Ax$. Non-symmetric: $(A + A^T) x$. This shows up constantly in deriving gradients of loss functions.
</details>

**LA3.** What is the relationship between the SVD of $X$ (data matrix, samples × features) and the eigendecomposition of $X^T X$? Use this to explain how PCA works.

<details><summary>Answer</summary>

If $X = U \Sigma V^T$, then $X^T X = V \Sigma^2 V^T$. So the right singular vectors of $X$ are the eigenvectors of the (unnormalized) covariance, and the squared singular values are the eigenvalues. PCA = project data onto the top-$k$ right singular vectors.
</details>

**LA4.** Show that if $A$ is positive semi-definite, all its eigenvalues are non-negative.

<details><summary>Answer</summary>

If $Av = \lambda v$ with $v \neq 0$, then $v^T A v = \lambda \|v\|^2$. PSD means $v^T A v \geq 0$, so $\lambda \geq 0$.
</details>

**LA5.** You have an over-determined system $Ax = b$ with $A \in \mathbb{R}^{m \times n}$, $m > n$, no exact solution. Derive the least-squares solution from the normal equations.

<details><summary>Answer</summary>

Minimize $\|Ax - b\|^2$. Gradient: $2A^T(Ax - b) = 0 \Rightarrow A^T A x = A^T b \Rightarrow x = (A^T A)^{-1} A^T b$. Geometrically: project $b$ onto the column space of $A$.
</details>

**LA6.** Why is the rank of $A^T A$ equal to the rank of $A$? Why does this matter for whether $(A^T A)^{-1}$ exists in linear regression?

<details><summary>Answer</summary>

$A^T A x = 0 \Rightarrow x^T A^T A x = \|Ax\|^2 = 0 \Rightarrow Ax = 0$, so they share a null space and have the same rank. $(A^T A)^{-1}$ exists iff $A$ has full column rank — i.e., features are linearly independent. If features are collinear, the closed form breaks. (This is what L2 regularization fixes by adding $\lambda I$.)
</details>

**LA7.** Compute the L1, L2, and L∞ norms of $x = (3, -4, 0, 1)^T$.

<details><summary>Answer</summary>

L1: $|3| + |-4| + |0| + |1| = 8$. L2: $\sqrt{9 + 16 + 0 + 1} = \sqrt{26}$. L∞: $\max(3, 4, 0, 1) = 4$.
</details>

**LA8.** *(ML-tied)* In a fully connected layer $y = Wx + b$ with $W \in \mathbb{R}^{m \times n}$, what is $\frac{\partial y}{\partial x}$? What is $\frac{\partial L}{\partial W}$ if $L$ is a scalar loss and you know $\frac{\partial L}{\partial y}$?

<details><summary>Answer</summary>

$\frac{\partial y}{\partial x} = W$. $\frac{\partial L}{\partial W} = \frac{\partial L}{\partial y} \cdot x^T$ (outer product). This is one half of backprop through a linear layer.
</details>

### Resources (only if a topic feels rusty)

- 3Blue1Brown's *Essence of Linear Algebra* — geometric intuition, ~3h total.
- *Matrix Cookbook* (free PDF) — reference for matrix derivatives. Don't read it; bookmark it.

---

## 2. Probability

### Topics to refresh

| Topic | ML hook |
|---|---|
| Conditional probability, Bayes' rule | Bayesian inference, classification posteriors |
| Discrete distributions (Bernoulli, Binomial, Categorical, Multinomial, Poisson) | Logistic regression, softmax, count models |
| Continuous distributions (Gaussian, Exponential, Beta, Dirichlet) | Most parametric models, priors |
| Multivariate Gaussian | Generative models, GMMs, kernel methods, Gaussian processes |
| Expectation, variance, covariance | Loss functions, error bars, regularization derivations |
| Joint, marginal, conditional | Graphical models, sampling |
| Independence and conditional independence | Naive Bayes, Bayesian networks |
| Law of large numbers, CLT | Why minibatch gradients work; confidence intervals |
| Maximum Likelihood Estimation (MLE) | The principle behind nearly every ML loss function |
| MAP estimation, priors | Regularization as a prior |
| KL divergence, cross-entropy, entropy, mutual information | Classification loss, VAEs, information bottleneck |

### Practice problems

**P1.** A test for a disease is 99% accurate (both sensitivity and specificity). The disease has 0.1% prevalence. You test positive. What's the probability you actually have the disease?

<details><summary>Answer</summary>

$P(D \mid +) = \frac{0.99 \cdot 0.001}{0.99 \cdot 0.001 + 0.01 \cdot 0.999} \approx 0.090$. About 9%. Base rates dominate. (This is why "the model is 99% accurate" is meaningless without base rates.)
</details>

**P2.** $X \sim \text{Bernoulli}(p)$. You observe $n$ iid samples with $k$ successes. Derive the MLE for $p$.

<details><summary>Answer</summary>

Likelihood: $p^k (1-p)^{n-k}$. Log-likelihood: $k \log p + (n-k) \log(1-p)$. Derivative: $\frac{k}{p} - \frac{n-k}{1-p} = 0 \Rightarrow \hat{p} = k/n$. The intuitive answer falls out of the principle.
</details>

**P3.** Show that minimizing cross-entropy between the empirical distribution and the model distribution is equivalent to maximum likelihood.

<details><summary>Answer</summary>

Cross-entropy: $H(p, q) = -\sum_x p(x) \log q(x)$. With empirical $p$ as a uniform distribution over the $n$ data points, this becomes $-\frac{1}{n} \sum_i \log q(x_i)$ — the negative average log-likelihood. Minimizing it = maximizing likelihood.
</details>

**P4.** $X \sim \mathcal{N}(\mu_1, \sigma_1^2)$ and $Y \sim \mathcal{N}(\mu_2, \sigma_2^2)$, independent. What is the distribution of $X + Y$? What about $aX + b$ for constants $a, b$?

<details><summary>Answer</summary>

$X + Y \sim \mathcal{N}(\mu_1 + \mu_2, \sigma_1^2 + \sigma_2^2)$. $aX + b \sim \mathcal{N}(a\mu_1 + b, a^2 \sigma_1^2)$. Linear combinations of Gaussians stay Gaussian — the property that makes them so tractable.
</details>

**P5.** Compute the KL divergence $D_{KL}(P \| Q)$ for two univariate Gaussians $P = \mathcal{N}(\mu_1, \sigma_1^2)$, $Q = \mathcal{N}(\mu_2, \sigma_2^2)$.

<details><summary>Answer</summary>

$D_{KL} = \log \frac{\sigma_2}{\sigma_1} + \frac{\sigma_1^2 + (\mu_1 - \mu_2)^2}{2 \sigma_2^2} - \frac{1}{2}$. Note it's asymmetric: $D_{KL}(P \| Q) \neq D_{KL}(Q \| P)$. This shows up in VAEs (the KL-to-prior term).
</details>

**P6.** You roll a fair 6-sided die 100 times. By the CLT, what's the approximate distribution of the sample mean? What's the probability the sample mean is within 0.1 of 3.5?

<details><summary>Answer</summary>

Mean $= 3.5$, variance of one roll $= \frac{35}{12} \approx 2.92$. Sample mean $\sim \mathcal{N}(3.5, 2.92/100) = \mathcal{N}(3.5, 0.0292)$, std $\approx 0.171$. $P(|\bar{X} - 3.5| < 0.1) \approx P(|Z| < 0.1/0.171) \approx P(|Z| < 0.585) \approx 0.44$.
</details>

**P7.** A random variable has $E[X] = 0$ and $E[X^2] = 4$. What's the variance? Use Markov's or Chebyshev's inequality to upper-bound $P(|X| \geq 3)$.

<details><summary>Answer</summary>

$\text{Var}(X) = E[X^2] - E[X]^2 = 4$, so $\sigma = 2$. Chebyshev: $P(|X - \mu| \geq k \sigma) \leq 1/k^2$. With $k = 1.5$: $P(|X| \geq 3) \leq 1/2.25 \approx 0.44$.
</details>

**P8.** *(ML-tied)* For binary classification with logistic regression, derive the gradient of the negative log-likelihood with respect to the weights. Why is the resulting update rule so clean?

<details><summary>Answer</summary>

For one example: $L = -[y \log \sigma(w^T x) + (1-y) \log(1 - \sigma(w^T x))]$. Using $\sigma'(z) = \sigma(z)(1-\sigma(z))$, the gradient simplifies to $\nabla_w L = (\sigma(w^T x) - y) \cdot x$ — i.e., (prediction − target) × input. The clean form is why logistic regression is the canonical "first model" — the gradient is just the residual times the feature.
</details>

### Resources (only if rusty)

- *Introduction to Probability* by Blitzstein & Hwang — readable, has a free Harvard course on YouTube ("Stat 110").
- StatQuest videos for visual intuition on specific topics.

---

## 3. Optimization (light pass)

You don't need a full convex optimization course for ML. You need: the vocabulary of convexity, gradient descent and its variants intuitively, and how constraints get handled.

### Topics to refresh

| Topic | ML hook |
|---|---|
| Convex sets and convex functions | Why some problems have a unique global optimum and others don't |
| First-order conditions ($\nabla f = 0$) | Where minima live |
| Second-order conditions (Hessian PSD) | Distinguishing minima from saddle points |
| Gradient descent | The base optimizer |
| Stochastic gradient descent (SGD) | Why minibatches work |
| Momentum, Adam (intuition only) | What modern optimizers add over vanilla SGD |
| Step size / learning rate | The single most important hyperparameter |
| Lagrange multipliers, KKT conditions | Constrained optimization, SVMs |
| Backpropagation as the chain rule | How gradients flow through deep networks |

### Practice problems

**O1.** Find all critical points of $f(x, y) = x^2 + xy + y^2 - 3x$. Classify each (min, max, or saddle) using the Hessian.

<details><summary>Answer</summary>

$\nabla f = (2x + y - 3, x + 2y) = 0 \Rightarrow x = 2, y = -1$. Hessian: $\begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$, eigenvalues 1 and 3 — both positive, so PSD. The point $(2, -1)$ is a local (and global, since $f$ is convex) minimum.
</details>

**O2.** Show that $f(x) = \|Ax - b\|^2$ is convex in $x$.

<details><summary>Answer</summary>

Expand: $f(x) = x^T A^T A x - 2 b^T A x + b^T b$. Hessian: $2 A^T A$, which is always PSD ($v^T A^T A v = \|Av\|^2 \geq 0$). PSD Hessian = convex.
</details>

**O3.** Run two iterations of gradient descent by hand on $f(x) = x^2$ starting from $x_0 = 4$ with step size $\eta = 0.3$.

<details><summary>Answer</summary>

$\nabla f = 2x$. $x_1 = 4 - 0.3 \cdot 8 = 1.6$. $x_2 = 1.6 - 0.3 \cdot 3.2 = 0.64$. Geometric convergence with rate $|1 - 2\eta| = 0.4$.
</details>

**O4.** What happens to the same gradient descent if $\eta = 1.5$? Why?

<details><summary>Answer</summary>

$x_1 = 4 - 1.5 \cdot 8 = -8$. $x_2 = -8 - 1.5 \cdot (-16) = 16$. It diverges — the step is too large for the curvature. For $f(x) = x^2$, GD converges iff $\eta < 1$ (since $f''=2$, the condition is $\eta < 2/L$ where $L$ is the Lipschitz constant of the gradient). This is why learning rate matters and why second-order curvature info (Hessian, Adam's per-parameter scaling) helps.
</details>

**O5.** Set up the Lagrangian for: minimize $x^2 + y^2$ subject to $x + y = 1$. Solve it.

<details><summary>Answer</summary>

$\mathcal{L} = x^2 + y^2 - \lambda (x + y - 1)$. Stationarity: $2x = \lambda$, $2y = \lambda$, $x + y = 1$. So $x = y = 1/2$, $\lambda = 1$. Geometric meaning: the projection of the origin onto the line $x + y = 1$.
</details>

**O6.** *(ML-tied)* Why does SGD with minibatches still converge, even though each step uses a noisy gradient estimate?

<details><summary>Answer</summary>

The minibatch gradient is an **unbiased estimator** of the true gradient ($E[\nabla L_{\text{batch}}] = \nabla L_{\text{true}}$). On average, the noisy steps point in the right direction. The variance of the estimate sets the noise floor — you can't converge tighter than that without shrinking the learning rate. The noise can also help by escaping shallow local minima or saddle points.
</details>

**O7.** *(ML-tied)* In one sentence each, what does momentum add over vanilla SGD, and what does Adam add over momentum?

<details><summary>Answer</summary>

Momentum: keeps a running average of past gradients, so updates accelerate in directions of consistent descent and damp oscillation across narrow valleys. Adam: adds a per-parameter learning rate by also tracking the running average of squared gradients, so parameters with consistently large gradients get smaller steps.
</details>

### Resources (only if rusty)

- Boyd & Vandenberghe's *Convex Optimization* (free PDF) — way more than you need; use as reference.
- Sebastian Ruder's blog post *An overview of gradient descent optimization algorithms* — best single read on SGD/Momentum/Adam.

---

## After this refresher

Once these feel fluent again, you're well-positioned for:

- **Karpathy's *Zero to Hero* series** — fills the deep learning gap; assumes the math you just refreshed.
- **The production ML learning loop** in [`../learning-loop/`](../learning-loop/) — the applied side.

If a topic still feels shaky after the practice problems, that's the one to spend a real evening on, not the loop.
