## Test case: Basic try-catch

JavaScript:
```js
try {
    let x = 1 / 0;
    console.log("Hello world");
} catch (e) {
    e += 'err'
    console.log('Error:', e);
}
```

Python
```py
try:
    x = 1 / 0
    console.log('Hello world')
except Exception as e:
    e += 'err'
    console.log('Error:', e)
```

---

## Test case: try-catch-finally

JavaScript
```js
try {
    doSomething();
} catch (err) {
    handleError(err);
} finally {
    cleanup();
}
```

Python
```py
try:
    doSomething()
except Exception as err:
    handleError(err)
finally:
    cleanup()
```

---

## Test case: Catching specific error

JavaScript
```js
try {
    JSON.parse('invalid');
} catch (e) {
    if (e instanceof SyntaxError) {
        console.log('Syntax error!');
    }
}
```

Python
```py
try:
    JSON.parse('invalid')
except Exception as e:
    if isinstance(e, SyntaxError):
        console.log('Syntax error!')
```

---

## Test case: Nested try-catch

JavaScript
```js
try {
    try {
        risky();
    } catch (inner) {
        handle(inner);
    }
} catch (outer) {
    handle(outer);
}
```

Python
```py
try:
    try:
        risky()
    except Exception as inner:
        handle(inner)
except Exception as outer:
    handle(outer)
```

---

## Test case: Rethrowing error

JavaScript
```js
try {
    doSomething();
} catch (e) {
    throw e;
}
```

Python
```py
try:
    doSomething()
except Exception as e:
    raise
```
