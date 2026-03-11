## Test case: literal with regex initialization
JavaScript:
```js
const regex = /ab+c/;
```

Python:
```py
regex = re.compile(r'ab+c')
```

## Test case: new regex by constructor
JavaScript:
```js
const regex =  new RegExp("ab+c");
```

Python:
```py
regex = re.compile(r'ab+c')
```

## Test case: new regex by constructor with variable
JavaScript:
```js
const regexpValue = "ab+c"
const regexp =  new RegExp(regexpValue);
```

Python:
```py
regexpValue = 'ab+c'
regexp = re.compile(regexpValue)
```

Add following tests:
- initialize as class
- call find
- call match
- call findall
- define capture groups
- define named capture groups
- mix of regex, \d + [] + groups
- look behind and ahead