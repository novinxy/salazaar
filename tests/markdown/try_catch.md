## Test case: Basic try-catch

JavaScript:
```js
try {
    let x = 1 / 0;
} catch (e) {
    console.log('Error:', e);
}
```

Python
```py
try:
    x = 1 / 0
except Exception as e:
    print('Error:', e)
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
    do_something()
except Exception as err:
    handle_error(err)
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
    json.loads('invalid')
except json.JSONDecodeError:
    print('Syntax error!')
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
    do_something()
except Exception as e:
    raise
```
