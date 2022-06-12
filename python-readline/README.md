# Python readline adds add history and editting to input()

If you add `inport readline` to a Python 3 program, 
history and line editting functionality is added to the `input()` function.


# Example

[input.py](https://github.com/tonyallan/python3-experiments/blob/main/python-readline/input.py):
```python3
import readline

print('A blank line will exit this program\n')

while True:
    input_line = input('text> ')

    if len(input_line) == 0:
        break

    print(f'{input_line=}')

print('\nDone')
```

## Reference
1. Python3 [GNU readline interface](https://docs.python.org/3/library/readline.html)
