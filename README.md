# SM403 — Everything you need to solve the exercises yourself

Reflex for every numerical answer: **identify the situation → pick the formula → read the right table → conclude in a sentence.**

---

## Chapter 1 — Descriptive statistics

### One variable
| Quantity | Formula | Notes |
|---|---|---|
| Mean | $\bar x=\frac1n\sum x_i$ | |
| Variance | $\sigma^2=\overline{x^2}-\bar x^2=\frac1n\sum(x_i-\bar x)^2$ | **König–Huygens** — use the $\overline{x^2}-\bar x^2$ form, it's faster |
| Std dev | $\sigma=\sqrt{\sigma^2}$ | same unit as $x$ |
| Skewness | $S_k=\frac1{\sigma^3}\cdot\frac1n\sum(x_i-\bar x)^3$ | $=0$ symmetric, $>0$ spread right |
| Kurtosis | $K=\frac1{\sigma^4}\cdot\frac1n\sum(x_i-\bar x)^4$ | $\approx3$ for normal |

**Median** (sort first): $n$ odd → value at rank $\frac{n+1}{2}$; $n$ even → average of ranks $\frac n2$ and $\frac n2+1$.
**Quartiles**: $n$ multiple of 4 → $Q_1$ = avg of ranks $\frac n4,\frac n4+1$; else $Q_1$ = rank $E(\frac n4)+1$ (same idea with $\frac{3n}{4}$ for $Q_3$).
**Mode** = most frequent value. **Range** = max − min. **Frequency** $f_i=n_i/n$.

**Linear transform** (for $Y=\alpha X+\beta$): $\overline{\alpha x+\beta}=\alpha\bar x+\beta$ and $\sigma_{\alpha x+\beta}=|\alpha|\sigma_x$ (variance $\times\alpha^2$).

### Two variables
- Covariance $\sigma_{xy}=\overline{xy}-\bar x\,\bar y$
- Correlation $\rho_{xy}=\dfrac{\sigma_{xy}}{\sigma_x\sigma_y}\in[-1,1]$ (Cauchy–Schwarz); $\pm1\Leftrightarrow$ perfect affine link
- **Regression line** $y=ax+b$: $\;a=\dfrac{\sigma_{xy}}{\sigma_x^2},\quad b=\bar y-a\bar x$ (passes through the centroid $G(\bar x,\bar y)$)
- ⚠️ Correlation ≠ causation.

**Linearization trick (Ex 6):** if the cloud is curved, substitute to make it straight. For $v=\alpha e^{\beta t}+\gamma$, set $n_i=\ln(v_i-\gamma)$ → now $n=\beta t+\ln\alpha$ is linear → fit $(t,n)$ → read $\beta=a$, $\alpha=e^{b}$.

**Weighted / combined means (Ex 4):** $\bar x=\frac{\sum n_k\bar x_k}{\sum n_k}$. Barycenter logic also gives "how many in each group." After a uniform raise on one group: mean moves predictably; **range/median** change only if the affected group holds the extreme/middle.

