## Test case: Closure test
JavaScript:
```js
function makeFunc() {
  const name = "test";
  function displayName() {
    console.log(name);
  }
  return displayName;
}

const myFunc = makeFunc();
myFunc();
```

Python:
```py
def makeFunc():
    name = 'test'

    def displayName():
        console.log(name)
    return displayName
myFunc = makeFunc()
myFunc()
```