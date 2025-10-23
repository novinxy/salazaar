## Test case: anonymous function to python lambda
JavaScript:
```js
const squares = numbers.map(function(x, y) { x + y });
```

Python:
```py
squares = numbers.map(lambda x, y: x + y)
```

## Test case: long anonymous function to python local function
JavaScript:
```js
const squares = numbers.map(function(x, y) {
    const tmp = x + y
    return tmp
});
```

Python:
```py

def local_anonymous_func(x, y):
    tmp = x + y
    return tmp
squares = numbers.map(local_anonymous_func)
```