# Cosmic Ray Sort ☢️

_This repository is a joke / thought experiment made executable via simulation._

![status](https://img.shields.io/badge/status-experimentally%20useless-brightgreen)
![correctness](https://img.shields.io/badge/correctness-almost%20sure-blue)
![runtime](https://img.shields.io/badge/expected%20runtime-cosmological-red)

> The worst sorting algorithm ever: do nothing and wait until random bit flips in memory (e.g. from cosmic rays) accidentally transform your array into sorted order.

## Abstract

Cosmic Ray Sort is a deliberately impractical sorting algorithm that delegates all state transitions to uncontrolled physical noise in the memory substrate. Instead of actively reordering elements, the algorithm passively waits for spontaneous bit flips induced by environmental perturbations (e.g., thermal noise, radiation, and other stochastic influences) to transform an initially unsorted array into a sorted configuration.

Under a simple physical model of stochastic bit flips, the algorithm is formally correct and terminates almost surely (conditioned on nonzero flip rates and a finite state space). However, its expected runtime grows astronomically with input size and exceeds any practical timescale for nontrivial arrays. This project serves as a conceptual and educational exploration of the relationship between computation, thermodynamics, and physical noise.

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

The expected waiting time scales like $1 / p_{\text{sorted}}$, up to factors determined by temporal correlations and the mixing time of the underlying Markov process. This quantity grows rapidly with $n$, rendering the expected runtime astronomically large for all but trivial input sizes.

Checking too frequently yields highly correlated observations; checking too infrequently risks missing short-lived sorted states. Neither choice improves the fundamental scaling.

### Back-of-the-Envelope Timescale

To illustrate the absurdity of the expected runtime, consider a toy example:

- $n = 10$ elements
- $w = 8$ bits per element (so $m = 256$)

The fraction of sorted arrays is:

$$
p_{\text{sorted}} = \frac{\binom{256 + 10 - 1}{10}}{256^{10}} \approx \frac{\binom{265}{10}}{256^{10}}.
$$

This is on the order of:

$$
p_{\text{sorted}} \sim 10^{-14}.
$$

Even if the memory were to decorrelate completely and effectively resample its entire state at a rate of $10^9$ independent configurations per second, the expected waiting time would be on the order of:

$$
\mathbb{E}[T] \sim 10^5 \text{ seconds} \approx \text{days}.
$$

For $n = 20$, the expected waiting time already exceeds geological timescales. For realistic array sizes, the expected time to observe a sorted configuration vastly exceeds cosmological timescales, proton decay bounds, and any meaningful notion of “runtime” in physics.

In other words, Cosmic Ray Sort is not merely impractical—it is _physically satirical_.

## Thermodynamic Interpretation

From a statistical-mechanical perspective, the sorted configuration corresponds to a highly constrained macrostate occupying a vanishingly small fraction of the total configuration space. Cosmic Ray Sort relies on rare fluctuations to drive the system into this low-measure macrostate.

Whereas conventional algorithms actively reduce entropy, Cosmic Ray Sort passively waits for entropy-driven fluctuations to transiently produce order. The sorted state is not thermodynamically stable and will typically be destroyed by subsequent noise unless the computation halts immediately upon detection.

### Relation to the Boltzmann Brain Problem

Cosmic Ray Sort is computationally analogous to the Boltzmann brain paradox: both rely on rare thermal or stochastic fluctuations to produce highly structured, low-entropy states from equilibrium noise. In both cases, the event is possible in principle, but dominated in practice by timescales so large that their physical relevance is questionable.

Cosmic Ray Sort can therefore be interpreted as a sorting algorithm that is correct in the same sense that Boltzmann brains are observers.

## Simulation Model

This repository provides a simulation that injects random bit flips at a configurable rate.

**Default model:**

- Each flip selects a uniformly random bit among all \( B = n \cdot w \) bits and flips it (in real-time mode, flips arrive as a Poisson process).
- Every \( T \) flips, the array is checked for nondecreasing order.
- Parameters control array length, bit width, flip rate (flips per second in simulated time), check interval, and random seed.

The simulation is intended to illustrate qualitative behavior and does not claim physical realism.

## Quickstart

```bash
git clone https://github.com/archudzik/CosmicRaySort.git
cd CosmicRaySort
python cosmic_ray_sort.py --n 5 --w 8 --flip-rate 1000 --check-every 100
```

Example output:

```text
Initial array: [172, 233, 119, 173, 187]
Params: n=5, w=8, flip_rate=1000.0/s, check_every=100, max_seconds=3.0, seed=None, mode=fast-sim
Sorted detected: [32, 65, 91, 151, 158]
Flips: 8400, Checks: 85, Wall: 0.002987s (2812375 flips/s), Simulated: 8.400000s
```

## Limitations

- The expected runtime is prohibitive for nontrivial input sizes.
- The sorted configuration is unstable under continued noise.
- Real hardware employs error correction and shielding that suppress the very effects this algorithm relies on.
- The checker and control logic must themselves be protected from noise for correctness to be meaningful.
- Local bit flips mix the global state space extremely slowly for large \( B \).

These limitations are intrinsic to the approach.

## Related Work

- Bogosort
- Miracle Sort
- Infinite monkey theorems
- Randomized and Monte Carlo algorithms
- Physical models of computation and thermodynamic limits

## Comparison to Bogosort

| Property          | Bogosort                     | Cosmic Ray Sort               |
| ----------------- | ---------------------------- | ----------------------------- |
| Writes to memory  | Yes (active shuffling)       | No (passive observation only) |
| Source of entropy | Algorithmic randomness       | Physical noise                |
| Correctness       | Eventual hit of sorted state | Eventual hit of sorted state  |
| Expected runtime  | Catastrophic                 | Cosmological                  |
| Practical use     | None                         | Even less                     |

## Conclusion

Cosmic Ray Sort is a formally correct but computationally degenerate sorting algorithm. It exists to illustrate the distinction between theoretical possibility and practical computability, and to emphasize that computation is ultimately constrained by the physical properties of the substrate on which it is implemented.

## License

MIT License.
