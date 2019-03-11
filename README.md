# Fried Chicken Restaurant

Order fried chicken online and pay it using Tpaga wallet.

### Estimated time:

- Setting up the Django project: 2 hours
- Creating the models: 4 hours
- Creating the views: 2 hours
- Creating the templates: 3 hours
- Tpaga API integration: 2 hours
- Creating a simple Ansible playbook to deploy the Django project: 2 hours

For a total estimated time of 15 hours.


### Run the project
**Create the container:**
```bash
docker-compose build
```
**Run the migrations:**
```bash
docker-compose run web ./manage.py migrate

```
**Run the development server:**
```bash
docker-compose up -d
```

For development it is necessary to create a *secrets.json* file and save it in *fried_chicken/fried_chicken/secrets.json* with the following information:

```json
{
    "TPAGA_USER": "tpaga_user",
    "TPAGA_PASSWORD": "tpaga_password"
}
```

