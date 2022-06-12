# Python readline adds add history and editting to input()

If you add `inport readline` to a python program history and line editting functionality is added to thr `input()` function.


# Example

[input.py](https://github.com/tonyallan/python3-experiments/blob/main/python-readline/input.py):
```python3
import readline

# https://docs.python.org/3/library/readline.html

print('A blank line will exit this program\n')

while True:
    input_line = input('text> ')

    if len(input_line) == 0:
        break

    print(f'{input_line=}')

print('\nDone')
```

## Reference
1. [readline](https://docs.python.org/3/library/readline.html)
