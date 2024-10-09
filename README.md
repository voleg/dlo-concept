# coding-assignment-dlo
Job interview coding assignment "DLO"

This is an app demonstrating Delegated Logon connection from third party to Minddistrict platform.

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

Right after that follow to [app admin page](http://localhost:8000/admin/) and configure *MD DLO connector*, by adding the third party service base url and the shared secret. 

