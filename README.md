# FlexSwarm: Swarm Learning With Flexible Labels

**A Decentralized AI Architecture for Training an Ensemble Model With Flexible Labels**


Project Overview:

We want to build a decentralized AI architecture that could train an ensemble model using datasets with a flexible number of labels. Also, we want to use blockchain to incentivize data owners to train models and allow clients to use the ensemble model for prediction.

We plan to use the CIFAR-10 dataset for simulation and testing. Then, we evaluate the feasibility and performance of using an ensemble model for training and prediction.


## TODO
1. AI Component:
    * Create a custom loss function to minimize false positives
      -- F1 score loss function has a gradient optimization problem. We might implement soft f1 if we have time, but we currently only use f1 score as an evaluation metric
    * Document simulation and testing details (finished)
    * Dataset partition (finished, save data owner information to an excel file)
    * Create build_model function
    * Run simulation

2. Model Parameter Sharing:
    * Implement asynchronous model parameters (at least, list of numbers and strings) sharing with homomorphic encryption operations on tensors.
    * 

3. Blockchain Component:
    * Create smart contracts to ensure data sharing 
    * [Navigate to Blockchain README](https://github.com/AI-and-Blockchain/F22_Federated_Learning_With_Flexible_Labels/blob/main/Blockchain%20Component/README.md)
