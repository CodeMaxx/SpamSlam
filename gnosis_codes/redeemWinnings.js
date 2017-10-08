const Gnosis = require('@gnosis.pm/gnosisjs');
const Web3 = require('web3');

const options = {
  ethereum: new Web3(new Web3.providers.HttpProvider('http://localhost:8545')).currentProvider,
  ipfs: {
    host: 'localhost',
    port: 5002,
    protocol: 'http'
  }
};

let gnosisInstance;
let ipfsHash;
let oracle;
let categoricalEvent;
let market;
let myJson;

let totalTokens;
let catEvent;
config = {}

Gnosis.create(options)
.then(result => {
    gnosisInstance = result;
    //console.log(gnosisInstance.setDefaultAccount.toString());
    var accounts = gnosisInstance['web3']['eth'].accounts;
    //console.log((gnosisInstance['web3']['eth'].getBalance(accounts[parseInt(process.argv[2])])/1e18).toString());
    
    gnosisInstance.setDefaultAccount(accounts[parseInt(process.argv[3])]);
    gnosisInstance.contracts.CategoricalEvent.at(process.argv[2]).redeemWinnings()
    .then(result=>{
        console.log(result);
    });
    //catEvent = gnosisInstance.contracts.CategoricalEvent;
    //Gnosis.requireEventFromTXResult(await catEvent.redeemWinnings(), 'WinningsRedemption');


})
.catch(error => {
  console.warn('Make sure that Gnosis Development kit is up and running');
});
