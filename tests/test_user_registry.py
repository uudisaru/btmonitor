from btmonitor.app import hub
from btmonitor.user_registry import UserRegistry

import pytest


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
    stats = user_registry.stats()
    assert len(stats) == 3
    assert stats[0].data == 0
    assert stats[1].data == 1


def test_unregister(user_registry: UserRegistry):
    user_registry.add(1)
    user_registry.add(2)
    user_registry.remove(1)
    # Max 3 stats kept (4 with copy of the last counter)
    stats = user_registry.stats()
    assert len(stats) == 4
    assert stats[0].data == 1
    assert stats[1].data == 2
    assert stats[2].data == 1
    # Last counter is a copy of previous
    assert stats[3].data == 1
    user_registry.remove(2)
    assert len(user_registry.stats()) == 4
    assert hub.is_suspended()
    assert user_registry.user_count() == 0
