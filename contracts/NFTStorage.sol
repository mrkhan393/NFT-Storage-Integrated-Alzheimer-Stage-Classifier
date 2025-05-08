// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract NFTStorage {
    struct NFT {
        uint256 id;
        string metadata;
        address owner;
    }

    NFT[] public nfts;
    uint256 public nextId;

    function createNFT(string memory metadata) public {
        nfts.push(NFT(nextId, metadata, msg.sender));
        nextId++;
    }

    function getNFT(uint256 id) public view returns (uint256, string memory, address) {
        NFT memory nft = nfts[id];
        return (nft.id, nft.metadata, nft.owner);
    }
}