#!/usr/bin/env python3
from __future__ import annotations

import argparse
import random
import time
from dataclasses import dataclass
from typing import List, Optional


def is_sorted_nondecreasing(a: List[int]) -> bool:
    return all(a[i] <= a[i + 1] for i in range(len(a) - 1))


@dataclass
class RunStats:
    flips: int
    checks: int
    sorted_found: bool
    wall_seconds: float
    simulated_seconds: float
    flips_per_second_wall: float


class BitArray:
    def __init__(self, values: List[int], w: int) -> None:
        if w <= 0:
            raise ValueError("w must be > 0")
        if not values:
            raise ValueError("array length must be > 0")
        self.w = w
        self.mask = (1 << w) - 1
        self.values = [v & self.mask for v in values]

    @property
    def n(self) -> int:
        return len(self.values)

    @property
    def total_bits(self) -> int:
        return self.n * self.w

    def flip_bit_by_index(self, bit_index: int) -> None:
        word = bit_index // self.w
        bit = bit_index % self.w
        self.values[word] = (self.values[word] ^ (1 << bit)) & self.mask

    def flip_random_bit(self, rng: random.Random) -> None:
        self.flip_bit_by_index(rng.randrange(self.total_bits))

    def is_sorted(self) -> bool:
        return is_sorted_nondecreasing(self.values)


class CosmicRaySorter:
    def __init__(
        self,
        bit_array: BitArray,
        flip_rate: float,
        check_every: int,
        max_wall_seconds: float,
        seed: Optional[int] = None,
        real_time: bool = False,
        show_progress: bool = False,
        progress_every: int = 200_000,
    ) -> None:
        if flip_rate <= 0:
            raise ValueError("flip_rate must be > 0")
        if check_every <= 0:
            raise ValueError("check_every must be > 0")
        if max_wall_seconds <= 0:
            raise ValueError("max_wall_seconds must be > 0")

        self.arr = bit_array
        self.flip_rate = flip_rate
        self.check_every = check_every
        self.max_wall_seconds = max_wall_seconds
        self.rng = random.Random(seed)
        self.real_time = real_time
        self.show_progress = show_progress
        self.progress_every = max(1, progress_every)

    @staticmethod
    def _fps(flips: int, wall: float) -> float:
        wall = max(wall, 1e-12)
        return flips / wall

    def run(self) -> RunStats:
        start = time.perf_counter()
        deadline = start + self.max_wall_seconds
        flips = 0
        checks = 0

        # Always count the initial check for consistent stats.
        checks += 1
        if self.arr.is_sorted():
            wall = time.perf_counter() - start
            return RunStats(
                flips=0,
                checks=checks,
                sorted_found=True,
                wall_seconds=wall,
                simulated_seconds=0.0 if not self.real_time else wall,
                flips_per_second_wall=0.0,
            )

        while True:
            now = time.perf_counter()
            if now >= deadline:
                wall = now - start
                simulated = wall if self.real_time else flips / self.flip_rate
                return RunStats(
                    flips=flips,
                    checks=checks,
                    sorted_found=False,
                    wall_seconds=wall,
                    simulated_seconds=simulated,
                    flips_per_second_wall=self._fps(flips, wall),
                )

            if self.real_time:
                # Poisson arrivals: inter-flip waiting time ~ Exp(flip_rate)
                dt = self.rng.expovariate(self.flip_rate)
                remaining = max(0.0, deadline - now)
                time.sleep(min(dt, remaining))

            # In fast mode we do not sleep; flip_rate only affects "simulated time" reporting.
            self.arr.flip_random_bit(self.rng)
            flips += 1

            if flips % self.check_every == 0:
                checks += 1
                if self.arr.is_sorted():
                    wall = time.perf_counter() - start
                    simulated = wall if self.real_time else flips / self.flip_rate
                    return RunStats(
                        flips=flips,
                        checks=checks,
                        sorted_found=True,
                        wall_seconds=wall,
                        simulated_seconds=simulated,
                        flips_per_second_wall=self._fps(flips, wall),
                    )

            if self.show_progress and flips % self.progress_every == 0:
                wall = time.perf_counter() - start
                sim = wall if self.real_time else flips / self.flip_rate
                extra = f" sim={sim:.6f}s" if not self.real_time else ""
                print(
                    f"[progress] flips={flips} checks={checks} "
                    f"wall={wall:.6f}s{extra} fps={self._fps(flips, wall):.0f}"
                )


def make_initial_array(n: int, w: int, seed: Optional[int], max_value: Optional[int]) -> List[int]:
    if n <= 0:
        raise ValueError("n must be > 0")
    if w <= 0:
        raise ValueError("w must be > 0")
    rng = random.Random(seed)
    upper = (1 << w) - 1
    if max_value is not None:
        if max_value < 0:
            raise ValueError("max_value must be >= 0")
        upper = min(upper, max_value)
    return [rng.randrange(upper + 1) for _ in range(n)]


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Cosmic Ray Sort (simulator)")
    p.add_argument("--n", type=int, default=5)
    p.add_argument("--w", type=int, default=8)
    p.add_argument(
        "--flip-rate",
        type=float,
        default=2000.0,
        help="Flips/sec. In fast mode this sets the simulated-time scale; in --real-time flips arrive as a Poisson process with this rate.",
    )
    p.add_argument("--check-every", type=int, default=10)
    p.add_argument("--max-seconds", type=float, default=3.0)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--max-value", type=int, default=None)
    p.add_argument("--real-time", action="store_true")
    p.add_argument("--show-progress", action="store_true")
    p.add_argument("--progress-every", type=int, default=200_000)
    return p


def main() -> None:
    args = build_parser().parse_args()

    init = make_initial_array(
        args.n, args.w, seed=args.seed, max_value=args.max_value)
    arr = BitArray(init, w=args.w)

    mode = "real-time" if args.real_time else "fast-sim"
    print(f"Initial array: {arr.values}")
    print(
        f"Params: n={args.n}, w={args.w}, flip_rate={args.flip_rate}/s, "
        f"check_every={args.check_every}, max_seconds={args.max_seconds}, seed={args.seed}, mode={mode}"
    )

    sorter = CosmicRaySorter(
        bit_array=arr,
        flip_rate=args.flip_rate,
        check_every=args.check_every,
        max_wall_seconds=args.max_seconds,
        seed=args.seed,
        real_time=args.real_time,
        show_progress=args.show_progress,
        progress_every=args.progress_every,
    )

    stats = sorter.run()

    if stats.sorted_found:
        print(f"Sorted detected: {arr.values}")
    else:
        print("No sorted state observed within wall-clock limit.")
        print(f"Current array:  {arr.values}")

    if args.real_time:
        print(
            f"Flips: {stats.flips}, Checks: {stats.checks}, "
            f"Wall: {stats.wall_seconds:.6f}s ({stats.flips_per_second_wall:.0f} flips/s)"
        )
    else:
        print(
            f"Flips: {stats.flips}, Checks: {stats.checks}, "
            f"Wall: {stats.wall_seconds:.6f}s ({stats.flips_per_second_wall:.0f} flips/s), "
            f"Simulated: {stats.simulated_seconds:.6f}s"
        )


if __name__ == "__main__":
    main()
