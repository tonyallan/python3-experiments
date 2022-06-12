import readline

print('A blank line will exit this program\n')

while True:
    input_line = input('text> ')

    if len(input_line) == 0:
        break

    print(f'{input_line=}')

print('\nDone')