## Test case: literal with regex initialization
JavaScript:
```js
const regex = /ab+c/;
```

Python:
```py
regex = r'ab+c'
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