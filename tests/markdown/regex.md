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

## Test case: exec to search
JavaScript:
```js
const r = /\d+/;
const m = r.exec("abc123");
```

Python:
```py
r = re.compile(r'\d+')
m = r.search('abc123')
```

## Test case: regex test operation
JavaScript:
```js
const r = /\d+/;
const m = r.test("abc123");
```

Python:
```py
r = re.compile(r'\d+')
m = r.search('abc123') is not None
```


## Test case: matchAll
JavaScript:
```js
const regexp = /\d+/g;
const text = "test1test2";

const array = text.matchAll(regexp);
```

Python:
```py
regexp = re.compile(r'\d+')
text = 'test1test2'

array = regexp.finditer(text)
```

## Test case: match
JavaScript:
```js
const regexp = /\d+/g;
const text = "test1test2";

const array = text.match(regexp);
```

Python:
```py
regexp = re.compile(r'\d+')
text = 'test1test2'

array = regexp.findall(text)
```

Add following tests:
- define capture groups
- define named capture groups
- mix of regex, \d + [] + groups
- look behind and ahead