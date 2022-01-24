from pathlib import Path
import os, requests, json

from brownie import network
from brownie import OllieAndMayhemNFT
from scripts.helpful_scripts import get_colour, get_pet
from metadata.metadata_resources import IMAGE_NUMBER_TO_DESCRIPTION, METADATA_TEMPLATE


def create_metadata():
    nft = OllieAndMayhemNFT[-1]

    number_of_NFTs = nft.tokenCounter()

    print(f"You have created {number_of_NFTs} NFTs.")

    for token_id in range(0, number_of_NFTs):
        nft_traits = nft.tokenIDtoTraits(token_id)  # returns a tuple

        pet = get_pet(nft_traits[0])
        image_number = nft_traits[1]
        colour = (
            "_" + get_colour(nft_traits[2])
            if get_colour(nft_traits[2]) == "INVERTED"
            else ""
        )

        image_file_path = f"./img/{pet}{image_number}{colour}.jpg".lower()
        metadata_file_path = f"./metadata/{network.show_active()}/{token_id}-{pet}{image_number}{colour}.json".lower()
        nft_metadata = METADATA_TEMPLATE

        if Path(metadata_file_path).exists():
            print(f"{metadata_file_path} already exists! Delete it to overwrite!\n")
        else:
            print(f"Creating metadata file: {metadata_file_path} ...")
            nft_metadata["name"] = f"{pet.capitalize()} {image_number}"
            nft_metadata["description"] = IMAGE_NUMBER_TO_DESCRIPTION[pet][image_number]

            image_uri = upload_to_pinata(image_file_path)
            nft_metadata["image"] = image_uri

            nft_metadata["attributes"] = (
                [{"trait_type": "Inverted Colour", "value": 3}]
                if get_colour(nft_traits[2]) == "INVERTED"
                else []
            )

            with open(metadata_file_path, "w") as file:
                json.dump(nft_metadata, file)

            json_uri = upload_to_pinata(metadata_file_path)

            return json_uri


def upload_to_ipfs(filepath):
    """Uploads filepath to our local IPFS node."""
    with Path(filepath).open("rb") as fp:
        file_binary = fp.read()

        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"

        filename = filepath.split("/")[-1:][0]  # "./img/mayhem1.jpg"--> "mayhem1.jpg"

        print(f"Posting {filename} to IPFS ...")
        response = requests.post(ipfs_url + endpoint, files={"file": file_binary})
        ipfs_hash = response.json()["Hash"]

        uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        # https://ipfs.io/ipfs/QmdtiV1A26mSrNmPzbSKGpcPiHtLaTQmavpr5YXpwdwHck?filename=mayhem8_inverted.jpg
        print(f"... Done! File is available at {uri}\n")

        return uri


def upload_to_pinata(filepath, already_posted_to_ipfs=True):
    """Uploads filepath to Pinata, who will pin it to a IPFS node, allowing us to
    access our URIs even when our local node is not running.
    """
    if not already_posted_to_ipfs:
        upload_to_ipfs(filepath)

    with Path(filepath).open("rb") as fp:
        file_binary = fp.read()

        pinata_url = "https://api.pinata.cloud"
        endpoint = "/pinning/pinFileToIPFS"
        headers = {
            "pinata_api_key": os.getenv("PINATA_API_KEY"),
            "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
        }

        filename = filepath.split("/")[-1:][0]  # "./img/mayhem1.jpg"--> "mayhem1.jpg"

        print(f"Posting {filename} to Pinata ...")
        response = requests.post(
            pinata_url + endpoint,
            files={"file": (filename, file_binary)},
            headers=headers,
        )

        ipfs_hash = response.json()["IpfsHash"]

        uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(f"... Done! File is available at {uri}\n")

        return uri


def main():
    create_metadata()
