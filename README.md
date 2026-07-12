# a11y-flow-recorder

A dependency-free CLI that validates recorded interaction flows for basic accessibility failures and generates Playwright test code.

## Quick start

```bash
python a11y_flow.py flow.json --test-out recorded.spec.ts
```

A flow contains ordered steps with an action and element metadata. The audit checks accessible names on interactive elements, keyboard reachability, and positive-tabindex focus regressions. It emits JSON and exits nonzero on violations.

## Test

```bash
python -m unittest discover -v
```

## License

MIT.
