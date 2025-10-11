## Test case: Import module
JavaScript:
```js
import 'module.js'
```

Python:
```py
import module
```

## Test case: NameSpace import
JavaScript:
```js
import * as module from 'module.js'
```

Python:
```py
import module
```

## Test case: NameSpace import with rename
JavaScript:
```js
import * as mod from 'module.js'
```

Python:
```py
import module as mod
```

## Test case: Named import
JavaScript:
```js
import {hello, world} from 'module.js'
```

Python:
```py
from module import hello, world
```

## Test case: Default import
JavaScript:
```js
import hello from 'module.js'
```

Python:
```py
from module import hello
```

## Test case: Nested imports
JavaScript:
```js
import 'libraries/module.js'
```

Python:
```py
import libraries.module
```