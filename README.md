# Linear Programming Solver

Uses google OR tools and Flask to solve linear programming problems.

Deployed to <https://tandyc.pythonanywhere.com/>

## python modules

- [google OR tools](https://developers.google.com/optimization/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/)

## run command

python3 -m waitress --listen=*:80 --call app:create_app
