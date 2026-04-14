import array as arr 
myArray = arr.array("i",[ ])
print("0. Create a Array ")
print("1. Print Array")
print("2. Append Element")
print("3. Delete LAst Element")
print("4. Quit")

while True:
    choice = int(input("Enter your Choice: "))
    if choice == 0:
        limit = int(input("Enter the number of element : "))
        for _ in range(limit):
            num = int(input())
            myArray.append(num)
            if len(myArray) > limit :
                print("Array is not valid you are not able to entering proper elements")
    elif choice == 1:
        print("Here is the array: ")
        for element in myArray:
            print(element)
    elif choice == 2:
        print("Enter a number which you want to append")
        num = int(input())
        myArray.append(num)
        for element in myArray:
            print(element)
    elif choice == 3:
        print("Here is array after applying pop method ")
        myArray.pop()
        for element in myArray:
            print(element)
    elif  choice == 4:
        print("Thank You!!!")
        break
    else:
        print("Enter choice number between 1-4")