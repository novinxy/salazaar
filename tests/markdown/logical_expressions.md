## Test case: and expression
JavaScript:
```js
var1 == var2 && i == 10;
```

Python:
```py
var1 == var2 and i == 10
```

## Test case: or expression
JavaScript:
```js
var1 == var2 || i == 10;
```

Python:
```py
var1 == var2 or i == 10
```

## Test case: negation
```js
!temp;
```

Python:
```py
not temp
```

## Test case: and then or expression
JavaScript:
```js
false && true || true
```

Python:
```py
False and True or True
```

## Test case: or then and expression
JavaScript:
```js
false || true && true
```

Python:
```py
False or (True and True)
```

## Test case: and then parentheses with or expression
JavaScript:
```js
false && (true || true)
```

Python:
```py
False and (True or True)
```

## Test case: another one
JavaScript:
```js
false && true && true
```

Python:
```py
False and True and True
```

## Test case: another one with parentheses
JavaScript:
```js
(false && true) && true
```

Python:
```py
(False and True) and True
```

## Test case: another two
JavaScript:
```js
false || true && false
```

Python:
```py
False or (True and False)
```

## Test case: chained logical expressions
JavaScript:
```js
false || true && false || true && false || true
```

Python:
```py
False or (True and False) or (True and False) or True
```

## Test case: chained logical expressions 2
JavaScript:
```js
var1 == var2 && var3 != var4 || var5 === var6
```

Python:
```py
var1 == var2 and var3 != var4 or var5 == var6
```

## Test case: logical not expression
JavaScript:
```js
!false && true || !true
```

Python:
```py
not False and True or not True
```

## Test case: mixed operators
JavaScript:
```js
false && true || false && true || true
```

Python:
```py
False and True or False and True or True
```

## Test case: mixed operators2
JavaScript:
```js
if(false || !true && false || false) {

	var z = 1
}
```

Python:
```py
if False or not True and False or False:
	z = 1
```


