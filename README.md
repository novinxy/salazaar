# salazaar

> **Make your codebase speak snake'ish! 🐍**

**salazaar** is a library that transpiles JavaScript code into syntax-correct Python code.

Main goal is to help you migrate legacy, untyped JS projects into the modern Python ecosystem as smoothly as possible.

---

## Features

- Converts JavaScript code to Python code
- Focuses on generating code that's ready to execute (with some manual tweaks)
- Eases the transition from JS to Python for large codebases

---

## Usage

There are 2 options to use salazaar:
- as library
    ```py
        import salazaar
        js_code = "let result = true ? 1: 0"

        # unsafe_fixes & comments are optional arguments
        py_code = salazaar.translate(js_code, unsafe_fixed=True, comments=False)

        assert "result = 1 if True else 0"
    ```
- in command line
    ```bash
    > "let result = 1" | python -m salazaar
    result = 1 if True else 0
    ```


## How it works
salazaar works by converting JavaScript AST to valid Python AST.

It uses [esprima-python](https://github.com/Kronuz/esprima-python) as JavaScript AST reader.

What salazaar implements are rules for converting AST, many of which are opinionated. Those languages differ and many features needs to be replaces with something "sensible" in Python language.

Except for syntax salazaar also allows for functions/methods conversion. To check which functions are translated please [unsafe_fixes](#unsafe_fixes) Unfortunately library doesn't infer JS types so those conversions are based on names and syntax. That's why those are categorized as "unsafe_fixes". It's best to be carefull with them and check how they perform for given code base.



## unsafe_fixes
Here is currently implemented list of JavaScript functions converted
- .toString
- Array.join
- Array.push
- Array.slice
- Array.sort
- JSON.parse
- JSON.stringify
- regex literals
- string.concat
- string.match
- string.matchAll
- string.replace
- string.split
- string.substr
- string.substring
- string.test
- string.toLowerCase
- string.toUpperCase
- string.trim

## Limitations

- **Not a Silver Bullet:** The tool is designed to simplify, not fully automate, the migration process.
- **Type Inference:** No automatic JS type inference; some function calls may not convert directly.
- **Built-in Libraries:** Many JS built-ins are not translated and may need custom handling.
- **Variable Scoping:** Differences in global/non-local variables and `var` behavior may require manual adjustments.



## Documentation

- Example translations and requirements are documented in the [`tests/markdown`](./tests/markdown) directory.
- These markdown files serve as both documentation and a specification for running test suite



## Contributing

If you are interested in this project feel free  to contribute! Please open issues for bugs or feature requests, and submit pull requests to help improve salazaar.



## License

MIT License. See [LICENSE](./LICENSE) for details.
