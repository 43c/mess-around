'''
mostly just try out forward pass and
back prop

architecture

i NEED to rename activation function since z is used for logits

z : activation function
i : inputs
h1 : hidden layer 1
h2 : hidden layer 2
o : outputs
L : loss
Lf : loss function
Wi1 : inputs to h1 weights
W12 : h1 to h2 weights
W2o : h2 to output weights

inputs -> z -> hidden1 -> z -> hidden2 -> z -> output

L = Lf(o)
o = z(a3)
a3 = W2o @ h2
h2 = z(a2)
a2 = W12 @ h1
h1 = z(a1)
a1 = Wi1 @ i

L = Lf(z(W2o @ z(W12 @ (z(wi1 @ i)))))

we want to find how the loss changes in relation to how
the weights change. thus we want to find
- dL / dW2o
- dL / dW12
- dL / dWi1

for a3, W20, h2 with sizes a n x 1, n x r, r x 1
W2o.l
dL / do : 1 x o.l
do / da3 : o.l x n
da3 / dW2o : n x n x r

dL / da3 = (dL / do) * (do / da3)
dL / dW2o = (dL / da3) * (da3 / dW2o)

multi variate chain rule
dL / da3_x,y = dL / do_1,1 * do_1,1 / da3_x,y + dL / do_2,1 * do_2,1 / da3_x,y + ... 

o_1,1 = z(a3_1,1)
o_2,1 = z(a3_2,1)
...
o_n,1 = z(a3_n,1)

da3 / dW2o_x,y follows a similar pattern, so each dL / dW2o_x,y is some summation (n, m)
over dL / da3_n,m * da3_n,m / dW2o_x,y
'''

from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt

def z(x):
    return 1 / (1 + np.exp(-x))

def z_p(y):
    # derivative of sigmoid
    # z(x)(1 - z(x))
    return y * (1 - y)

def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    # basically 1 if above 0, else 0
    return (x > 0).astype(float)

def leaky_relu(x, leak_factor = 0.05):
    return np.where(x > 0, x, x * leak_factor)

def leaky_relu_derivative(x, leak_factor = 0.05):
    return np.where(x > 0, 1, leak_factor)

def sigmoid(x):
    # 1 / (1 + e^-x)
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    # derivative of sigmoid
    # σ(x)(1 - σ(x))
    return x * (1 - x)

def loss_BCE(y_i, o_i):
    return -(y_i * np.log(o_i) + (1 - y_i) * np.log(1 - o_i))

def loss_BCE_derivative(y_i, o_i):
    '''
    derivative of ln(x) is 1/x
    z := logits, o := sigmoid(logits)
    the thing is dL / dz is far simpler than dL / do

    
    dL / do = (1 - y_i) / (1 - o_i) - y_i / o_i
    do / dz = σ(z)(1 - σ(z))
            = o_i * (1 - o_i)
    dL / dz = dL / do * do / dz
            = ((1 - y_i) / (1 - o_i) - y_i / o_i) * (o_i * (1 - o_i))
            = o_i * (1 - y_i) - y_i * (1 - o_i)
            = o_i - o_i * y_i - y_i + o_i * y_i
            = o_i - y_i

    crazy how it works huh
    '''
    return - y_i / o_i + (1 - y_i) / (1 - o_i)
    ...

class SimpleFNN:
    def __init__(self, input_size, hidden1_size, hidden2_size, output_size, learning_rate=0.01):
        # random weights
        self.Wi1 = np.random.randn(input_size, hidden1_size)
        self.W12 = np.random.randn(hidden1_size, hidden2_size)
        self.W2o = np.random.randn(hidden2_size, output_size)

        # zero biases
        self.b1 = np.zeros((1, hidden1_size))
        self.b2 = np.zeros((1, hidden2_size))
        self.bo = np.zeros((1, output_size))

        self.lr = learning_rate

    def forward(self, X):
        self.a1 = X @ self.Wi1 + self.b1
        self.h1 = leaky_relu(self.a1)

        self.a2 = self.h1 @ self.W12  + self.b2
        self.h2 = leaky_relu(self.a2)

        self.a3 = self.h2 @ self.W2o + self.bo
        self.o = sigmoid(self.a3)

        return self.o

    def backward(self, X, y):
        # loss derivative using binary cross entropy -> dL/do = (o - y)
        # the dL / dz = dL / do * do / dz tech go crazy
        dL_da3 = self.o - y

        # W2o : n x m
        # h2 : 1 x n
        # a3 : 1 x m

        dL_dW2o = self.h2.T @ dL_da3
        dL_dbo = np.sum(dL_da3, axis=0, keepdims=True)


        dL_dh2 = dL_da3 @ self.W2o.T
        dL_da2 = dL_dh2 * leaky_relu_derivative(self.a2)
        dL_dW12 = self.h1.T @ dL_da2
        dL_db2 = np.sum(dL_da2, axis=0, keepdims=True)

        dL_dh1 = dL_da2 @ self.W12.T
        dL_da1 = dL_dh1 * leaky_relu_derivative(self.a1)
        dL_dWi1 = X.T @ dL_da1
        dL_db1 = np.sum(dL_da1, axis=0, keepdims=True)

        # update weights and bias
        self.W2o -= self.lr * dL_dW2o
        self.W12 -= self.lr * dL_dW12
        self.Wi1 -= self.lr * dL_dWi1
        self.bo -= self.lr * dL_dbo
        self.b2 -= self.lr * dL_db2
        self.b1 -= self.lr * dL_db1

    def train(self, X, y, epochs=10000, progress_split=20):
        for epoch in range(epochs):
            loss = 0

            # stochastic gradient descent
            # cuz im doing one sample at a time
            for i in range(X.shape[0]):
                x_i = X[[i], :]
                y_i = y[[i], :]
                o = self.forward(x_i)
                self.backward(x_i, y_i)

                # we clip it so we dont get log(0) stuff
                eps = np.finfo(float).eps
                o = np.clip(o, eps, 1 - eps)
                loss -= y_i * np.log(o) + (1 - y_i) * np.log(1 - o)

            div = epochs // progress_split
            if epoch % div == 0:
                print(f"epoch={epoch}, loss={loss.item() / X.shape[1]:.6f}")

def main():
    digits_test()

def digits_meta():
    digits = load_digits()
    print(digits.data[0])
    print(digits.data[0]/16)
    print(len(digits.data))
    print(digits.feature_names)
    print(digits.target_names)

def digits_test():
    digits = load_digits()
    X = digits.data
    # sigmoid overflows if i don't normalize?
    # i want everything 0 to 1 anyway
    X = X / 16.0
    
    # binary classification task for now since my output
    # layer is sigmoid -> bce
    # could softmax for the big boy classification
    y = (digits.target == 3).astype(int).reshape(-1, 1)


    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # init and train
    fnn = SimpleFNN(input_size=64, hidden1_size=32, hidden2_size=16, output_size=1, learning_rate=0.02)
    fnn.train(X_train, y_train, epochs=100)

    # eval on tests
    outputs = fnn.forward(X_test)
    preds = (outputs > 0.5).astype(int)
    accuracy = np.mean(preds == y_test)
    print()
    print(f"accuracy: {accuracy * 100:.2f}%")

if __name__ == "__main__":
    main()