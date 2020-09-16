# SETUP
```sh
sudo pip install -r requirements.txt
```

# RUN SERVER
```sh
./run.sh
```

# API

```sh
[GET] /devices
```
Get all devices
RESPONSE:
```json
{
    "hum": 30,
    "temp1": 26,
    "pressure": 1000,
    "temp2": 26.5,
    "accel1": 9.8,
    "Gaxis": 12,
    "accel2": 2.34,
    "magneto": 11,
    "relay1": 1,
    "relay2": 0,
    "relay3": 0,
    "relay4": 0
}
```

```sh
[POST] /devices
```
Set one/many devices
SEND:
```json
{
    "hum": 30,
    "temp1": 26,
    "pressure": 1000,
    "temp2": 26.5,
    "accel1": 9.8,
    "Gaxis": 12,
    "accel2": 2.34,
    "magneto": 11,
    "relay1": 1,
    "relay2": 0,
    "relay3": 0,
    "relay4": 0
}
```

