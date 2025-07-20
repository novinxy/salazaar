# Test suite: variable declaration

## Test case: decimal
JavaScript:
```js
var number = 10;
```

Python:
```py
number = 10
```

## Test case: float
JavaScript:
```js
var number = 1.5;
```

Python:
```py
number = 1.5
```

## Test case: boolean true
JavaScript:
```js
var flag = true
```

Python:
```py
flag = True
```

## Test case: boolean false
JavaScript:
```js
var flag = false
```

Python:
```py
flag = False
```

## Test case: for loop ascending
JavaScript:
```js
for (let index = 0; index < array.length; index++) {
    const element = array[index];
}
```

Python:
```py
for index in range(len(array)):
    element = array[index]
```

## Test case: for loop descending
JavaScript:
```js
for (let index = array.length - 1; index >= 0; index--) {
    const element = array[index];
}
```

Python:
```py
for index in range(len(array) - 1, -1, -1):
    element = array[index]
```
