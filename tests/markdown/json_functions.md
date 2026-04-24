## Test case: call json parse
JavaScript:
```js
const data = JSON.parse(json);
```

Python:
```py
data = json.loads(json)
```

## Test case: call json stringify
JavaScript:
```js
const jsonStr = JSON.stringify({ x: 5, y: 6 });
```

Python:
```py
jsonStr = json.dumps({x: 5, y: 6})
```