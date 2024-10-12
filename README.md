# Auth: Delegated logon concept

This is an app demonstrating Delegated Logon connection from third party to DLO enabled platform.

Tooling: 
- Docker
- Python 3.11
- package manager: [UV](https://github.com/astral-sh/uv)
- Django 5, pytest
- ruff

## Run 
### system requerements
- [docker](https://docs.docker.com/get-started/get-docker/)
- optional: [make](https://www.gnu.org/software/make/)

this make you can:

	$ make build 
	$ make run	

without it: 

	$ docker build -t heljetech_dlo:latest .
	$ docker run -p heljetech_dlo:latest


<details>
<summary>you want run localy ?</summary>

*note:* You need [UV](https://github.com/astral-sh/uv) installed for that.
	
	$ uv sunc
	$ uv run manage.py migrate
	$ uv run manage.py collectstatic
	$ uv run manage.py loaddata demo_init.json
	$ uv run pytest
	$ uv run manage.py runserver 0.0.0.0:8000

</details>

than open [app admin](http://localhost:8000/admin)

## Usage

After successfull build and run you should see django migrations runnign, fixtures applied, tests succeed and app stated. 

Right after that follow to [app admin page](http://localhost:8000/admin/) login `login: admin, passwd: 123` and configure [MD DLO connector](http://localhost:8000/admin/minddistrict_connect/platformconfig/add/), by adding the third party service `base_url` and the `shared_secret`.

After that logout from `admin` account and login to one of the users:

credentials of client:
- Username: clara@example.com
- Password: secret
 
credentials of professional:
- Username: peter@example.com
- Password: secret

You will see a simple user profile, with the links to external resources in minddistrict platform. By clicking on then the DLO flow will be executed resulting in generation of URLs, according to [delegated logon specs](https://docs.minddistrict.com/delegatedlogon/index.html).
