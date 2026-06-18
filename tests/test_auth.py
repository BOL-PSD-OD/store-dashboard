from lib import auth

def test_check_password():
    assert auth.check_password("secret", "secret") is True
    assert auth.check_password("secret", "nope") is False
    assert auth.check_password("", "secret") is False
    assert auth.check_password("secret", "") is False

def test_is_expired():
    assert auth.is_expired(last=1000.0, now=1000.0 + 10 * 60, timeout_min=30) is False
    assert auth.is_expired(last=1000.0, now=1000.0 + 31 * 60, timeout_min=30) is True
    assert auth.is_expired(last=None, now=1000.0, timeout_min=30) is True
