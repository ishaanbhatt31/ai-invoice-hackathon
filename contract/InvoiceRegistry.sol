// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract InvoiceRegistry {
    mapping(string => address) public invoiceIssuers;
    event HashStored(string indexed invoiceHash, address indexed issuer);

    function storeHash(string memory _hash) public {
        require(invoiceIssuers[_hash] == address(0), "Hash already stored");
        invoiceIssuers[_hash] = msg.sender;
        emit HashStored(_hash, msg.sender);
    }
}
