def add(a,b):
    return a+b

def subtract(a,b):
    return a-b

def multiply(a,b):
    return a*b

def divide(a,b):
    if b== 0:
        raise ValueError("Cannot divide by zero")
    return a/b

def modulus(a,b):
    return a%b

def exponent(a,b):
    return a**b

def floor_divide(a,b):
    if b== 0:
        raise ValueError("Cannot divide by zero")
    return a//b


def calculator():
    print("=== Program 1: Calculator ===")
    num1=float(input("Enter the first number: "))
    num2=float(input("Enter the second number: "))
    operator=input("Enter the operator (+, -, *, /, %, **, //): ")
    print(f" Number 1: {num1}, Number 2: {num2}, Operator: {operator}")
    
    match operator:
        case '+':
            result=add(num1,num2)
        case '-':
            result=subtract(num1,num2)
        case '*':
            result=multiply(num1,num2)
        case '/':
            result=divide(num1,num2)
        case '%':
            result=modulus(num1,num2)
        case '**':
            result=exponent(num1,num2)
        case  '//':
            result=floor_divide(num1,num2)
        case _:
            print("Invalid operator!")
            return
        
    print(f"{num1} {operator} {num2}={result}")
    
calculator()