# heimdall
Modular Linux orchestration platform. This is how I'm learning Python; use at your own risk.

## Requirements
Heimdall requires pyyaml:
`pip install pyyaml`

## Configuration
```
server:
    port: 85
    # list of clients allowed to manage this server
    authorized_clients:
        - '127.0.0.1'
    # packages to monitor, grouped by module
    packages:
        apt:
            - '*'
        git:
            - '/opt/heimdall'
            
client:
    # list of hosts to manage
    hosts:
        - 'localhost'
```

## Client Usage
`python client.py <command> [<host> [<module> [<package>]]]`
- command: currently supports `get` or `update`
- host: hostname or address of server (does not need to be specified in config.yaml)
- module: name of module in `./modules` (does not need to be specified in config.yaml)
- package: name of package (does not need to be specified in config.yaml)
### Example: List all packages for all configured hosts
`python client.py get`
### Example: Update php8.0 on localhost via apt
`python client.py update localhost apt php8.0`
