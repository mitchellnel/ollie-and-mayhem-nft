from brownie import accounts, config, network, Contract
from brownie import LinkToken, VRFCoordinatorMock
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]

OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

CONTRACT_TO_MOCK = {"vrf_coordinator": VRFCoordinatorMock, "link_token": LinkToken}

PET_MAPPING = {0: "OLLIE", 1: "MAYEHM"}
COLOUR_MAPPING = {0: "NORMAL", 1: "INV"}


def get_account(index=None, id=None):
    if index is not None:
        return accounts[index]
    elif id is not None:
        return accounts.load(id)
    elif (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def get_contract(contract_name):
    """Returns the contract address from the Brownie config if it is defined.
    Otherwise, it will deploy a mock version of the contract, and return the
        mock contract.

    Keyword arguments:
    - contract_name -- the name of the contract that we are looking to interact with

    Returns:
    a brownie.network.contract.ProjectContract object, which is the most recently
        deployed Contract of the type specified by the dictionary. This could either
        be a mock contract or a real contract deployed on a live network.
    """
    contract_type = CONTRACT_TO_MOCK[contract_name]

    # do we need to deploy a mock?
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        # use address and ABI to create contract object
        contract_address = config["networks"][network.show_active()][contract_name]

        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )

    return contract


def deploy_mocks():
    """Deploys mock contracts to a testnet."""
    account = get_account()
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks...")

    print("... Deploying Mock LinkToken ...")
    link_token = LinkToken.deploy({"from": account})
    print(f"... LinkToken deployed to {link_token.address} ...")

    print(" ... Deploying Mock VRFCoordinator ...")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print(f"... VRFCoordinator deployed to {vrf_coordinator.address} ...")

    print(f"... Done! All mocks deployed.\n")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=Web3.toWei(1, "ether")
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")

    print(f"Funding {contract_address} with {amount} LINK ...")
    fund_txn = link_token.transfer(contract_address, amount, {"from": account})
    fund_txn.wait(1)
    print("... Done!\n")

    return fund_txn
