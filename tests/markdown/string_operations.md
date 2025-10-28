## Test case: One line string initialization
JavaScript:
```js
var text = "hello"
```

Python:
```py
text = 'hello'
```

## Test case: String concated with plus sign
JavaScript:
```js
var text = 'hello' + 'world' + 'from py'
```

Python:
```py
text = 'hello' + 'world' + 'from py'
```

## Test case: String concated with plus sign on many lines
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

## Test case: String concated with plus sign with variables
JavaScript:
```js
var text = 'hello' + var1 + 'world' + var2
```

Python:
```py
text = 'hello' + var1 + 'world' + var2
```


## Test case: Template Literal
JavaScript:
```js
var text = `hello ${var1} world ${var2}`
```

Python:
```py
text = f'hello {var1} world {var2}'
```

## Test case: Multiline Template Literal
JavaScript:
```js
var text = `hello
world
from py
`
```

Python:
```py
text = '''hello
world
from py
'''
```