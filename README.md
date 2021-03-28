# twitter-clone

# OverView
Created an application similar to Twitter by using Django.


# Usage

1. Build docker containers for running db and sever.
```docker-compose up --build``` 

# URLs

***User function***

POST(create user): ```http://localhost:8000/user/register/```

POST(user login): ```http://localhost:8000/user/login/```

GET(get login user information): ```http://localhost:8000/user/me/```

POST(logout authenticated user): ```http://localhost:8000/user/logout/```


***Tweet function***


POST(post tweet): ```http://localhost:8000/tweet/create/```

GET(get tweet list): ```http://localhost:8000/tweet/list/```

GET(get tweet detail): ```http://localhost:8000/list/<int:tweet_id>```

PUT(update tweet): ```http://localhost:8000/update/<int:tweet_id>```

DELETE(delete tweet): ```http://localhost:8000/delete/<int:tweet_id```

***Chat function***

GET(create new thread with other user): ```http://localhost:8000/chat/<str:username>/```

GET(get created thread list): ```http://localhost:8000/chat/thread/list/```

POST(send message to other user): ```http://localhost:8000/chat/send/<str:username>/```


# What did I implement

* User registration using unique username and a password

* User login (Including session maintenance using any means you're comfortable with) 

* Unit tests for these basic methods

* Chat with other users

* Create, read, update, delete tweet

* Unit/Integration tests for *all* endpoints you've built so far (Basic & Extended Functionality)

# Tech Stack

* Django==3.14

* djangorestframework==3.12.2

* Python==3.9.1

* PostgreSQL

* Docker

* docker-compose





