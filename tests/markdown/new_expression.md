## Test case: simple NewExpression to class creation
JavaScript:
```js
var fso = new ActiveXObject("Scripting.FileSystemObject");
```

Python:
```py
fso = ActiveXObject('Scripting.FileSystemObject')
```

## Test case: complex NewExpression to class creation
JavaScript:
```js
var fso = new ActiveXObject("Scripting.FileSystemObject", new Dependency("test", 10));
```

Python:
```py
fso = ActiveXObject('Scripting.FileSystemObject', Dependency('test', 10))
```