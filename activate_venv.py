import os

venv = os.path.join(os.path.dirname(__file__), 'venv')

if not os.path.isdir(venv):
    raise RuntimeError(f'Virtualenv not initialized in {venv}. Please execute "init_venv.bash".')


activate_this = f'{venv}/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
