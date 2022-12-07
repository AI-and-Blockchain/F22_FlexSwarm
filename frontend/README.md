## Set up
npm version: 9.1.3
node version: 18.0.0

To meet npm and node version requirements, the current best solution is installing `nvm` (Node Version Manager), refer to this page for more information `https://github.com/nvm-sh/nvm#installing-and-updating`

`nvm install 18.0.0 && nvm use 18.0.0`

## Usage
Navigate to frontend folder, run
`npm install`

Then, `npm start`

Port set to `localhost:3000`, proxy set to `localhost:8888` which is the backend API port, find in `backend/wsgi.py`



