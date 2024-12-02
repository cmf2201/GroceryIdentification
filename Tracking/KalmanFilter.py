import numpy as np
import random
import matplotlib.pyplot as plt

class KalmanFilter:
    def __init__(self, init_state: np.array):
        init_state.shape = (12,1)
        self.x = init_state
        self.P = np.eye(12,12) * 1000
        self.R = np.eye(4,4)
        self.prev_x = init_state
        self.H = np.array([
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        self.K = None
        self.prev_P = None
        self.predict_P = None
        self.predict_x = None
        
        self.count = 1
        self.steps = [0]
        self.state_data = np.empty((12,1))
        self.prediction_data = np.empty((12,1))
        
    
    def predict(self, dt=1):
        # State is defined by the box's center (x,y) position, box width, box height, and their velocities
        # state = [x1, x2, x3, x4, v1, v2, v3, v4]^T
        F = np.array([
            [1, 0, 0, 0, dt, 0, 0, 0, 0.5*dt**2, 0, 0, 0],
            [0, 1, 0, 0, 0, dt, 0, 0, 0, 0.5*dt**2, 0, 0],
            [0, 0, 1, 0, 0, 0, dt, 0, 0, 0, 0.5*dt**2, 0],
            [0, 0, 0, 1, 0, 0, 0, dt, 0, 0, 0, 0.5*dt**2],
            [0, 0, 0, 0, 1, 0, 0, 0, dt, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, dt, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, dt, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, dt],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        ])
        self.predict_x = np.matmul(F, self.x)
        self.predict_P = F @ self.P @ F.T + np.eye(12) * 1e-3  # Small regularization term to avoid singularity
    
    def update(self, measurement: np.array):
        measurement.shape = (4,1)
        y = measurement - self.H @ self.predict_x
        S = self.H @ self.P @ self.H.T + self.R
        self.K = self.predict_P @ self.H.T @ np.linalg.inv(S)
        correction = self.x + self.K @ y
        # self.x = correction
        self.x = np.concatenate((measurement, correction[4:12]), axis=0)
        self.P = (np.eye(12,12) - self.K @ self.H) @ self.predict_P
        
        self.state_data = np.concatenate((self.state_data, self.x), axis=1)
        self.prediction_data= np.concatenate((self.prediction_data, self.predict_x), axis=1)
        self.steps.append(self.count)
        self.count += 1

def main(args=None):
    """
    Mainly used for testing and plotting. Not ran during ByteTrack.
    """
    
    init_state = np.array([1,1,3,3, 0, 0, 0, 0, 0, 0, 0, 0])
    init_state.shape = (12,1)
    filter = KalmanFilter(init_state)
    value = 1
    
    # arrays for plotting
    steps = []
    ground_truth = []
    measurements = []
    filter_output = []
    predictions = []
    
    actual_x = 10
    actual_y = 10
    for i in range(100):
        actual_x = 10
        actual_y += 10
        actual_width = 10
        actual_height = 10
        actual_pose = np.array([
            [actual_x],
            [actual_y],
            [actual_width],
            [actual_height]
        ])
        filter.predict()
        # filter.x = filter.predict_x
        # filter.P = filter.predict_P
        measurement = actual_pose + random.uniform(-10, 10)
        filter.update(measurement)
        
        steps.append(i)
        ground_truth.append(actual_x)
        measurements.append(measurement[0])
        filter_output.append(filter.x[0])
        predictions.append(filter.predict_x[0])
    
    plt.plot(steps, ground_truth, label="Ground Truth", color="green", linestyle='-', linewidth=2)
    plt.plot(steps, measurements, label="Noisy Measurements", color="red", linestyle='-', linewidth=2)
    plt.plot(steps, filter_output, label="Kalman Filter Estimate", color="blue", linestyle='-', linewidth=2)
    plt.plot(steps, predictions, label="Kalman Filter Prediction", color="black", linestyle='-', linewidth=2)
 
    
    plt.title("Kalman Filter vs. Noisy Measurements vs. Ground Truth")
    plt.xlabel("Time [s]")
    plt.ylabel("Position [m]")
    plt.legend()
    plt.grid(True)
    plt.show()

# if __name__ == '__main__':
#     main()
