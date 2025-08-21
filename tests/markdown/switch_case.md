# JS `switch` to Python `match` Conversion Tests

This file contains examples and tests for converting JavaScript `switch` statements to Python 3.10+ `match` statements.

---

## Test case: Simple Value Matching

JavaScript:
```js
switch (value) {
    case 1:
        result = "one";
        break;
    case 2:
        result = "two";
        break;
    default:
        result = "other";
}
```

Python:
```py
match value:
    case 1:
        result = 'one'
    case 2:
        result = 'two'
    case _:
        result = 'other'
```


## Test case: Multiple Cases - Fallthrough

JavaScript:
```js
switch (color) {
    case "red":
    case "blue":
        result = "primary";
        break;
    case "green":
        result = "secondary";
        break;
    default:
        result = "unknown";
}
```

Python:
```py
match color:
    case 'red' | 'blue':
        result = 'primary'
    case 'green':
        result = 'secondary'
    case _:
        result = 'unknown'
```


## Test case: Switch with Expressions

JavaScript:
```js
switch (x + y) {
    case 10:
        result = "ten";
        break;
    default:
        result = "not ten";
}
```

Python:
```py
match x + y:
    case 10:
        result = 'ten'
    case _:
        result = 'not ten'
```


## Test case: No Default Case

JavaScript:
```js
switch (status) {
    case "ok":
        result = true;
        break;
    case "fail":
        result = false;
        break;
}
```

Python:
```py
match status:
    case 'ok':
        result = True
    case 'fail':
        result = False
```


## Test case: Nested Switch

JavaScript:
```js
switch (type) {
    case "A":
        switch (subtype) {
            case 1:
                result = "A1";
                break;
            default:
                result = "A-other";
        }
        break;
    default:
        result = "other";
}
```

Python:
```py
match type:
    case 'A':
        match subtype:
            case 1:
                result = 'A1'
            case _:
                result = 'A-other'
    case _:
            result = 'other'
```