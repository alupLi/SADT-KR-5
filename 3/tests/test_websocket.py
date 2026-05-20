import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocketDisconnect
from app.main import app
from app.room_manager import room_manager


@pytest.fixture
def client():
    room_manager.rooms.clear()
    return TestClient(app)


def test_connect_with_valid_username(client):
    with client.websocket_connect("/ws/rooms/python?username=alice") as websocket:
        # Сначала приходит system-сообщение о входе
        system_msg = websocket.receive_json()
        assert system_msg["type"] == "system"
        assert "joined" in system_msg["text"]


def test_connect_without_username(client):
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/ws/rooms/python"):
            pass


def test_connect_with_empty_username(client):
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/ws/rooms/python?username="):
            pass


def test_connect_with_spaces_only(client):
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/ws/rooms/python?username=   "):
            pass


def test_send_and_receive_message(client):
    with client.websocket_connect("/ws/rooms/python?username=alice") as websocket:
        # Пропускаем system-сообщение о входе
        websocket.receive_json()
        
        websocket.send_json({"type": "message", "text": "Hello everyone!"})
        response = websocket.receive_json()
        assert response["type"] == "message"
        assert response["text"] == "Hello everyone!"
        assert response["username"] == "alice"
        assert response["room_id"] == "python"


def test_two_clients_same_room_receive_message(client):
    with client.websocket_connect("/ws/rooms/python?username=alice") as websocket1:
        # Пропускаем system-сообщение о входе alice
        websocket1.receive_json()
        
        with client.websocket_connect("/ws/rooms/python?username=bob") as websocket2:
            # Пропускаем system-сообщение о входе bob (получают оба клиента)
            websocket1.receive_json()
            websocket2.receive_json()
            
            websocket1.send_json({"type": "message", "text": "Hi Bob!"})
            
            # Оба клиента должны получить сообщение
            response1 = websocket1.receive_json()
            response2 = websocket2.receive_json()
            
            assert response1["text"] == "Hi Bob!"
            assert response2["text"] == "Hi Bob!"
            assert response1["username"] == "alice"
            assert response2["username"] == "alice"


def test_different_rooms_dont_share_messages(client):
    with client.websocket_connect("/ws/rooms/python?username=alice") as websocket1:
        websocket1.receive_json()  # Пропускаем system-сообщение
        
        with client.websocket_connect("/ws/rooms/java?username=bob") as websocket2:
            websocket2.receive_json()  # Пропускаем system-сообщение
            
            websocket1.send_json({"type": "message", "text": "Only Python room"})
            
            response1 = websocket1.receive_json()
            assert response1["text"] == "Only Python room"
            
            # Второй клиент не должен получить сообщение
            with pytest.raises(Exception):
                websocket2.receive_json(timeout=1)


def test_message_too_long_returns_error(client):
    with client.websocket_connect("/ws/rooms/python?username=alice") as websocket:
        # Пропускаем system-сообщение о входе
        websocket.receive_json()
        
        long_text = "a" * 301
        websocket.send_json({"type": "message", "text": long_text})
        response = websocket.receive_json()
        assert response["type"] == "error"
        assert "too long" in response["detail"].lower()


def test_disconnect_removes_user(client):
    with client.websocket_connect("/ws/rooms/python?username=alice") as websocket:
        websocket.receive_json()  # Пропускаем system-сообщение
        pass  # Соединение закрывается
    
    response = client.get("/rooms/python/users")
    assert response.status_code == 200
    assert response.json()["users"] == []


def test_get_users_in_room(client):
    with client.websocket_connect("/ws/rooms/python?username=alice") as websocket1:
        websocket1.receive_json()
        
        with client.websocket_connect("/ws/rooms/python?username=bob") as websocket2:
            websocket2.receive_json()
            
            response = client.get("/rooms/python/users")
            assert response.status_code == 200
            users = response.json()["users"]
            assert "alice" in users
            assert "bob" in users
            assert len(users) == 2