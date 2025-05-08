const { ethers } = require("hardhat");

async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("Interacting with the contract using account:", deployer.address);

    const contractAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3";
    const NFTStorage = await ethers.getContractAt("NFTStorage", contractAddress);
    const tx = await NFTStorage.createNFT("NFT Metadata #1");
    await tx.wait();
    console.log("NFT created successfully!");

    const nft = await NFTStorage.getNFT(0);
    console.log("Fetched NFT");
    console.log("NFT ID:", nft[0].toString());
    console.log("NFT Metadata:", nft[1]);
    console.log("NFT Owner:", nft[2]);
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error("Interaction failed:", error);
        process.exit(1);
    });