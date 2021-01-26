# dynamic-dag-assignment

assign IP dynamically to dag configured in panorama


# Running this App


```bash

cd cnc
pip install -r requirements.txt

```

You should now have two top level directories: `src` and `cnc`. 

## Running Pan-CNC

#### 1. Build the database

```bash

./cnc/manage.py migrate

```

#### 2. Create a new user

NOTE: In the below command, change ***email address*** and ***passwd*** to your respective entries .Common practice 
is to have the password be the name of the app, unless specifically spelled out in your documentation.

```bash

./cnc/manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('dag', 'admin@example.com', 'dag')"

```

#### Local Development

You can launch this new app with the following commands:

```bash
cd cnc
celery -A pan_cnc worker --loglevel=info  & 
./manage.py runserver 8080

```

This will start a background task worker and then start the application on port `8080`. You can login using the 
`username` and `password` specified above. 
