# ruff: noqa: S101
from unittest.mock import patch

import pytest

from minddistrict_connect.dlo import DLOAdapter, build_hmac_token


# Mock UUID for predictability
@pytest.fixture
def mock_uuid():
    return '123e4567-e89b-12d3-a456-426614174000'

@pytest.fixture
def secret_key():
    return 'THE_SECRET_KEY'

@pytest.fixture
def base_url():
    return 'https://example.com'


# Test HMAC token generation
def test_build_hmac_token(secret_key):
    message = 'testmessage'
    # Check if the token generation is successful
    token = build_hmac_token(secret_key, message)
    assert isinstance(token, str) and len(token) > 0


# Test DLOAdapter initialization
def test_dlo_adapter_init(secret_key, base_url):
    adapter = DLOAdapter(secret_key, base_url, 'client', 'client-1')
    assert adapter.secret_key == secret_key
    assert adapter.base_url == base_url
    assert adapter.usertype == 'client'
    assert adapter.userid == 'client-1'


# Test nonce generation
@patch('uuid.uuid4', return_value='123e4567-e89b-12d3-a456-426614174000')
def test_get_nonce(mock_uuid, secret_key, base_url):
    adapter = DLOAdapter(secret_key, base_url, 'client', 'client-1')
    assert adapter.get_nonce() == mock_uuid()


# Test parameter construction (without checking timestamp)
@patch('uuid.uuid4', return_value='123e4567-e89b-12d3-a456-426614174000')
def test_get_params(mock_uuid, secret_key, base_url):
    adapter = DLOAdapter(secret_key, base_url, 'client', 'client-1')
    params = adapter.get_params()

    # Remove timestamp from the comparison
    assert params['nonce'] == mock_uuid()
    assert params['userid'] == 'client-1'
    assert params['usertype'] == 'client'


# Test message building with sorted params
def test_build_message(secret_key, base_url):
    adapter = DLOAdapter(secret_key, base_url, 'client', 'client-1')
    params = {
        'nonce': '123e4567-e89b-12d3-a456-426614174000',
        'userid': 'client-1',
        'usertype': 'client'
    }
    expected_message = 'nonce123e4567-e89b-12d3-a456-426614174000useridclient-1usertypeclient'
    assert adapter.build_message(**params) == expected_message


# Test URL building without redirect (ignoring token)
@patch('uuid.uuid4', return_value='123e4567-e89b-12d3-a456-426614174000')
def test_build_url(mock_uuid, secret_key, base_url):
    adapter = DLOAdapter(secret_key, base_url, 'client', 'client-1')

    url = adapter.build_url()

    # Check that the base part of the URL is correct
    assert url.startswith('https://example.com/?')

    # Check that required parameters are in the URL
    assert 'nonce=123e4567-e89b-12d3-a456-426614174000' in url
    assert 'userid=client-1' in url
    assert 'usertype=client' in url

    # Ensure the token is present (without checking its exact value)
    assert 'token=' in url


# Test URL building with redirect (ignoring token)
@patch('uuid.uuid4', return_value='123e4567-e89b-12d3-a456-426614174000')
def test_build_url_with_redirect(mock_uuid, secret_key, base_url):
    adapter = DLOAdapter(secret_key, base_url, 'client', 'client-1')

    redirect = '/dashboard'

    url = adapter.build_url(redirect=redirect)

    # Check that the base part of the URL is correct
    assert url.startswith('https://example.com/aux/frameredirect')

    # Check that required parameters are in the URL
    assert 'nonce=123e4567-e89b-12d3-a456-426614174000' in url
    assert 'userid=client-1' in url
    assert 'usertype=client' in url
    assert 'redirect=%2Fdashboard' in url

    # Ensure the token is present (without checking its exact value)
    assert 'token=' in url
