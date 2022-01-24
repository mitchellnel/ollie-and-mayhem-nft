import pytest
from brownie import network
from scripts.deploy_and_create_OllieOne import deploy_and_create_ollieOne
from scripts.helpful_scripts import (
    FORKED_LOCAL_ENVIRONMENTS,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
)


def test_can_create_OllieOne():
    if (
        network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() not in FORKED_LOCAL_ENVIRONMENTS
    ):
        pytest.skip("This unit test is only for local testing\n")

    nft = deploy_and_create_ollieOne()

    assert nft.ownerOf(0) == get_account()
