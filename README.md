# Cosmic Ray Sort ☢️

_This repository is a joke / thought experiment made executable via simulation._

![status](https://img.shields.io/badge/status-experimentally%20useless-brightgreen)
![correctness](https://img.shields.io/badge/correctness-almost%20sure-blue)
![runtime](https://img.shields.io/badge/expected%20runtime-cosmological-red)

> The worst sorting algorithm ever: do nothing and wait until random bit flips in memory (e.g. from cosmic rays) accidentally transform your array into sorted order.

## Abstract

Cosmic Ray Sort is a deliberately impractical sorting algorithm that delegates all state transitions to uncontrolled physical noise in the memory substrate. Instead of actively reordering elements, the algorithm passively waits for spontaneous bit flips induced by environmental perturbations (e.g., thermal noise, radiation, and other stochastic influences) to transform an initially unsorted array into a sorted configuration.

Under a simple physical model of stochastic bit flips, the algorithm is formally correct and terminates almost surely (conditioned on nonzero flip rates and a finite state space). However, its expected runtime grows rapidly with input size and exceeds any practical timescale for nontrivial arrays. This project serves as a conceptual and educational exploration of the relationship between computation, thermodynamics, and physical noise.

## Motivation

Sorting algorithms traditionally impose order by actively manipulating data, reducing entropy through deliberate computation. Cosmic Ray Sort explores the opposite extreme: **can order be obtained by passively waiting for entropy-driven fluctuations to produce it spontaneously?**

This repository treats physical noise not as a failure mode to be mitigated, but as the sole computational primitive. While computationally meaningless in practice, the model provides a concrete thought experiment illustrating how deeply computation is embedded in physical reality and constrained by thermodynamics.

## Algorithm

Given an array $A = (a_1, \ldots, a_n)$:

1. Store $A$ in memory.
2. Allow the memory to evolve under environmental perturbations that induce random bit flips.
3. Periodically check whether $A$ is sorted (nondecreasing).
4. Halt when a sorted configuration is observed.

The algorithm performs no write operations on the array; all state changes are delegated to physical noise.

## Physical Model

Each bit is modeled as a bistable physical system with two metastable states separated by an energy barrier $\Delta E$. Environmental coupling induces rare stochastic transitions between states. Under weak coupling to a thermal bath, the global memory configuration evolves as a continuous-time Markov process over a finite state space of size $2^B$, where $B = n \cdot w$ is the total number of bits.

At a fundamental level, physical dynamics may be unitary and deterministic. However, for any realistic subsystem the effective dynamics are stochastic due to chaotic many-body interactions, entanglement with unobserved degrees of freedom, decoherence, and coarse-graining. For computational purposes, bit flips are therefore modeled as random events.

In practice, hardware memory is engineered to _suppress_ precisely these transitions, making Cosmic Ray Sort adversarial to modern computer architecture.

## Correctness

Assume that:

- each bit has a nonzero probability of flipping over time,
- the system is not driven into absorbing failure states,
- the memory state space is finite,
- the checker used to test sortedness is reliable (or protected by error correction), and
- no irreversible hardware faults permanently remove reachable states.

With positive flip rates, the induced continuous-time Markov chain over memory states is irreducible and aperiodic, hence ergodic. Consequently, every reachable configuration is visited infinitely often with probability 1, including those corresponding to sorted arrays.

**Cosmic Ray Sort is therefore correct in the limit of infinite time and terminates almost surely.**  
When the algorithm halts, the observed array is guaranteed to be sorted.

## Expected Runtime

Let each array element be represented by $w$ bits, so that values lie in $\{0, \ldots, m-1\}$ with $m = 2^w$. The number of nondecreasing (“sorted”) arrays of length $n$ is:

$$
\binom{m + n - 1}{n}.
$$

In the symmetric independent bit-flip model, the stationary distribution over all $m^n$ arrays is uniform. The stationary probability that the array is sorted is therefore:

$$
p_{\text{sorted}} = \frac{\binom{m + n - 1}{n}}{m^n}.
$$

A common (but physically very optimistic) back-of-the-envelope estimate is to assume the memory “effectively resamples” an independent uniform configuration at some rate $R$ states/second. Under that i.i.d. resampling idealization:

$$
\mathbb{E}[T] \approx \frac{1}{R\,p_{\text{sorted}}}.
$$

### Back-of-the-Envelope Numbers (i.i.d. resampling idealization)

Take $w=8$ ($m=256$) and $R = 10^9$ independent configurations/second (already absurdly generous).

- **$n=10$**:

  $$
  p_{\text{sorted}}=\frac{\binom{256+10-1}{10}}{256^{10}}
  =\frac{\binom{265}{10}}{256^{10}}
  \approx 3.28\times 10^{-7}.
  $$

  So $\mathbb{E}[T] \approx \frac{1}{10^9\cdot 3.28\times 10^{-7}} \approx 3\times 10^{-3}$ s (milliseconds).

- **$n=20$**:

  $$
  p_{\text{sorted}}=\frac{\binom{275}{20}}{256^{20}}
  \approx 8.48\times 10^{-19},
  $$

  so $\mathbb{E}[T]\approx 1.2\times 10^9$ s (about **38 years**).

- **$n=30$**:
  $$
  p_{\text{sorted}}=\frac{\binom{285}{30}}{256^{30}}
  \approx 1.94\times 10^{-32},
  $$
  so $\mathbb{E}[T]\approx 1.6\times 10^{15}$ years (far longer than the age of the universe).

### Why the Real Runtime Is Worse

The i.i.d. resampling model is not how bit flips work: real dynamics change _local bits_ and produce highly correlated states. The time to “mix” across the full $2^{nw}$ state space can dominate the hitting time, making the practical waiting time far larger than $\frac{1}{p_{\text{sorted}}}$ suggests. In other words, even when $p_{\text{sorted}}$ is not astronomically tiny, _actually reaching_ something close to the uniform distribution can be the bottleneck.

Checking too frequently yields highly correlated observations; checking too infrequently risks missing short-lived sorted states. Neither choice improves the fundamental scaling.

## Thermodynamic Interpretation

From a statistical-mechanical perspective, the sorted configuration corresponds to a highly constrained macrostate occupying a vanishingly small fraction of the total configuration space. Cosmic Ray Sort relies on rare fluctuations to drive the system into this low-measure macrostate.

Whereas conventional algorithms actively reduce entropy, Cosmic Ray Sort passively waits for entropy-driven fluctuations to transiently produce order. The sorted state is not thermodynamically stable and will typically be destroyed by subsequent noise unless the computation halts immediately upon detection.

### Relation to the Boltzmann Brain Problem

Cosmic Ray Sort is computationally analogous to the Boltzmann brain paradox: both rely on rare thermal or stochastic fluctuations to produce highly structured, low-entropy states from equilibrium noise. In both cases, the event is possible in principle, but dominated in practice by timescales so large that their physical relevance is questionable.

## Simulation Model

This repository provides a simulation that injects random bit flips at a configurable rate.

## Quickstart

```bash
git clone https://github.com/archudzik/CosmicRaySort.git
cd CosmicRaySort
python cosmic_ray_sort.py --n 5 --w 8 --flip-rate 1000 --check-every 100
```

## Conclusion

Cosmic Ray Sort is a formally correct but computationally degenerate sorting algorithm. It exists to illustrate the distinction between theoretical possibility and practical computability, and to emphasize that computation is ultimately constrained by the physical properties of the substrate on which it is implemented.

## License

MIT License.
