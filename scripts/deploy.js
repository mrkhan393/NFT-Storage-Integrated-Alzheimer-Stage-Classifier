const { ethers } = require("hardhat");

async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("Deploying contracts with the account:", deployer.address);

    // Compile and deploy the contract
    const NFTStorage = await ethers.getContractFactory("NFTStorage");
    const nftStorage = await NFTStorage.deploy();

    // Wait until the contract is deployed
    await nftStorage.waitForDeployment();

    // Get and print the deployed contract address
    const contractAddress = await nftStorage.getAddress();
    console.log("NFTStorage contract deployed to:", contractAddress);
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error("Deployment failed:", error);
        process.exit(1);
    });
