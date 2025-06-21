import pandas as pd
import numpy as np

# Parameters
num_samples = 1000
attack_types = ['Normal', 'DDoS', 'MITM', 'Data Leak', 'Spoofing', 'Brute Force']
attack_distribution = [0.7, 0.1, 0.06, 0.05, 0.05, 0.04]  # sum to 1.0

# Generate labels based on distribution
labels = np.random.choice(attack_types, size=num_samples, p=attack_distribution)

# Create synthetic features
data = pd.DataFrame({
    'packet_size': np.random.randint(50, 1500, num_samples),
    'duration': np.random.uniform(0.1, 5.0, num_samples),
    'protocol': np.random.randint(0, 3, num_samples),  # 0=TCP, 1=UDP, 2=ICMP
    'src_bytes': np.random.randint(0, 10000, num_samples),
    'dst_bytes': np.random.randint(0, 10000, num_samples),
    'attack_type': labels
})

# Save dataset
data.to_csv('../backend/iot_security__multi_data.csv', index=False)
print("Generated synthetic multi-class dataset.")
