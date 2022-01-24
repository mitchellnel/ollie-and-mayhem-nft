// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract OllieAndMayhemNFT is ERC721, VRFConsumerBase {
    // tracking existing NFTs
    uint256 public tokenCounter;
    mapping(uint256 => NFTTraits) public tokenIDtoTraits;
    event traitsAssigned(
        uint256 indexed tokenID,
        Pet pet,
        uint256 imageNumber,
        Colour colour
    );

    // for NFT traits
    struct NFTTraits {
        Pet pet;
        uint256 imageNumber;
        Colour colour;
    }

    enum Pet {
        OLLIE,
        MAYHEM
    }

    enum Colour {
        NORMAL,
        INVERTED
    }

    // translating trait combinations to their respective token URIs

    // for VRFCoordinator
    bytes32 keyhash;
    uint256 fee;

    // for tracking who initiated the request, and thus who is minting
    mapping(bytes32 => address) public requestIDtoSender;
    event requestedNFT(bytes32 indexed requestID, address requester);

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyhash,
        uint256 _fee
    )
        public
        ERC721("OllieAndMayhem", "OllieMayhem")
        VRFConsumerBase(_vrfCoordinator, _linkToken)
    {
        tokenCounter = 0;

        keyhash = _keyhash;
        fee = _fee;
    }

    function createNFT() public returns (bytes32) {
        // get randomness from Chainlink VRF
        bytes32 requestID = requestRandomness(keyhash, fee);
        requestIDtoSender[requestID] = msg.sender;
        emit requestedNFT(requestID, msg.sender);
    }

    function fulfillRandomness(bytes32 requestID, uint256 randomNumber)
        internal
        override
    {
        // get random traits
        Pet pet = Pet(randomNumber % 2);
        uint256 imageNumber = randomNumber % 9; // 9 images for each pet
        Colour colour = Colour(randomNumber % 2);

        NFTTraits memory traits;
        traits.pet = pet;
        traits.imageNumber = imageNumber;
        traits.colour = colour;

        // map tokenID to traits
        uint256 newTokenID = tokenCounter;
        tokenIDtoTraits[newTokenID] = traits;
        emit traitsAssigned(
            newTokenID,
            traits.pet,
            traits.imageNumber,
            traits.colour
        );

        // mint NFT to the requester
        address owner = requestIDtoSender[requestID];
        _safeMint(owner, newTokenID);
        tokenCounter += 1;

        // TODO: Add URI setting code
    }

    function setTokenURI(uint256 tokenID, string memory _tokenURI) internal {
        require(
            _isApprovedOrOwner(_msgSender(), tokenID),
            "ERC721: caller is not owner nor approved."
        );
    }
}
