from time import time
from typing import Any, List, Tuple, TypedDict

from nptyping import NDArray, Float64
import numpy as np


np.seterr(over='raise')

# Input Matrix
# X = | x1,1 x1,2 ... x1,n |
#     | x2,1 x2,2 ... x2,n |
#     |  ..   ..  ...  ..  |
#     | xm,1 xm,2 ... xm,n |
Number_of_Examples = Any
Number_of_Features = Any
Input_Matrix = NDArray[(Number_of_Examples, Number_of_Features), Float64]

# Target Matrix
# Y = | y1,1 y1,2 ... y1,n |
#     | y2,1 y2,2 ... y2,n |
#     |  ..   ..  ...  ..  |
#     | ym,1 ym,2 ... ym,n |
Number_of_Targets = Any
Target_Matrix = NDArray[(Number_of_Examples, Number_of_Targets), Float64]

# Output Matrix
# Y = | y1,1 y1,2 ... y1,n |
#     | y2,1 y2,2 ... y2,n |
#     |  ..   ..  ...  ..  |
#     | ym,1 ym,2 ... ym,n |
Output_Matrix = NDArray[(Number_of_Examples, Number_of_Targets), Float64]

# Perceptron
# Pk = | w1,k |
#      | w2,k |
#      |  ..  |
#      | wj,k |
# Bias
# bk = | w0,k |
Number_of_Inputs = Any
Bias, Weight = Float64, Float64
Perceptron = NDArray[(Number_of_Inputs, 1), Weight]

# Layer
# Weights
# W = | P1, P2, ..., Pk |
# Biases
# Bk = | b1, b2, .., bk |
Number_of_Perceptrons = Any
Weights = NDArray[(Number_of_Inputs, Number_of_Perceptrons), Perceptron]
Biases = NDArray[Number_of_Perceptrons, Bias]

Network_Weights = List[Weights]
Network_Biases = List[Biases]


class Network(TypedDict):
    weights: Network_Weights
    biases: Network_Biases


class MultilayerPerceptron:

    def __init__(self, perceptrons_per_hidden_layer: List[int] = []):
        self.network: Network = {'weights': [], 'biases': []}
        self.score = 0.0
        self._perceptrons_per_hidden_layer = perceptrons_per_hidden_layer

    @staticmethod
    def activation(x: NDArray[Float64]) -> NDArray[Float64]:
        return 1.0 / (1.0 + np.exp(-x))

    def backpropagate(self, grad_z: NDArray[Float64], A: List, Z: List, layer_index: int) -> Tuple:
        # This is the gradient with respect to the weights "w" of the layer.
        grad_w = np.matmul(A[layer_index].T, grad_z)  # len( A ) = len( Z ) + 1
        # This is the gradient with respect to the biases "b" of the layer.
        grad_b = grad_z.sum(axis=0)
        if layer_index > 0:  # There is no weighted input for layer 0.
            # This is the gradient with respect to the weighted input "z" of the layer.
            grad_z = self.derivative(Z[layer_index - 1])\
                     * np.matmul(grad_z, self.network['weights'][layer_index].T)
        return grad_z, grad_w, grad_b

    @staticmethod
    def cost(A: Output_Matrix, Y: Target_Matrix) -> Float64:
        return np.square(A - Y).sum()

    @staticmethod
    def derivative(x: NDArray[Float64]) -> NDArray[Float64]:
        return np.exp(-x) / np.square(1.0 + np.exp(-x))

    @staticmethod
    def grad(A: Output_Matrix, Y: Target_Matrix) -> NDArray[Float64]:
        return 2 * (A - Y)

    def forward_propagation(self, L: Input_Matrix) -> Output_Matrix:
        for w, b in zip(self.network['weights'], self.network['biases']):
            L = self.activation(np.matmul(L, w) + b)
        return L

    def _initialize(self, X: Input_Matrix, Y: Target_Matrix) -> None:
        number_of_inputs = X.shape[1]
        number_of_targets = Y.shape[1]
        self.network = {'weights': [], 'biases': []}
        # Random array contains fractions between zero and one.
        random_array = np.random.rand
        for number_of_perceptrons in self._perceptrons_per_hidden_layer:
            self.network['weights'].append(random_array(number_of_inputs, number_of_perceptrons) - 0.5)
            self.network['biases'].append(random_array(number_of_perceptrons) - 0.5)
            number_of_inputs = number_of_perceptrons
        self.network['weights'].append(random_array(number_of_inputs, number_of_targets) - 0.5)
        self.network['biases'].append(random_array(number_of_targets) - 0.5)
        return None

    def train(self, X: Input_Matrix, Y: Target_Matrix, learning_rate=1.0,
              convergence=0.01, batch_size=10, max_epoch=500, max_time=60) -> None:
        """This uses the Stochastic Gradient Descent training algorithm."""
        epoch = 1
        start = time()
        total_gradient = np.inf
        self._initialize(X, Y)
        output_layer_index = len(self.network['weights']) - 1
        while np.sqrt(total_gradient) > convergence:
            total_gradient = 0
            shuffle = np.random.permutation(len(X))
            X, Y = X[shuffle], Y[shuffle]
            for batch_x, batch_y in zip(np.array_split(X, len(X) // batch_size),
                                        np.array_split(Y, len(Y) // batch_size)):
                A, Z = [], []
                output = self._forward_propagation(batch_x, A, Z)
                # This is the gradient with respect to the output layer "a."
                grad_a = self.grad(output, batch_y)
                total_gradient += np.linalg.norm(grad_a)**2
                # This is the gradient with respect to the weighted input "z" of the output layer.
                grad_z = self.derivative(Z[-1]) * grad_a
                for layer_index in range(output_layer_index, -1, -1):
                    grad_z, grad_w, grad_b = self.backpropagate(grad_z, A, Z, layer_index)
                    self.network['weights'][layer_index] -= learning_rate * grad_w / len(batch_x)
                    self.network['biases'][layer_index] -= learning_rate * grad_b / len(batch_x)
            epoch += 1
            if time() - start > max_time:
                print('Maximum runtime encountered.')
                break
            if epoch > max_epoch:
                print('Maximum epoch encountered.')
                break
        self.score = self.cost(self.forward_propagation(X), Y)
        return None

    def _forward_propagation(self, X: Input_Matrix, A_ref: List, Z_ref: List) -> Output_Matrix:
        """
        This method is the same as the other forward propagation method,
        except it populates two containers, A and Z,
        which are used in the backpropagation method.
        """
        A_ref.append(X)  # len(A) = len(Z) + 1
        for w, b in zip(self.network['weights'], self.network['biases']):
            # weighted input to layer
            Z_ref.append(np.matmul(A_ref[-1], w) + b)
            # output of layer
            A_ref.append(self.activation(Z_ref[-1]))
        return A_ref[-1]
