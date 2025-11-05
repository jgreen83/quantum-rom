# quantum-rom
2 Potential implementations in Qiskit for a Quantum ROM system: takes a boolean function $f: \mathbb{F}_2^n \to \mathbb{F}_2^d$ and outputs a circuit, $U$, such that $U |x\rangle_n |0 \rangle_d = |x \rangle_n |f(x) \rangle_d.$

# File Directory
- [`qrom-different-implementations.ipynb`](./qrom-different-implementations.ipynb) - step-by-step implementation and verification of both implementations, with some examples for small n: good for exploring the two methods
- [`demos.ipynb`](./demos.ipynb) - demos for each implementation for n = 3
- [`select.py`](./select.py) - cleaned-up, packaged select implementation
- [`selectswap.py`](./selectswap.py) - cleaned-up, packaged select-swap implementation


