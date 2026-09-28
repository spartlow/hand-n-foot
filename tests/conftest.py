import pytest

from context import cardtable


@pytest.fixture(autouse=True)
def reset_cardtable_global_state():
    cardtable.Modifiers.set_meld_method(None)
    cardtable.Modifiers.set_wild_ranks([])
    yield
    cardtable.Modifiers.set_meld_method(None)
    cardtable.Modifiers.set_wild_ranks([])
