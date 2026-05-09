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

## Test case: simple if without braces
JavaScript:
```js
if (false)
    log(2);
log(3)
```

Python:
```py
if False:
    log(2)
log(3)
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
    log(tmp)
    tmp += 1
    console.log(tmp)
} else if (i == 10) {
    var tmp = 20;
    tmp += 20;
    console.log(tmp)
} else if (i == -1) {
    var tmp = 1;
} else if (i == 50) {
    var tmp = 100;
    log('test')
} else {
    var tmp = 5000;
    tmp -= 1
    console.log("hello")
}
```

Python:
```py
if False:
    tmp = 10
    log(tmp)
    tmp += 1
    console.log(tmp)
elif i == 10:
    tmp = 20
    tmp += 20
    console.log(tmp)
elif i == -1:
    tmp = 1
elif i == 50:
    tmp = 100
    log('test')
else:
    tmp = 5000
    tmp -= 1
    console.log('hello')
```

## Test case: empty if-elif-else
JavaScript:
```js
if (true){}
else if (false) {}
else {
}

```

Python:
```py
if True:
    ...
elif False:
    ...
else:
    ...
```
