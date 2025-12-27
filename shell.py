#this is for running the interpreter in a terminal
from basic import run
while True:
    try:
        text = input('basic > ')
        result = run(text)
        if result is not None:  
            print(result)
    except Exception as e:
        print(e)
