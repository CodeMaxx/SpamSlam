const Gnosis = require('@gnosis.pm/gnosisjs');
const Web3 = require('web3');

const resolutionDate = new Date();
resolutionDate.setDate(resolutionDate.getDate() + 30);

const options = {
  ethereum: new Web3(new Web3.providers.HttpProvider('http://localhost:8545')).currentProvider,
  ipfs: {
    host: 'localhost',
    port: 5001,
    protocol: 'http'
  }
};

const eventDescription = {
    title: 'Spam?',
    description: 'Is the email associated with this market spam or not?',
    resolutionDate: resolutionDate.toISOString(),
    outcomes: ['Yes', 'No'],
};

let gnosisInstance;
let ipfsHash;
let oracle;
let categoricalEvent;
let market;
let accounts;
var fs = require("fs");

Gnosis.create(options)
.then(result => {
    gnosisInstance = result;
    //console.info('[GnosisJS] > connection established');
    //console.info("[GnosisJS] > Creating event description...");
    gnosisInstance.publishEventDescription(eventDescription)
    .then(result => {
      ipfsHash = result;
      //console.info("[GnosisJS] > Event description hash: " + ipfsHash);
      //console.info("[GnosisJS] > Creating Centralized Oracle...");
      gnosisInstance.createCentralizedOracle(ipfsHash)
      .then(result => {
        oracle = result;
        //console.info("[GnosisJS] > Centralized Oracle was created");
        //console.info("[GnosisJS] > Creating Categorical Event...");
        gnosisInstance.createCategoricalEvent({
            collateralToken: gnosisInstance.etherToken,
            oracle,
            // Note the outcomeCount must match the length of the outcomes array published on IPFS
            outcomeCount: 2,
        })
        .then(result => {
          categoricalEvent = result;
          //fs.writeFile( "contract.json", JSON.stringify( categoricalEvent ), "utf8");
          //console.info("[GnosisJS] > Categorical event was created");
          //console.info("[GnosisJS] > Creating market...");
          // console.info(gnosisInstance);
          gnosisInstance.createMarket({
              event: categoricalEvent,
              marketMaker: gnosisInstance.lmsrMarketMaker,
              marketFactory: gnosisInstance.standardMarketFactory,
              fee: 1
          })
          .then(response => {
            market = response;
            //console.info("[GnosisJS] > Market was created");
            Promise.all([
               gnosisInstance.etherToken.deposit({ value: 2e18 }),
               gnosisInstance.etherToken.approve(market.address, 2e18),
            
                //gnosisInstance.setDefaultAccount(gnosisInstance['web3']['eth'].accounts[1]),

                //gnosisInstance.etherToken.deposit({ value: 5e18 }),
                //gnosisInstance.etherToken.approve(market.address, 5e18),

                market.fund(1e18)
            ])
            .then(values => {
              console.info(market["contract"]["address"]);
              //console.info(categoricalEvent);
              //console.info("[GnosisJS] > All done!");
            })
            .catch(error => {
              console.warn(error);
            });
          })
          .catch(error => {
            console.warn(error);
          });

        })
        .catch(error => {
          console.warn(error);
        });

      })
      .catch(error => {
        console.warn(error);
      });
    })
    .catch(error => {
      console.warn(error);
    });

})
.catch(error => {
  console.warn('Make sure that Gnosis Development kit is up and running');
});
