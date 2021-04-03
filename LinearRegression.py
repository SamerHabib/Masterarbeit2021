import matplotlib.pyplot as plt
from sklearn import linear_model
import numpy
def plotLinearReg(xx, yy):
    xx = numpy.array(xx).reshape((-1, 1))
    plt.scatter(xx, yy, color='black')
    plt.xlabel("Score")
    plt.ylabel("Saving")
    plt.show()
    reg = linear_model.LinearRegression()
    reg.fit(xx.reshape(-1,1), yy)
    m = reg.coef_[0]
    b = reg.intercept_
    print("slope=", m, "intercept=", b)
    plt.scatter(xx, yy, color='black')
    predicted_values = [reg.coef_ * i + reg.intercept_ for i in xx]
    plt.plot(xx, predicted_values, 'b')
    plt.xlabel("Score")
    plt.ylabel("Saving")
    plt.show()