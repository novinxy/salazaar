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


## Test case: sort function
JavaScript:
```js
collection.sort()
```

Python:
```py
collection.sort()
```


## Test case: sort function with function
JavaScript:
```js
collection.sort(function compare(a,b) {
    return a.value > b.value
})
```

Python:
```py
collection.sort(key=lambda a: a.value)
```
