## Test case: typeof assign to variable

JavaScript:
```js
let result = typeof value
```

Python
```py
result = type(value)
```

## Test case: typeof String

JavaScript:
```js
let result = typeof value
typeof value == "string"
typeof value != "string"
```

Python
```py
result = type(value)
isinstance(value, str)
not isinstance(value, str)
```

## Test case: typeof Number

JavaScript:
```js
typeof value == "number"
typeof value != "number"
```

Python
```py
isinstance(value, (int, float))
not isinstance(value, (int, float))
```


## Test case: typeof Number

JavaScript:
```js
typeof value == "boolean"
"boolean" != typeof value
```

Python
```py
isinstance(value, bool)
not isinstance(value, bool)
```


## Test case: typeof undefined

JavaScript:
```js
typeof value == "undefined"
typeof value != "undefined"
```

Python
```py
value is None
value is not None
```

## Test case: typeof object

JavaScript:
```js
typeof value == "object"
typeof value != "object"
```

Python
```py
isinstance(value, object)
not isinstance(value, object)
```
## Test case: typeof on both sides

JavaScript:
```js
typeof value == typeof value1
typeof value != typeof value2
```

Python
```py
type(value) == type(value1)
type(value) != type(value2)
```