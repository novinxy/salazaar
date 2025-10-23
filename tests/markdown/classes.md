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

## Test case: Class declaration with inheritance
JavaScript:
```js
class Rectangle extends Shape {
  constructor(height, width) {
    super()
    this.height = height;
    this.width = width;
  }
}
```

Python:
```py
class Rectangle(Shape):

    def __init__(self, height, width):
        super().__init__()
        self.height = height
        self.width = width
```

## Test case: Class declaration access base property
JavaScript:
```js
class Rectangle extends Shape {
  constructor(height, width) {
    this.height = height;
    this.width = width;
    super.color
  }
}
```

Python:
```py
class Rectangle(Shape):

    def __init__(self, height, width):
        self.height = height
        self.width = width
        super().color
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


Maybe also following tests:
- static methods
- class methods
- class properties
- multiple functions