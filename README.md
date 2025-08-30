# salazaar

> **Make your codebase speak snake'ish! 🐍**

**salazaar** is a library that transpiles JavaScript code into syntax-correct Python code. Its main goal is to help you migrate legacy, untyped JS projects into the modern Python ecosystem as smoothly as possible.

---

## Features

- Converts JavaScript code to Python syntax
- Focuses on generating code that's ready to execute (with some manual tweaks)
- Eases the transition from JS to Python for large codebases

---

## How it works
salazaar works by converting JavaScript AST to valid Python AST.

It uses [esprima-python](https://github.com/Kronuz/esprima-python) as JavaScript AST reader.

What salazaar implements are rules for converting AST, many of which are opinionated. Those languages differ and many features needs to be replaces with something "sensible" in other language.

---

## Limitations

- **Variable Scoping:** Differences in global/non-local variables and `var` behavior may require manual adjustments.
- **Built-in Libraries:** Many JS built-ins are not translated and may need custom handling.
- **Type Inference:** No automatic JS type inference; some function calls may not convert directly.
- **Not a Silver Bullet:** The tool is designed to simplify, not fully automate, the migration process.

---

## Documentation

- Example translations and requirements are documented in the [`tests/markdown`](./tests/markdown) directory.
- These markdown files serve as both documentation and a specification for running test suite

---

## Contributing

If you are interested in this project feel free  to contribute! Please open issues for bugs or feature requests, and submit pull requests to help improve salazaar.

---

## License

MIT License. See [LICENSE](./LICENSE) for details.
