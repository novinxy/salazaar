## Test case: Class declaration
JavaScript:
```js
class Rectangle {
  constructor(height, width) {
    this.height = height;
    this.width = width;
  }
}
```

Python:
```py
class Rectangle:
    def __init__(self, height, width):
        self.height = height
        self.width = width
```

## Test case: Anonymous class assigned to a variable
JavaScript:
```js
const Rectangle = class {
  constructor(height, width) {
    this.height = height;
    this.width = width;
  }
};
```

Python:
```py
class Rectangle:
    def __init__(self, height, width):
        self.height = height
        self.width = width
```

## Test case: Class assigned to a variable
JavaScript:
```js
const Rectangle = class Rectangle2 {
  constructor(height, width) {
    this.height = height;
    this.width = width;
  }
};
```

Python:
```py
class Rectangle:
    def __init__(self, height, width):
        self.height = height
        self.width = width
```
