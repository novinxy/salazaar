## Test case: array length
JavaScript:
```js
collection.length
```

Python:
```py
len(collection)
```

## Test case: array length on member collection
JavaScript:
```js
parent.collection.length
```

Python:
```py
len(parent.collection)
```

## Test case: array length on deep member collection
JavaScript:
```js
parent.child.collection.length
```

Python:
```py
len(parent.child.collection)
```

## Test case: array push
JavaScript:
```js
collection.push(1)
```

Python:
```py
collection.append(1)
```

## Test case: array push multiple values
JavaScript:
```js
collection.push(1, 2, 3, 4)
```

Python:
```py
collection.extend([1, 2, 3, 4])
```

## Test case: array concat
JavaScript:
```js
var newCollection = collection.concat(secondCollection)
```

Python:
```py
newCollection = collection + secondCollection
```

## Test case: concat multiple arrays
JavaScript:
```js
var newCollection = collection.concat(secondCollection, thirdCollection, col)
```

Python:
```py
newCollection = collection + secondCollection + thirdCollection + col
```

## Test case: splice remote elements
JavaScript:
```js
let arr = [1, 2, 3, 4, 5];
let removed = arr.splice(1, 2);

console.log(arr);      // [1, 4, 5]
console.log(removed);  // [2, 3]
```

Python:
```py
arr = [1, 2, 3, 4, 5]

removed = arr[1:3]
del arr[1:3]

print(arr)      # [1, 4, 5]
print(removed)  # [2, 3]
```


## Test case: splice insert elements
JavaScript:
```js
let arr = [1, 2, 5];
arr.splice(2, 0, 3, 4);

console.log(arr); // [1, 2, 3, 4, 5]
```

Python:
```py
arr = [1, 2, 5]

arr[2:2] = [3, 4]

print(arr)  # [1, 2, 3, 4, 5]
```

## Test case: splice replace elements
JavaScript:
```js
let arr = [1, 2, 3, 4];
arr.splice(1, 2, 9, 8);

console.log(arr); // [1, 9, 8, 4]
```

Python:
```py
arr = [1, 2, 3, 4]

arr[1:3] = [9, 8]

print(arr)  # [1, 9, 8, 4]
```

## Test case: splice remove from end
JavaScript:
```js
let arr = [1, 2, 3, 4];
arr.splice(-2, 1);

console.log(arr); // [1, 2, 4]
```

Python:
```py
arr = [1, 2, 3, 4]

removed = arr[-2]
del arr[-2]

print(arr)  # [1, 2, 4]
```
