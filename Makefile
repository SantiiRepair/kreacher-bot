# create virtual enviroment ro run the bot
create_env:
	virtualenv kreacher_env

# install deps required to run this project
install:
	pip3 install --no-deps -U pytgcalls==3.0.0.dev24 tgcalls==3.0.0.dev6 && pip3 install -r requirements.txt

# format files in the project
format:
	black . --line-length 79

# generate string session of your telegram account
gen_session:
	python3 ./session/session.py

# lint all project looking for issues
lint:
	pylint --disable=C0301,C0103 --recursive yes --jobs=4 .

# command to run bot in normal mode
run_bot:
	python3 -m bot

# command to run bot in virtual enviroment
run_bot_virtual_env:
	make create_env && make install && source kreacher_env/bin/activate && bash python3 -m kreacher

