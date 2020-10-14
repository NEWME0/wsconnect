# WSConnect


## Installation

```
pip install -r requirements.txt
```


## Run

Run app with default settings
```
python -m app
```

Or run app with custom settings
```
uvicorn app:app --ws=websockets [<custom-settings>]
```

> Note!<br>
> By default `uvicorn` doesn't handle `WS|WSS` protocols used by websockets.<br>
> We need to specify module that will be used for `WS|WSS` protocols with argument<br>
> `--ws=websockets` where `websockets` is python module.


## API

#### Documentation API

Swagger
```
GET /docs
```

Redoc
```
GET /redoc
```

OpenAPI json schema
```
GET /openapi.json
```

#### Sender API

Send message to specific channel
```
POST /message/send/
{
    "channel": "chat_{user_id}",
    "message": "..."
}
```

Send message to all channels
```
POST /message/push/
{
    "message": "..."
}
```

#### Receiver API

Connect websocket
```
WS /channel/websocket/
{
    "token": "<user-token>"
}
```

#### Dashboard API

List of channels with count of active connections
```
GET /channel/dashboard/
```
