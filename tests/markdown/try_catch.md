### TestCase: Basic try-catch

JavaScript
```js
try {
    let x = 1 / 0;
} catch (e) {
    console.log('Error:', e);
}
```

Python
```python
try:
    x = 1 / 0
except Exception as e:
    print('Error:', e)
```

---

### TestCase: try-catch-finally

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
```python
try:
    do_something()
except Exception as err:
    handle_error(err)
finally:
    cleanup()
```

---

### TestCase: Catching specific error

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
```python
try:
    json.loads('invalid')
except json.JSONDecodeError:
    print('Syntax error!')
```

---

### TestCase: Nested try-catch

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
```python
try:
    try:
        risky()
    except Exception as inner:
        handle(inner)
except Exception as outer:
    handle(outer)
```

---

### TestCase: Rethrowing error

JavaScript
```js
try {
    doSomething();
} catch (e) {
    throw e;
}
```

Python
```python
try:
    do_something()
except Exception as e:
    raise
```
