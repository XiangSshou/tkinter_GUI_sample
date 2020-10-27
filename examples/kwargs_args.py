def mult_args(*args):
    for i in args:
        print(i)


def mult_args_kwargs(*args,**kwargs):
    for i in args:
        print(i)
    for key,value in kwargs.items():
        print(key,value)

def print_letters_opt(sequence_of_letters,space=''):
    for x in sequence_of_letters:
        print(x + space)

def mult_args2(*args):
    sum=0
    for i in args:
        sum += i
    return sum
        
