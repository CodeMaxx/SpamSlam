
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

Gnosis.create(options)
.then(result => {
    gnosisInstance = result;
    //console.log(gnosisInstance.setDefaultAccount.toString());
    var accounts = gnosisInstance['web3']['eth'].accounts;
    //console.log((gnosisInstance['web3']['eth'].getBalance(accounts[parseInt(process.argv[2])])/1e18).toString());
    gnosisInstance.etherToken.balanceOf(accounts[parseInt(process.argv[2])])
    .then(result=>{
        totalTokens = result;
        var amount = gnosisInstance['web3'].toWei(totalTokens/1e18,"ether");
        gnosisInstance.setDefaultAccount(accounts[parseInt(process.argv[2])]);
        gnosisInstance.etherToken.withdraw(totalTokens)
        .then(result=>{
            //console.log(result);
        })
        .catch(error=>{
            console.warn(error);
        });
    })
    .catch(error=>{
        console.warn(error)
    });

})
.catch(error => {
  console.warn('Make sure that Gnosis Development kit is up and running');
});
