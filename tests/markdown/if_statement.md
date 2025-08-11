## Test case: simple if
JavaScript:
```js
if (false) {
    var tmp = 10;
}
```

Python:
```py
if False:
    tmp = 10
```

## Test case: if else
JavaScript:
```js
if (false) {
    var tmp = 10;
} else {
    var tmp = 20;
}
```

Python:
```py
if False:
    tmp = 10
else:
    tmp = 20
```

## Test case: if elif
JavaScript:
```js
if (false) {
    var tmp = 10;
} else if (i == 10) {
    var tmp = 20;
}
```

Python:
```py
if False:
    tmp = 10
elif i == 10:
    tmp = 20
```

## Test case: multiple elif with else
JavaScript:
```js
if (false) {
    var tmp = 10;
} else if (i == 10) {
    var tmp = 20;
} else if (i == -1) {
    var tmp = 1;
} else if (i == 50) {
    var tmp = 100;
} else {
    var tmp = 5000;
}
```

Python:
```py
if False:
    tmp = 10
elif i == 10:
    tmp = 20
elif i == -1:
    tmp = 1
elif i == 50:
    tmp = 100
else:
    tmp = 5000
```
