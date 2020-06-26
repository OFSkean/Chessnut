import evaluation.corex as ce
import numpy as np
import time

X = np.random.randint(0, 2, size=(15, 773))

layer1 = ce.Corex(n_hidden=20)  # Define the number of hidden factors to use.
layer1.fit(X)

print(layer1.clusters)  # Each variable/column is associated with one Y_j
# array([0, 0, 0, 1, 1])
print(layer1.labels[0])  # Labels for each sample for Y_0
# array([0, 0, 1, 1])
print(layer1.labels[1])  # Labels for each sample for Y_1
# array([0, 1, 0, 1])
print(layer1.tcs)  # TC(X;Y_j) (all info measures reported in nats).
# array([ 1.385,  0.692])
# TC(X_Gj) >=TC(X_Gj ; Y_j)
# For this example, TC(X1,X2,X3)=1.386, TC(X4,X5) = 0.693


avg = 0
for i in range(1000):
    X = np.random.randint(0, 2, size=(1, 773))
    s = time.time()
    print(layer1.predict(X))
    avg += time.time() - s

print(avg)
print(avg / 1000)