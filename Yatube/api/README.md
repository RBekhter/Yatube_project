# API YaTube
```
Get token:
POST..http://127.0.0.1:8000/api/v1/api-token-auth/
body:
{
    "username": "your_username",
    "password": "your_password"
}
OK: token
```
* Token -> head

## Check, update, create posts

## Query examples:
```
GET..http://127.0.0.1:8000/api/v1/posts/
OK:
[
    {
        "id": 21,
        "author": "dashaa",
        "text": "Пост через Postman",
        "group": "IT",
        "publication_date": "2024-07-30T16:21:27.523654+03:00"
    }
]
```

* GET..http://127.0.0.1:8000/api/v1/posts/7/comments/

```POST..http://127.0.0.1:8000/api/v1/posts/
body:
{
    "text": "Пост через Postman"
}
```