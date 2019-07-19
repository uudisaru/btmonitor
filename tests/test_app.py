from btmonitor.app import register, hub, USERS, unregister


def test_register():
    assert hub.is_suspended()
    assert len(USERS) == 0
    register(1)
    assert not hub.is_suspended()
    assert len(USERS) > 0


def test_unregister():
    register(1)
    assert not hub.is_suspended()
    assert len(USERS) > 0
    unregister(1)
    assert hub.is_suspended()
    assert len(USERS) == 0