### p variables (matrices)
With $\bar x_j,\sigma_j$ per column:
- $M$ = raw data, $M_c=(x_{ij}-\bar x_j)$ centered, $M_s=\big(\frac{x_{ij}-\bar x_j}{\sigma_j}\big)$ centered-reduced
- **Variance–covariance** $\Sigma=\frac1n\,{}^tM_cM_c$ (variances on diagonal, covariances off)
- **Correlation** $R=\frac1n\,{}^tM_sM_s$ (1's on diagonal, $\rho$ off)
- Euclidean distance $d(x_i,x_k)=\sqrt{\sum_j(x_{ij}-x_{kj})^2}$

> **Covers Ex 1, 4, 5, 6.**

---

## Chapter 2 — Estimation by intervals

**Key distinction:** a **prediction (fluctuation) interval** uses the *known* parameters to say where future data fall (fixed). A **confidence interval** is built *from the sample* to bracket an *unknown* parameter (it moves with the sample).

### Prediction / fluctuation intervals (parameters known)
| Case | Interval | Conditions |
|---|---|---|
| Normal $\mathcal N(\mu,\sigma^2)$ | $[\mu\pm\sigma z_\alpha]$ | — |
| Empirical frequency $F$ | $\Big[p\pm\sqrt{\frac{p(1-p)}{n}}\,z_\alpha\Big]$ | $n\ge30,\ np\ge5,\ n(1-p)\ge5$ |
| Empirical mean $\bar X$ | $\Big[\mu\pm\frac{\sigma}{\sqrt n}z_\alpha\Big]$ | $n\ge30$ |

Useful: $E(\bar X)=\mu$, $\mathrm{Var}(\bar X)=\frac{\sigma^2}{n}$ → $\bar X\sim\mathcal N(\mu,\frac{\sigma^2}{n})$ for large $n$ (CLT).

### Estimators
- $\bar X$ → consistent, **unbiased** estimator of the mean.
- $F$ → consistent, **unbiased** estimator of a proportion.
- Observed variance $S^2_{obs}=\overline{X^2}-\bar X^2$ → consistent but **biased** (underestimates).
- **Corrected variance** $S^2_c=\frac{n}{n-1}S^2_{obs}$ → consistent and **unbiased**. *Use $\sigma_c$ in every CI for a mean with unknown variance.*

### Confidence intervals (parameter unknown)
| Estimate | Interval | Read from |
|---|---|---|
| Proportion | $\Big[p_0\pm\sqrt{\frac{p_0(1-p_0)}{n}}\,z_\alpha\Big]$ | Normal table |
| Mean, $\sigma$ unknown | $\Big[\bar x\pm\frac{\sigma_c}{\sqrt n}\,t_{n-1,\alpha}\Big]$ | **Student, two-sided**, $n-1$ df |
| Mean, $\sigma$ known | $\Big[\bar x\pm\frac{\sigma}{\sqrt n}\,z_\alpha\Big]$ | Normal table |

**Inverse problem (Ex 11.3):** given a target width $w$, set half-width $=\frac w2=\frac{\sigma}{\sqrt n}z$, solve for $z$, then confidence $=2\Phi(z)-1$.

**Table reading:**
- Normal $\Phi(z)$: $z_{5\%}=1.96$, $z_{1\%}=2.576$, $z_{10\%}=1.645$ (two-sided / risk in tails).
- Student: use the **two-sided (bilateral)** column for a CI; row = $n-1$ df. As $n\to\infty$ it → the normal value.

> **Covers Ex 8, 9, 10, 11.**

---

## Chapter 3 — Inferential statistics (hypothesis tests)

### The 5 steps (always write them)
1. **$H_0$ / $H_1$** ($H_0$ = "no difference / due to chance"). One-sided if "greater/lower," two-sided if "different."
2. **Distribution of the statistic under $H_0$.**
3. **Critical region** for risk $\alpha$ (an interval for two-sided, a threshold for one-sided).
4. **Compute the statistic** from the sample.
5. **Conclude**: inside → don't reject $H_0$; outside/over threshold → reject $H_0$. *A test never "proves" $H_0$.*

### Errors & quality
- $\alpha=P(\text{reject }H_0\mid H_0\text{ true})$ — false positive. Confidence $=1-\alpha$.
- $\beta=P(\text{not reject }H_0\mid H_1\text{ true})$ — false negative. **Power $=1-\beta$**.
- To get $\beta$/power: place yourself **under $H_1$** (use the $H_1$ distribution) and compute the probability of landing in the non-rejection region.

### Threshold logic (crucial)
- **Two-sided**, risk $\alpha$ → use $z_\alpha$ directly (e.g. 5% → 1.96).
- **One-sided**, risk $\alpha$ → use $z_{2\alpha}$ (e.g. 5% one-sided → the 10%-two-sided value $1.645$). For a *lower* alternative, "exceeding the threshold" means being **more negative** than $-z_{2\alpha}$.

### The tests
| Test | Statistic | Distribution | Conditions |
|---|---|---|---|
| Proportion conformity | $z=\dfrac{p_0-p}{\sqrt{p(1-p)/n}}$ | Normal | $n\ge30,\ np\ge5,\ n(1-p)\ge5$ |
| Mean, $\sigma$ unknown | $t=\dfrac{\bar x-\mu}{\sqrt{\sigma_e^2/n}}$ | Student $n-1$ | $n\ge30$ (or $X$ normal) |
| Mean, $\sigma$ known | $z=\dfrac{\bar x-\mu}{\sqrt{\sigma^2/n}}$ | Normal | same |
| $\chi^2$ conformity (fit) | $\chi^2=\sum_{i=1}^{k}\dfrac{(o_i-n_i)^2}{n_i}$ | $\chi^2$, **one-sided** | $n\ge50,\ o_i\ge5$ |
| $\chi^2$ independence | $\chi^2=\sum_{i,j}\dfrac{(o_{ij}-n_{ij})^2}{n_{ij}}$ | $\chi^2$, **one-sided** | $n\ge50,\ o_{ij}\ge5$ |

**$\chi^2$ degrees of freedom — the classic trap:**
- Fit test: $df=k-1$ … **minus 1 for every parameter you estimate from the data** (e.g. you estimate $p$ → $df=k-2$, as in Ex 19).
- Independence test: $df=(k_1-1)(k_2-1)$, expected cell $n_{ij}=\dfrac{o_{i\bullet}\,o_{\bullet j}}{n}$.
- $\chi^2$ is always one-tailed: reject only if the statistic **exceeds** the table threshold $\chi^2_{df,\alpha}$.

> **Covers Ex 13, 15, 16, 17, 18, 19, 20.**

---

## Chapter 4 — PCA

### Pipeline
1. **Standardize** the data → $M_s$ → compute $R=\frac1n\,{}^tM_sM_s$ (work on $R$, the correlation matrix).
2. **Diagonalize $R$:** characteristic polynomial $\det(R-\lambda I)=0$ → eigenvalues $\lambda_i$; eigenvectors solve $Ru=\lambda u$; **normalize** them to unit length.
   - Shortcut for a $2\times2$ correlation matrix $\begin{psmallmatrix}1&\rho\\\rho&1\end{psmallmatrix}$: eigenvalues $1+\rho$ and $1-\rho$, eigenvectors $\frac1{\sqrt2}(1,1)$ and $\frac1{\sqrt2}(-1,1)$.
3. **Change-of-basis** $P=[\,u_1\,|\,u_2\,|\dots]$ (eigenvectors as columns, largest $\lambda$ first).
4. **New coordinates** of individuals $F=M_sP$.

### Quantities to interpret
| Tool | Formula | Meaning |
|---|---|---|
| **oqe / qge** | $\dfrac{\lambda_i}{p}$ | share of information on axis $i$; $\sum\lambda_i=p$ |
| **qlt** (of individual $i$ on axis $j$) | $\dfrac{f_{ij}^2}{\sum_k f_{ik}^2}$ | how well that axis represents the individual ($=\cos^2$ of the angle); sums to 1 over axes |
| **Saturation** $S$ | $S=P\,D^{1/2}$, $D=\mathrm{diag}(\lambda_i)$ | correlations between original variables and principal axes, in $[-1,1]$ |
| Saturation identities | $\sum_i s_{ij}^2=\lambda_j$ (column), $\sum_j s_{ij}^2=1$ (row) | use to fill blanks / check |

### Reading a PCA
- **Correlation circle**: plot variables at $(s_{i,1},s_{i,2})$; only interpret variables **near the circle**. Variables clustered together define an axis; opposite ends = anti-correlated.
- **Name each axis** from the variables saturating it (e.g. "overall level," "type").
- **Select individuals** with **high qlt *and* extreme coordinate** — those are well-represented and meaningful; plot/map them.
- **Sanity checks on $R$**: it's symmetric with 1's on the diagonal — use $R_{ij}=R_{ji}$ and $R_{ii}=1$ to repair a faulty matrix (Ex 26).

> **Covers Ex 24, 26.**

---

## One-page decision flow

- "Describe / mean / correlation / regression" → **Chapter 1**.
- "In which interval will it fall / estimate a parameter with confidence" → **Chapter 2** (known params → prediction; unknown → confidence; mean unknown σ → Student + $\sigma_c$).
- "Can we say… significantly / test the hypothesis" → **Chapter 3** (proportion → $z$; mean → $t$; *distribution/several categories* → $\chi^2$ fit; *two qualitative variables* → $\chi^2$ independence). One-sided ⇒ $z_{2\alpha}$.
- "Several variables / redundancy / principal axes" → **Chapter 4**.

**Always finish with the conditions check** (the $n\ge30$, $np\ge5$, $o_i\ge5$ lines) — they're free marks and they justify the distribution you used.
