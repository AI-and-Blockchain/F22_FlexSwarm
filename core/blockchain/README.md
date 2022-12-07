# Blockchain component

## Requirement
Before you run the program file, there are couple command you need to install.
- Enable the python virtual environment `python3 -m venv venv` then activate it by `source venv/bin/activate`

```python
pip3 install bigchaindb_driver
pip3 install py-algorand-sdk
pip3 install pyteal
pip3 install dotenv
```

### Main Idea
- [BigchainDB](https://www.bigchaindb.com/) is being used in this project. We use [BigchainDB](https://www.bigchaindb.com/) act as the *database* to store our model data, such as model structure, model parameter, model parameters values and model label
- Using *Algorand Testnet* to build the smart contract code to complete transaction with the client.

### Implementation Details
- Total of **2239** blockchain block used in bigchainDB. 
- Over **2 millions** model data saved into the bigchainDB. 
    - Unable to save them into one block since the data are tooo big
    - Hence, we *separate* th model edata into over 100+ block for each model, and *reconstruct* them after the user provided the specific label [We only query the model data that related to this label ] later.


If you met any error on running any file in this folder, please navigate to [Blockchain Component](https://github.com/AI-and-Blockchain/F22_Federated_Learning_With_Flexible_Labels/tree/main/Blockchain%20Component) to run 

