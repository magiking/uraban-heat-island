import numpy as np
import math
from sklearn.linear_model import LinearRegression

def load_data():
    data = np.load('linked-data.npy', allow_pickle=True)
    print(data.shape)
    scrap = []
    for i in range(data.shape[0]):
        if None in data[i] or 255 in data[i]:
            scrap.append(i)
    data = np.delete(data, scrap, 0)
    print(data.shape)
    y = np.float32(data[:,7])
    X = np.delete(data,7,1)
    for row in X:
        row[4] = int(row[4][:2])
    X = np.float32(X)
    
    # separate to train and test
    split = math.floor(0.7 * len(X))
    x_train = X[:split]
    y_train = y[:split]
    x_test = X[:split]
    y_test = y[:split]
    return x_train, y_train, x_test, y_test

if __name__ == "__main__":
    x_train, y_train, x_test, y_test = load_data()

    model = LinearRegression()
    x_train = x_train[:,6].reshape(-1,1)
    x_test = x_test[:,6].reshape(-1,1)
    model.fit(x_train, y_train)

    prediction = model.predict(x_test)
    err = y_test - prediction
    mse = np.mean(err * err)
    print('mse: ', mse)
    print(y_test[:10])
    print(prediction[:10])
    
