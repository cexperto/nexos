
# nexos

project challenge for nexos

clone this repo, config a postgresql database and reemplace credentials in settings.py file

option:
For do more easy process execute:

./cli

for use the storage for azure follow the instructions in 
uploader\views.py

## API Reference


#### insert data in DB

```http
  post /upload/
  http://localhost:8000/upload/
```
use MultipartForm and select csv file, just csv is allowed, use MOCK_DATA.csv file from this repo for example.

#### Get all items

```http
  GET /querys/
  http://localhost:8000/querys/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `querys` | `string` | **Required**. |


## Authors

- [@cexperto](https://github.com/cexperto)



