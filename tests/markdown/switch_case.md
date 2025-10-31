# JS `switch` to Python `match` Conversion Tests

This file contains examples and tests for converting JavaScript `switch` statements to Python 3.10+ `match` statements.

---

## Test case: simple value matching

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


## Test case: multiple cases - fallthrough

JavaScript:
```js
switch (color) {
    case "red":
    case "blue":
        flag = true
    case "yellow":
        result = "primary";
    case "green":
        sayHello();
        break;
    case "black":
        flag = false
    case "white":
        sayHello();
        break;
    default:
        result = "unknown";
}
```

Python:
```py
match color:
    case 'red':
        flag = True
        result = 'Primary'
        sayHello()
    case 'blue':
        flag = True
        result = 'Primary'
        sayHello()
    case 'yellow':
        result = 'Primary'
        sayHello()
    case 'green':
        sayHello()
    case 'black':
        flag = False
        sayHello()
    case 'white':
        sayHello()
    case _:
        result = 'unknown'
```


## Test case: switch with expressions

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


## Test case: no default case

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


## Test case: nested switch

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