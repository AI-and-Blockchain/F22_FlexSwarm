## Blockchain component

### Main Idea
- [BigchainDB](https://www.bigchaindb.com/) is being used in this project. We use [BigchainDB](https://www.bigchaindb.com/) act as the database to store our model data, such as model structure, model parameter, model parameters values and model label

### Details
- Total 2239 transaction block used. 
- Over 2 millions data stored. 
- Unable to save them into one block since the data are tooo big, hence, we separate the data into over 100+ block for one model, and reconstruct them later. 