## Test case: handle line with empty line
JavaScript:
```js
var i = 10;
;
const a = 5;
```

Python:
```py
i = 10
a = 5
```

## Test case: handle line with double semicolon
JavaScript:
```js
var i = 10;;
```

Python:
```py
i = 10
```

## Test case: function with line with double semicolon
JavaScript:
```js
function test() {
    var i = 10;;
}
```

Python:
```py
def test():
    i = 10
```
