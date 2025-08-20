## Test case: function expression without arguments to python lambda
JavaScript:
```js
const hello = function () {
  return console.log("Hello world");
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
