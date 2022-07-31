from numbers import Real
from time import time
from typing import Any, Dict, List, Tuple

import numpy as np


np.seterr(over='raise')

# Input Matrix
# X = | x1,1 x1,2 ... x1,n |
#     | x2,1 x2,2 ... x2,n |
#     |  ..   ..  ...  ..  |
#     | xm,1 xm,2 ... xm,n |
NumberOfExamples = Any  # m
NumberOfFeatures = Any  # n
InputMatrix = np.ndarray[(NumberOfExamples, NumberOfFeatures), Real]

# Target Matrix (True Values)
# Y = | y1,1 y1,2 ... y1,k |
#     | y2,1 y2,2 ... y2,k |
#     |  ..   ..  ...  ..  |
#     | ym,1 ym,2 ... ym,k |
NumberOfTargets = Any
TargetMatrix = np.ndarray[(NumberOfExamples, NumberOfTargets), Real]

# Output Matrix (Computed Values)
# Y = | y'1,1 y'1,2 ... y'1,k |
#     | y'2,1 y'2,2 ... y'2,k |
#     |   ..    ..  ...   ..  |
#     | y'm,1 y'm,2 ... y'm,k |
OutputMatrix = np.ndarray[(NumberOfExamples, NumberOfTargets), Real]

# Gradient Matrix
# R = | y"1,1 y"1,2 ... y"1,k |
#     | y"2,1 y"2,2 ... y"2,k |
#     |   ..    ..  ...   ..  |
#     | y"m,1 y"m,2 ... y"m,k |
GradientMatrix = np.ndarray[(NumberOfExamples, NumberOfTargets), Real]

# Perceptron
# Pk' = | w1,k' |
#       | w2,k' |
#       |  ..   |
#       | wj,k' |
# Bias
# bk' = | w0,k' |
# k': number of the perceptron
NumberOfInputs = Any
Bias, Weight = Real, Real
Perceptron = np.ndarray[(1, NumberOfInputs), Weight]

# Layer
# Weights
# W = | P1, P2, ..., Pk' |
# Biases
# Bk = | b1, b2, .., bk' |
NumberOfPerceptrons = Any
Weights = np.ndarray[(NumberOfPerceptrons, NumberOfInputs), Weight]
Biases = np.ndarray[NumberOfPerceptrons, Bias]

Layer_Number = int
Network_Weights = Dict[Layer_Number, Weights]
Network_Biases = Dict[Layer_Number, Biases]


class NeuralNetwork:

    instantiated = False

    def __init__(self, perceptrons_per_hidden_layer: List[int] = []):
        self.weights: Network_Weights = {}
        self.biases: Network_Biases = {}
        self.score = 0.0
        self.initiated = False
        self.instantiated = True
        self._perceptrons_per_hidden_layer = perceptrons_per_hidden_layer

    @staticmethod
    def activation(x: np.ndarray[Any, Real]) -> np.ndarray[Any, Real]:
        """This is the logistic function with amplitude and steepness of one."""
        return 1.0 / (1.0 + np.exp(-x))

    @staticmethod
    def derivative(x: np.ndarray[Any, Real]) -> np.ndarray[Any, Real]:
        """This is the first derivative of the logistic function with amplitude and steepness of one."""
        return np.exp(-x) / np.square(1.0 + np.exp(-x))

    @staticmethod
    def error(A: OutputMatrix, Y: TargetMatrix) -> Real:
        """This is the sum of squared residuals."""
        return np.square(A - Y).sum()

    def forward_propagation(self, L: InputMatrix) -> OutputMatrix:
        raise NotImplementedError('The method "forward_propagation" is not implemented.')

    @staticmethod
    def grad(A: OutputMatrix, Y: TargetMatrix) -> GradientMatrix:
        """This is the gradient of the sum of squared residuals with respect to the output of the output layer."""
        return 2 * (A - Y)

    def initialize(self, number_of_features: int, number_of_targets: int) -> None:
        raise NotImplementedError('The method "initialize" is not implemented.')


