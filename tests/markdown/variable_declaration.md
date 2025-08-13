## Test case: undefined value
JavaScript:
```js
var number = undefined;
```

Python:
```py
number = None
```

## Test case: null value
JavaScript:
```js
var number = null;
```

Python:
```py
number = None
```

## Test case: declare - without initialization
JavaScript:
```js
let nothing
```

Python:
```py
nothing = None
```

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

## Test case: string
JavaScript:
```js
var text = 'Hello world';
```

Python:
```py
text = 'Hello world'
```

## Test case: list
JavaScript:
```js
var collection = [1, 2, 3];
```

Python:
```py
collection = [1, 2, 3]
```

## Test case: list of variables
JavaScript:
```js
var collection = [var1, var2, var3];
```

Python:
```py
collection = [var1, var2, var3]
```

## Test case: objects
JavaScript:
```js
var collection = {'key1': 'value1', 'key2': 'value2'};
```

Python:
```py
collection = {'key1': 'value1', 'key2': 'value2'}
```

## Test case: list of objects
JavaScript:
```js
var collection = [{'key1': '1st', 'key2': 2}, {'key3': true, 'key4': [1, 2, 3]}];
```

Python:
```py
collection = [{'key1': '1st', 'key2': 2}, {'key3': True, 'key4': [1, 2, 3]}]
```

## Test case: multiple - tuple unpack
JavaScript:
```js
var [number, flag] = [10, true]
```

Python:
```py
number, flag = (10, True)
```

## Test case: multiple - split with comma
JavaScript:
```js
let x = 20, y = 30, z = 40;
```

Python:
```py
x = 20
y = 30
z = 40
```

## Test case: multiple - assignment
JavaScript:
```js
let x = y = z = 10
```

Python:
```py
x = y = z = 10
```

## Test case: multiple - declaration then assignment
JavaScript:
```js
let x = y = z;
x = y = z = 10;
```

Python:
```py
x = y = z = 10
```

## Test case: assignment expression
JavaScript:
```js
flag = true
```

Python:
```py
flag = True
```

## Test case: multi assignment expression in line
JavaScript:
```js
flag = flag1 = flag2
```

Python:
```py
flag = flag1 = flag2
```