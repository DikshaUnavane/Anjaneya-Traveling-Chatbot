from sklearn.tree import DecisionTreeClassifier
# c1 = Horse Power and c2 = seate
# seat == 2 ---> 0
# seat == 8 ---> 1
# seat == 9 ---> 2
features = [[300 ,  0] , [450 , 0] , [200 , 1] , [150 , 2]]

# where sportsCar = 0 and Minivan = 1
label = [0 ,  0 , 1 , 1]
clf = DecisionTreeClassifier()
pred = clf.fit(features , label)
result = pred.predict([[150 , 1]])
if result == [0]:
    print("Sports Car")
else:
    print("Minivan")