class MultilayerPerceptron(NeuralNetwork):

    def __init__(self, perceptrons_per_hidden_layer: List[int] = []):
        super().__init__(perceptrons_per_hidden_layer)

    def backpropagate(self, grad_z: np.ndarray, A: Dict, Z: Dict, current_layer: int) -> Tuple:
        # This is the gradient with respect to the weights "w" of the layer.
        grad_w = np.matmul(A[current_layer].T, grad_z)  # len( A ) = len( Z ) + 1
        # This is the gradient with respect to the biases "b" of the layer.
        grad_b = grad_z.sum(axis=0)
        if current_layer > 0:  # There is no weighted input for the zeroth layer.
            # This is the gradient with respect to the weighted input "z" of the layer.
            grad_z = self.derivative(Z[current_layer]) * np.matmul(grad_z, self.weights[current_layer].T)
        return grad_z, grad_w, grad_b

    def forward_propagation(self, L: InputMatrix) -> OutputMatrix:
        for w, b in zip(self.weights.values(), self.biases.values()):
            L = self.activation(np.matmul(L, w) + b)
        return L

    def initialize(self, number_of_features: int, number_of_targets: int) -> None:
        self.weights, self.biases = {}, {}
        # Random array contains fractions between zero and one.
        random_array = np.random.rand
        current_layer = 1  # The input or zeroth layer has no weights or biases.
        number_of_inputs = number_of_features
        for number_of_perceptrons in self._perceptrons_per_hidden_layer:
            self.weights[current_layer] = random_array(number_of_inputs, number_of_perceptrons) - 0.5
            self.biases[current_layer] = random_array(number_of_perceptrons) - 0.5
            number_of_inputs = number_of_perceptrons
            current_layer += 1
        # The weights and biases for the output layer are below.
        self.weights[current_layer] = random_array(number_of_inputs, number_of_targets) - 0.5
        self.biases[current_layer] = random_array(number_of_targets) - 0.5
        self.initiated = True
        return None

    def train(self, X: InputMatrix, Y: TargetMatrix, batch_size=10, convergence=0.0,
              learning_rate=1.0, max_epoch=10, max_time_seconds=60) -> None:
        """This uses the Stochastic Gradient Descent training algorithm."""
        epoch = 1
        start = time()
        self.initialize(X.shape[1], Y.shape[1])
        output_layer = len(self.weights)
        while True:
            total_gradient = 0.0
            shuffle = np.random.permutation(len(X))
            X, Y = X[shuffle], Y[shuffle]
            for batch_x, batch_y in zip(np.array_split(X, len(X) // batch_size),
                                        np.array_split(Y, len(Y) // batch_size)):
                A, Z = {}, {}
                batch_output = self._forward_propagation(batch_x, A, Z)
                # This is where backpropagation begins.
                # This is the gradient with respect to the output layer "a".
                grad_a = self.grad(batch_output, batch_y)
                total_gradient += np.linalg.norm(grad_a)**2
                # This is the gradient with respect to the weighted input "z" of the output layer.
                grad_z = self.derivative(Z[output_layer]) * grad_a
                for current_layer in range(output_layer, -1, -1):
                    # These are the gradients with respect to the weighted input "z",
                    # weights "w" and biases "b" of the current layer.
                    grad_z, grad_w, grad_b = self.backpropagate(grad_z, A, Z, current_layer)
                    self.weights[current_layer] -= learning_rate * grad_w / len(batch_x)
                    self.biases[current_layer] -= learning_rate * grad_b / len(batch_x)
                # This is where backpropagation ends.
            epoch += 1
            if time() - start > max_time_seconds:
                print('Maximum runtime encountered.')
                break
            if epoch > max_epoch:
                print('Maximum epoch encountered.')
                break
            if np.sqrt(total_gradient) <= convergence:
                print('Convergence achieved.')
                break
        final_output = self.forward_propagation(X)
        self.score = self.error(final_output, Y)
        return None

    def _forward_propagation(self, X: InputMatrix, A_ref: Dict, Z_ref: Dict) -> OutputMatrix:
        """
        This method is the same as the other forward propagation method,
        except it populates two containers, A and Z,
        which are used in the backpropagation method.
        """
        current_layer = 0
        # The input layer does not have a weighted input. Therefore, len(A) = len(Z) + 1.
        A_ref[current_layer] = X
        current_layer += 1
        for w, b in zip(self.weights, self.biases):
            # "Z" is the weighted input to the current layer.
            Z_ref[current_layer] = np.matmul(A_ref[current_layer - 1], w) + b
            # "A" is the output of the current layer.
            A_ref[current_layer] = self.activation(Z_ref[current_layer])
            current_layer += 1
        return A_ref[current_layer - 1]
