## Test case: for in
JavaScript:
```js
for (const i in collection) {
    var tmp = collection[i];
}
```

Python:
```py
for i in range(len(collection)):
    tmp = collection[i]
```

## Test case: for of
JavaScript:
```js
for (const elem of collection) {
    var tmp = elem;
}
```

Python:
```py
for elem in collection:
    tmp = elem
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
index = 0
while index < array.length:
    element = array[index]
    index += 1
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
index = array.length - 1
while index >= 0:
    element = array[index]
    index -= 1
```


todo: add test for missing tests for returns, breaks and continue