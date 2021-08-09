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
            - 'php*'
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
```
# python client.py get
localhost git https://github.com/willregelmann/heimdall.git (f9cb5deaf8b971ad385427b4a456cbfba7024c14 => b87c655f609a70806a666c7c436ed26d898064a2)
localhost apt php-common (2:84+0~20210621.36+debian10~1.gbp28513e)
localhost apt php8.0-cli (8.0.9-1+0~20210730.22+debian10~1.gbp99e7e9)
localhost apt php8.0-common (8.0.9-1+0~20210730.22+debian10~1.gbp99e7e9)
localhost apt php8.0-curl (8.0.9-1+0~20210730.22+debian10~1.gbp99e7e9)
```
### Example: Update php8.0 on localhost via apt
`python client.py update localhost apt php8.0`
