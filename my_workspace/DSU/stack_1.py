# using stack class

class Stack :
    def __init__(self):
        self.stack = []
    def push(self , element):
        self.stack.append(element)
        return self.stack
    def out(self):
        if not self.isempty :
            return self.stack.pop()
        else:
            print("Stack is empty")
            return None
    def isempty(self):
        return self.stack.pop == [ ] ,"Empty Stack"

while True: 
    s = Stack
    print("1. Push Element \n 2. Pop Element \n 3. Quiet")    
    choice = int(input("Enter your choice: "))
    if choice == 1:
        element = int(input("Enter values to add in stack: "))  
        s.push(element)
    elif choice == 2:
        s.out()
    elif choice == 3 :
        break
          