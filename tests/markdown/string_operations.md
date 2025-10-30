## Test case: one line string initialization
JavaScript:
```js
var text = "hello"
```

Python:
```py
text = 'hello'
```

## Test case: string concatenation with plus sign
JavaScript:
```js
var text = 'hello' + 'world' + 'from py'
```

Python:
```py
text = 'hello' + 'world' + 'from py'
```

## Test case: string concatenation with plus sign on many lines
JavaScript:
```js
var text = 'hello' +
'world' +
'from py'
```

Python:
```py
text = 'hello' + 'world' + 'from py'
```

## Test case: string concatenation with plus sign with variables
JavaScript:
```js
var text = 'hello ' + var1 + 'world' + var2
```

Python:
```py
text = 'hello ' + var1 + 'world' + var2
```


## Test case: template literal
JavaScript:
```js
var text1 = `hello ${var1} world ${var2}`
var text2 = `${var1} World world ${var2}`
var text3 = `${var1} World ${var2} world`

```

Python:
```py
text1 = f'hello {var1} world {var2}'
text2 = f'{var1} World world {var2}'
text3 = f'{var1} World {var2} world'
```

## Test case: multiline string
JavaScript:
```js
var text = `hello
world
from py
`
```

Python:
```py
text = 'hello\nworld\nfrom py\n'
```

## Test case: one-line with caret return string
JavaScript:
```js
var text = "hello\nworld\nfrom py\n"
```

Python:
```py
text = 'hello\nworld\nfrom py\n'
```