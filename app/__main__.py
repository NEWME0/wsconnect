import uvicorn


default = {
    'app': 'app:app',
    'host': '0.0.0.0',
    'port': 8000,
    'ws': 'websockets'
}


if __name__ == '__main__':
    uvicorn.run(**default)
