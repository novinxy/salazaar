## Test case: while loop
JavaScript:
```js
while (true) {
    var i = 10;
}
```

Python:
```py
while True:
    i = 10
```

## Test case: do-while loop
JavaScript:
```js
do {
  i += 1;
  result += i;
} while (i < 5);
```

Python:
```py
i += 1
result += i

while i < 5:
  i += 1
  result += i

```

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


todo: add test for missing tests for returns, breaks and continue