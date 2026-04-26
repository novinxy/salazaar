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
while index < len(array):
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
index = len(array) - 1
while index >= 0:
    element = array[index]
    index -= 1
```

## Test case: for loop empty init
JavaScript:
```js
for (; !files.atEnd(); files.moveNext()) {
    var fileName = files.Name();
}
```

Python:
```py
while not files.atEnd():
    fileName = files.Name()
    files.moveNext()
```

## Test case: for loop empty condition
JavaScript:
```js
for (let value = 1;; files.moveNext()) {
    if (files.atEnd()) {
        break;
    }
    var fileName = files.Name();
}
```

Python:
```py
value = 1
while True:
    if files.atEnd():
        break
    fileName = files.Name()
    files.moveNext()
```

## Test case: for loop empty afterthough
JavaScript:
```js
for (let value = 1;!files.atEnd();) {
    var fileName = files.Name();
    files.moveNext()
}
```

Python:
```py
value = 1
while not files.atEnd():
    fileName = files.Name()
    files.moveNext()
```

## Test case: for of loop with continue statement
JavaScript:
```js
for (const elem of collection) {
    if (elem == 2) {
        continue
    }
    var tmp = elem;
}
```

Python:
```py
for elem in collection:
    if elem == 2:
        continue
    tmp = elem
```

## Test case: for in loop with break statement
JavaScript:
```js
for (const i in collection) {
    let elem = collection[i];
    if (elem == 2) {
        break
    }
    var tmp = elem;
}
```

Python:
```py
for i in range(len(collection)):
    elem = collection[i]
    if elem == 2:
        break
    tmp = elem
```

## Test case: for in loop with empty return statement
JavaScript:
```js
function hello() {
    for (const i in collection) {
        let elem = collection[i];
        if (elem == 3) {
            return
        }
        var tmp = elem;
    }
}
```

Python:
```py
def hello():
    for i in range(len(collection)):
        elem = collection[i]
        if elem == 3:
            return
        tmp = elem
```

## Test case: for in loop with null return statement
JavaScript:
```js
function hello() {
    for (const i in collection) {
        let elem = collection[i];
        if (elem == 3) {
            return null
        }
        var tmp = elem;
    }
}
```

Python:
```py
def hello():
    for i in range(len(collection)):
        elem = collection[i]
        if elem == 3:
            return None
        tmp = elem
```

## Test case: for in loop with return statement
JavaScript:
```js
function hello() {
    for (const i in collection) {
        let elem = collection[i];
        if (elem == 3) {
            return elem
        }
        var tmp = elem;
    }
}
```

Python:
```py
def hello():
    for i in range(len(collection)):
        elem = collection[i]
        if elem == 3:
            return elem
        tmp = elem
```