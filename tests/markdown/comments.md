## Test case: leading comment
JavaScript:
```js
// simple comment
let value = "hello"
```

Python:
```py
# simple comment
value = 'hello'
```

## Test case: multiple comments
JavaScript:
```js
// simple comment
// second comment
let value = "hello"
```

Python:
```py
# simple comment
# second comment
value = 'hello'
```

## Test case: multiline comments
JavaScript:
```js
/* 1 line
2 line
3 line */
let value = "hello"
```

Python:
```py
# 1 line
# 2 line
# 3 line
value = 'hello'
```

## Test case: mixed comments
JavaScript:
```js
// simple comment
/* 1 line
2 line
3 line */
let value = "hello"
```

Python:
```py
# simple comment
# 1 line
# 2 line
# 3 line
value = 'hello'
```

## Test case: more complicated code with comments
JavaScript:
```js
// simple comment
let value = "hello"

/* function hello
returns "hello" */
function hello() {

    // inner comment
    return "Hello"
}
```

Python:
```py
# simple comment
value = 'hello'
# function hello
# returns "hello"

def hello():
# inner comment
    return 'Hello'
```