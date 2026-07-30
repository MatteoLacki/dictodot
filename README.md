# dictodot

A short description of the project.

## NumPy helpers

Install the optional NumPy support to use `dd_zeros`, `dd_empty`, and
`dd_full`:

```sh
pip install "dictodot[numpy]"
```

The base package and `DotDict` do not require NumPy. The NumPy dependency is
loaded only when one of the NumPy-backed allocation helpers is called.
