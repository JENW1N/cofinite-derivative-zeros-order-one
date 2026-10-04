# Cofinite derivative zeros at the order-one threshold

**Designated manuscript authors:** Jensen Kohlmeyer ([JENW1N](https://github.com/JENW1N)) and Liam Kruer ([lkruer](https://github.com/lkruer)).

Version 1.0.0, October 4, 2026. This repository publishes an AI-assisted mathematical proof for review.

[Read the full manuscript source](paper.tex) · [Download the compiled PDF](https://github.com/JENW1N/cofinite-derivative-zeros-order-one/releases/download/v1.0.0/cofinite_derivative_zeros_order_one.pdf)

## Exact problem and result

The catalogue entry is [JSP-000752](https://github.com/TheJustinSunPrize/awards/blob/main/problems/catalog-0701-0800.md#JSP-000752). Its original source is [Erdős Problem 906](https://www.erdosproblems.com/906), concerning zeros of derivatives of entire functions. The catalogue number is not the Erdős problem number.

Theorem 2 proves that there is a transcendental entire function $f$ such that

$$
\forall U\subset\mathbb C\text{ nonempty and open},\quad
\exists N_U\quad\forall n\ge N_U,\quad
\exists z\in U:\ f^{(n)}(z)=0.
$$

Lemma 1 proves that this statement is equivalent to the union of derivative zero sets being dense along **every** strictly increasing infinite sequence of derivative orders. The argument covers the full original problem.

The construction also satisfies

$$
\log M_f(r)=O(r\log r\log\log r).
$$

Proposition 3 rules out finite exponential type for any transcendental entire function with the required zero property. Consequently, order one is the smallest possible order and is attained here, with infinite exponential type. Theorem 10 gives the locally weak limit of the derivative zero-counting measures, including multiplicities:

$$
\frac{\nu_n}{W_n}\longrightarrow\frac{1}{2\pi|z|}\,dA(z),
\qquad W_n=\log(n+e^e)\log\log(n+e^e).
$$

The density is locally integrable and has no atom at zero. The construction uses independent uniform-disk coefficients, an inverse-amplitude moment, the harmonic mean identity on zero-free disks, and the first Borel-Cantelli lemma. No independence between derivative orders is assumed.

## Prior work and attribution

The original existence assertion already has prior solution claims, including Eric Hou's [*Cofinite Zeros of High Derivatives*, arXiv:2607.20816v3](https://arxiv.org/html/2607.20816v3) and [source repository](https://github.com/erichou1/cofinite-derivative-zeros). Hou's bounded random-series and zero-free-disk argument is a precedent for the framework used here; his stated construction has order two. Earlier probabilistic proposals appear in the [Problem 906 discussion](https://www.erdosproblems.com/forum/thread/906?embed=1).

This manuscript does **not** claim first discovery of the existence assertion or priority over those contributions. The proposed additional contributions are the order-one construction, the finite-exponential-type obstruction, and the limiting zero density. Their novelty remains subject to literature review. References acknowledge the prior sources; no third-party proof files are copied into this repository.

Jensen Kohlmeyer and Liam Kruer are the designated authors requested for this research manuscript. OpenAI Codex substantially assisted with the mathematical construction, proof development, coefficient checks, literature comparison, and manuscript preparation. The repository and submission are published from the JENW1N account. No independent human verification or distinct individual author roles are asserted. Authorship, contribution attribution, mathematical correctness, and novelty are submitted for review.

## Reading and checking the proof

The proof is self-contained in [paper.tex](paper.tex), especially Sections 2-5 for the complete original result. Section 6 proves the additional zero-density theorem; Section 7 discusses general weights. The argument does not rely on numerical computations or an unproved conjecture.

The source compiled successfully with the Codex built-in LaTeX compiler before publication. The release PDF is generated from the public source at a fixed full commit SHA using [LaTeX.Online](https://github.com/aslushnikov/latex-online#api). The accompanying build record identifies the source commit and source/PDF SHA-256 hashes. [build_pdf.py](build_pdf.py) reproduces this export without uploading local files or using credentials. LaTeX compilation checks typesetting, not mathematical correctness.

The accompanying Python script supplies finite high-precision sanity checks, not a proof, interval certification, or Lean formalization. To reproduce:

```sh
python3 -m pip install -r requirements.txt
python3 check_order_one_estimates.py --json order_one_estimate_checks.json
```

The committed report records 56 cases at 90 decimal digits: 32 coefficient-peak checks and 47 derivative-majorant checks where the sufficient cutoff holds, all passing. The infinite inequalities are proved analytically in the manuscript.

For a local PDF build with a TeX distribution:

```sh
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
```

No Lean proof is claimed. The [prize rules](https://github.com/TheJustinSunPrize/awards/blob/main/docs/award-process.md#mathematical-solution-only) allow a complete mathematical submission before Lean formalization. Prize acceptance, formal verification, award eligibility, and recipient confirmation are separate review steps.
