import pytest

from btmonitor.app import hub
from btmonitor.user_registry import UserRegistry


@pytest.fixture()
def user_registry() -> UserRegistry:
    return UserRegistry(hub, 3)


def test_register(user_registry: UserRegistry):
    assert hub.is_suspended()
    assert user_registry.user_count() == 0
    user_registry.add(1)
    assert not hub.is_suspended()
    assert user_registry.user_count() > 0
    assert len(user_registry.users()) == 1
    assert len(user_registry.stats()) == 2
    assert user_registry.stats()[0].count == 0
    assert user_registry.stats()[1].count == 1


def test_unregister(user_registry: UserRegistry):
    user_registry.add(1)
    user_registry.add(2)
    user_registry.remove(1)
    # Max 3 stats keps
    assert len(user_registry.stats()) == 3
    assert user_registry.stats()[0].count == 1
    assert user_registry.stats()[1].count == 2
    assert user_registry.stats()[2].count == 1
    user_registry.remove(2)
    assert len(user_registry.stats()) == 3
    assert hub.is_suspended()
    assert user_registry.user_count() == 0
