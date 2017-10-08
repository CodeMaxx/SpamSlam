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
    var sender = accounts[parseInt(process.argv[2])];
    var receiver = accounts[parseInt(process.argv[3])];
    var amount = gnosisInstance['web3'].toWei(2,"ether");
    //console.log((gnosisInstance['web3']['eth'].getBalance(accounts[0])/1e18).toString());
    // console.log(gnosisInstance['web3']['eth'].getBalance(receiver).toString());
    gnosisInstance['web3']['eth'].sendTransaction({from:sender, to:receiver, value:amount});
    // console.log(gnosisInstance['web3']['eth'].getBalance(sender).toString());
    // console.log(gnosisInstance['web3']['eth'].getBalance(receiver).toString());

    //console.log(gnosisInstance['contracts']['Market']);
    //console.log(gnosisInstance['contracts']['Market'].at(process.argv[2])['buy'].toString());

})
.catch(error => {
  console.warn('Make sure that Gnosis Development kit is up and running');
});
