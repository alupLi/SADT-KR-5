# Контрольная работа №5. Технологии разработки серверных приложений

## Общие требования

- Python 3.12 или выше
- Docker Desktop (для Задания 2)

---

## Задание 1

### Установка и запуск

```bash
cd 1
python -m venv .venv

# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### Запуск тестов

```bash
pytest tests/test_tasks.py -v
```

### Ожидаемый результат

```
=========================== test session starts ===========================
platform win32 -- Python 3.12.10, pytest-8.3.4, pluggy-1.6.0 -- C:\ПУТЬ\SADT-KR-5\1\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\ПУТЬ\SADT-KR-5\1
plugins: anyio-4.13.0
collected 9 items

tests/test_tasks.py::test_create_task_success PASSED                 [ 11%]
tests/test_tasks.py::test_create_task_title_too_short PASSED         [ 22%]
tests/test_tasks.py::test_create_task_no_user_id PASSED              [ 33%]
tests/test_tasks.py::test_user_sees_only_own_tasks PASSED            [ 44%]
tests/test_tasks.py::test_filter_by_status_and_priority PASSED       [ 55%]
tests/test_tasks.py::test_update_task_status_success PASSED          [ 66%]
tests/test_tasks.py::test_get_foreign_task_returns_404 PASSED        [ 77%]
tests/test_tasks.py::test_get_nonexistent_task_returns_404 PASSED    [ 88%]
tests/test_tasks.py::test_delete_task_success PASSED                 [100%]

============================ 9 passed in 0.71s ============================
```

---

## Задание 2

### Установка и запуск через Docker

```bash
cd 2
docker compose up --build
```

### Запуск тестов

```bash
cd 2
python -m venv .venv

# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate

pip install -r requirements.txt

pytest tests/ -v
```

### Ожидаемый результат

```bash
=========================== test session starts ===========================
platform win32 -- Python 3.12.10, pytest-8.3.4, pluggy-1.6.0 -- C:\ПУТЬ\SADT-KR-5\2\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\ПУТЬ\SADT-KR-5\2
plugins: anyio-4.13.0
collected 10 items

tests/test_tasks.py::test_create_task_success PASSED                 [ 10%]
tests/test_tasks.py::test_create_task_title_too_short PASSED         [ 20%]
tests/test_tasks.py::test_create_task_no_user_id PASSED              [ 30%]
tests/test_tasks.py::test_user_sees_only_own_tasks PASSED            [ 40%]
tests/test_tasks.py::test_filter_by_status_and_priority PASSED       [ 50%]
tests/test_tasks.py::test_update_task_status_success PASSED          [ 60%]
tests/test_tasks.py::test_get_foreign_task_returns_404 PASSED        [ 70%]
tests/test_tasks.py::test_get_nonexistent_task_returns_404 PASSED    [ 80%]
tests/test_tasks.py::test_delete_task_success PASSED                 [ 90%]
tests/test_tasks.py::test_health_endpoint PASSED                     [100%]

=========================== 10 passed in 0.70s ============================
```

### Примеры запросов

```bash
curl http://localhost:8000/health
{"status":"ok"}

curl "http://localhost:8000/tasks/" -H "X-User-Id: 10"

curl -X POST http://localhost:8000/tasks/ -H "Content-Type: application/json" -H "X-User-Id: 10" -d "{\"title\": \"Docker task\", \"status\": \"todo\", \"priority\": 3}"
{"id":1,"title":"Docker task","description":null,"status":"todo","priority":3,"owner_id":10}

curl "http://localhost:8000/tasks/" -H "X-User-Id: 10"
[{"id":1,"title":"Docker task","description":null,"status":"todo","priority":3,"owner_id":10}]
```

### Ожидаемые логи сервера

```bash
time="2026-05-20T13:33:14+03:00" level=warning msg="C:\\ПУТЬ\\SADT-KR-5\\2\\docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
[+] up 2/2
 ✔ Network 2_default Created                                            0.0s
 ✔ Container 2-api-1 Created                                            0.1s
