## Test case: simple function
JavaScript:
```js
function Test() {
    var tmp = 10;
}
```

Python:
```py
def Test():
    tmp = 10
```

## Test case: function with argument
JavaScript:
```js
function Test(arg1) {
    var tmp = 10;
}
```

Python:
```py
def Test(arg1):
    tmp = 10
```

## Test case: function with multiple arguments
JavaScript:
```js
function Test(arg1, arg2, arg3) {
    var tmp = 10;
}
```

Python:
```py
def Test(arg1, arg2, arg3):
    tmp = 10
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
multiple = lambda a, b: a * b
```

## Test case: array function to python lambda
JavaScript:
```js
const squares = numbers.map(num => num * num);
```

Python:
```py
squares = numbers.map(lambda num: num * num)
```
