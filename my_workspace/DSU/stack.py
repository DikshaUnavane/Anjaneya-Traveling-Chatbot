# Using Normal List Way
stack = []
def isempty():
    if len(stack) == 0:
        print("Stack is Empty!!!")
    else:
        for num in stack:
            print(num)

ele1 = stack.append(10)
ele2 = stack.append(20)
ele3 = stack.append(30)
print("Here is a Stack: ")
isempty()
ele_1 = stack.pop()
ele_2 = stack.pop()
ele_3 = stack.pop()
print("poped elements are : ",ele_1 , ele2 , ele3)
isempty()