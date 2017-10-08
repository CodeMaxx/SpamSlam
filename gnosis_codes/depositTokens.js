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

Gnosis.create(options)
.then(result => {
    gnosisInstance = result;
    //console.log(gnosisInstance.setDefaultAccount.toString());
    var accounts = gnosisInstance['web3']['eth'].accounts;

    gnosisInstance.setDefaultAccount(accounts[parseInt(process.argv[3])]);
    gnosisInstance.etherToken.deposit({ value: 2e18 });
    gnosisInstance.etherToken.approve(process.argv[2], 2e18);

})
.catch(error => {
  console.warn('Make sure that Gnosis Development kit is up and running');
});
