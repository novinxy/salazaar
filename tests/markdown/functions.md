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

## Test case: function with multiple lines
JavaScript:
```js
function Test() {
    var tmp = 10;
    tmp += 1
}
```

Python:
```py
def Test():
    tmp = 10
    tmp += 1
```

## Test case: simple function with return
JavaScript:
```js
function Test() {
    return 10;
}
```

Python:
```py
def Test():
    return 10
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

## Test case: arrow function to python lambda
JavaScript:
```js
const squares = numbers.map(num => num * num);
```

Python:
```py
squares = numbers.map(lambda num: num * num)
```

## Test case: long arrow function to python local function
JavaScript:
```js
const squares = numbers.map(num => {
    const tmp = num * num
    return tmp;
});
```

Python:
```py
def local_anonymous_func(num):
    tmp = num * num
    return tmp

squares = numbers.map(local_anonymous_func)
```

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


todo: add missing test with return statment for normal function