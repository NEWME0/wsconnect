# wsconnect


## Instalation

```pip install -r requirements.txt```


## Startup

```
# Run app with custom settings
uvicorn app:app --ws=websockets
```

Or

```
# Run app with default settings
python -m app
```


## Sender API

```
POST /message/send/ - Send message to specificated channel
{
    "channel": "chat_{user_id}",
    "message": "..."
}


POST /message/push/ - Send message to all channels
{
    "message": "..."
}

```

## Receiver API

```
WS/WSS /channel/websocket/ - Connect websocket
```

## Dashboard API

```
GET /channel/dashboard/ - List of channels with count of active connections
```
