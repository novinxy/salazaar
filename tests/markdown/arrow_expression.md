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