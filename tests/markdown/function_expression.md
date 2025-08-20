## Test case: function expression without arguments to python lambda
JavaScript:
```js
const hello = function () {
  console.log("Hello world");
};
```

Python:
```py
hello = lambda: console.log('Hello world')
```


## Test case: function expression to python lambda
JavaScript:
```js
const multiply = function mul(a, b) {
  return a * b;
};
```

Python:
```py
multiply = lambda a, b: a * b
```

## Test case: function expression in one line to python lambda
JavaScript:
```js
const multiply = function mul(a, b) { return a * b; };
```

Python:
```py
multiply = lambda a, b: a * b
```

## Test case: function expression in function call
JavaScript:
```js
const result = collection.map(function power(a) { return a * a; });
```

Python:
```py
result = collection.map(lambda a: a * a)
```

## Test case: function expression multi line to python lambda
JavaScript:
```js
const multiply = function (a, b)
{
  a++
  return a * b;
};
```

Python:
```py
def multiply(a, b):
    a += 1
    return a * b
```
