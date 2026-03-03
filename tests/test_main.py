from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Welcome to the Chatbot API"}

def test_chat_with_bot_success(mocker):
    # Mock the OpenAI API call to avoid actual costs and dependencies
    mocker.patch(
        "openai.ChatCompletion.create",
        return_value={
            "choices": [{
                "message": {
                    "content": "This is a mocked response."
                }
            }]
        }
    )

    # Mock Redis client to simulate cache miss then cache set
    mock_redis = mocker.Mock()
    mock_redis.get.return_value = None # Cache miss
    mocker.patch("app.main.redis_client", mock_redis)

    response = client.post("/chat/", json={"user_input": "Hello"})
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["bot_response"] == "This is a mocked response."
    assert json_response["source"] == "model"
    mock_redis.get.assert_called_once_with("Hello")
    mock_redis.setex.assert_called_once_with("Hello", 3600, "This is a mocked response.")

def test_chat_with_bot_cache_hit(mocker):
    # Mock Redis client to simulate a cache hit
    mock_redis = mocker.Mock()
    mock_redis.get.return_value = b"This is a cached response." # Cache hit
    mocker.patch("app.main.redis_client", mock_redis)

    # Mock the OpenAI API call to ensure it is NOT called
    mock_openai_create = mocker.patch("openai.ChatCompletion.create")

    response = client.post("/chat/", json={"user_input": "Hi again"})
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["bot_response"] == "This is a cached response."
    assert json_response["source"] == "cache"
    mock_redis.get.assert_called_once_with("Hi again")
    mock_openai_create.assert_not_called()
