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

## Test case: multi line function expression in function call to global function
JavaScript:
```js
const result = collection.map(function calc(a) {
  a += 5;
  return a * a;
});
```

Python:
```py
def calc(a):
    a += 5
    return a * a
result = collection.map(calc)
```

## Test case: multi line function expression in function call to local function
JavaScript:
```js
function test() {
  let c = 10;

  const result = collection.map(function calc(a, b) {
    a += 5;
    return a * b + c;
  });
}
```

Python:
```py
def test():
    c = 10

    def calc(a, b):
        a += 5
        return a * b + c
    result = collection.map(calc)
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