Attaching to api-1
api-1  | INFO:     Started server process [1]
api-1  | INFO:     Waiting for application startup.
api-1  | INFO:     Application startup complete.
api-1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
api-1  | INFO:     172.19.0.1:46792 - "GET /health HTTP/1.1" 200 OK
api-1  | INFO:     172.19.0.1:56494 - "GET /tasks/ HTTP/1.1" 200 OK
api-1  | INFO:     172.19.0.1:37638 - "POST /tasks/ HTTP/1.1" 201 Created
api-1  | INFO:     172.19.0.1:33046 - "GET /tasks/ HTTP/1.1" 200 OK
```

### Остановка

```bash
cd 2
docker compose down
```

---

## Задание 3

### Установка и запуск

```bash
cd 3
python -m venv .venv

# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### Запуск тестов

```bash
pytest tests/test_websocket.py -v
```

### Ожидаемые результаты тестов

```
=========================== test session starts ===========================
platform win32 -- Python 3.12.10, pytest-8.3.4, pluggy-1.6.0 -- C:\ПУТЬ\SADT-KR-5\3\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\ПУТЬ\SADT-KR-5\3
plugins: anyio-4.13.0
collected 10 items

tests/test_websocket.py::test_connect_with_valid_username PASSED     [ 10%]
tests/test_websocket.py::test_connect_without_username PASSED        [ 20%]
tests/test_websocket.py::test_connect_with_empty_username PASSED     [ 30%]
tests/test_websocket.py::test_connect_with_spaces_only PASSED        [ 40%]
tests/test_websocket.py::test_send_and_receive_message PASSED        [ 50%]
tests/test_websocket.py::test_two_clients_same_room_receive_message PASSED [ 60%]
tests/test_websocket.py::test_different_rooms_dont_share_messages PASSED [ 70%]
tests/test_websocket.py::test_message_too_long_returns_error PASSED  [ 80%]
tests/test_websocket.py::test_disconnect_removes_user PASSED         [ 90%]
tests/test_websocket.py::test_get_users_in_room PASSED               [100%]

=========================== 10 passed in 0.66s ============================
```

---

## Задание 4

### Установка и запуск

```bash
cd 4
python -m venv .venv

# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### Запуск тестов

```bash
pytest tests/ -v
```

### Ожидаемые результаты тестов

```
=========================== test session starts ===========================
platform win32 -- Python 3.12.10, pytest-8.3.4, pluggy-1.6.0 -- C:\ПУТЬ\SADT-KR-5\4\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\ПУТЬ\SADT-KR-5\4
plugins: anyio-4.13.0
collected 16 items

tests/test_dependencies_and_routing.py::test_users_me_returns_current_user PASSED [  6%]
tests/test_dependencies_and_routing.py::test_no_x_user_id_returns_401 PASSED [ 12%]
tests/test_dependencies_and_routing.py::test_regular_user_cannot_access_admin_stats PASSED [ 18%]
tests/test_dependencies_and_routing.py::test_admin_can_access_stats PASSED [ 25%]
tests/test_dependencies_and_routing.py::test_regular_user_cannot_delete_others_task PASSED [ 31%]
tests/test_dependencies_and_routing.py::test_admin_can_delete_any_task_via_admin_endpoint PASSED [ 37%]
tests/test_dependencies_and_routing.py::test_admin_cannot_delete_nonexistent_task PASSED [ 43%]
tests/test_tasks.py::test_create_task_success PASSED                 [ 50%]
tests/test_tasks.py::test_create_task_title_too_short PASSED         [ 56%]
tests/test_tasks.py::test_create_task_no_user_id PASSED              [ 62%]
tests/test_tasks.py::test_user_sees_only_own_tasks PASSED            [ 68%]
tests/test_tasks.py::test_filter_by_status_and_priority PASSED       [ 75%]
tests/test_tasks.py::test_update_task_status_success PASSED          [ 81%]
tests/test_tasks.py::test_get_foreign_task_returns_404 PASSED        [ 87%]
tests/test_tasks.py::test_get_nonexistent_task_returns_404 PASSED    [ 93%]
tests/test_tasks.py::test_delete_task_success PASSED                 [100%]

=========================== 16 passed in 0.77s ============================
```

---