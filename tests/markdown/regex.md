## Test case: literal with regex initialization
JavaScript:
```js
const regex = /ab+c/;
```

Python:
```py
import re
regex = re.compile(r'ab+c')
```

## Test case: new regex by constructor
JavaScript:
```js
const regex =  new RegExp("ab+c");
```

Python:
```py
import re
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
import re
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
import re
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
import re
r = re.compile(r'\d+')
m = bool(r.search('abc123'))
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
import re
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
import re
regexp = re.compile(r'\d+')
text = 'test1test2'
array = regexp.findall(text)
```

## Test case: regex class with named capture group
JavaScript:
```js
const regex = new RegExp("(?<num>\\d+)");
```

Python:
```py
import re
regex = re.compile(r'(?P<num>\d+)')
```
