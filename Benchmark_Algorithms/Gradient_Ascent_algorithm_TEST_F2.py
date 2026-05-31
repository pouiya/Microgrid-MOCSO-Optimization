import numpy as np
import matplotlib.pyplot as plt

# Define the objective functions
def objective_function_1(x1, x2):
    return -(x1)**2 + x2

def objective_function_2(x1, x2):
    return 0.5*x1 + x2 + 1

# Define the Gradient Ascent algorithm
class GradientAscent:
    def __init__(self, objective_function_1, objective_function_2, learning_rate, num_iterations):
        self.objective_function_1 = objective_function_1
        self.objective_function_2 = objective_function_2
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self.x1_history = []
        self.x2_history = []
    
    def optimize(self):
        x1 = np.random.uniform(-10, 10)
        x2 = np.random.uniform(-10, 10)
        
        for _ in range(self.num_iterations):
            self.x1_history.append(x1)
            self.x2_history.append(x2)
            
            grad_f1 = -2*x1
            grad_f2 = 0.5

            x1 += self.learning_rate * grad_f1
            x2 += self.learning_rate * grad_f2
        
        return x1, x2

# Define the main function
def main():
    learning_rate = 0.1
    num_iterations = 100
    
    gradient_ascent = GradientAscent(objective_function_1, objective_function_2, learning_rate, num_iterations)
    x1, x2 = gradient_ascent.optimize()
    
    f1 = objective_function_1(x1, x2)
    f2 = objective_function_2(x1, x2)
    
    print("Optimal Solution:")
    print("x1 =", x1)
    print("x2 =", x2)
    print("f1 =", f1)
    print("f2 =", f2)
    
    plt.plot(gradient_ascent.x1_history, gradient_ascent.x2_history, 'b-o')
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.title('Gradient Ascent Optimization')
    plt.show()

# Run the main function
if __name__ == '__main__':
    main()