# Slowly stamps tracker :mailbox_with_mail:

Do you like sending new stamps to your penpals when using [Slowly](https://slowly.app/en/)?

Is it also difficult for you to keep track of which stamps you have already sent to your pal when you have been having conversation for months? :dizzy_face:

Well, this small and simple **Flask** app is perfect to help you keep track of which stamps you have sent to which of your pals.

* :point_right: **Production** Environment (recommended) :
  * Requires [Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/) to be installed first.
  * `docker-compose up`
* :technologist: **Development** Environment :
  * `cd myapp`
  * `pip install -r requirements.txt`
  * `python wsgi.py`

Access frontend from here after doing one of the above : `http://localhost:5000`


Get all stamp images from [here](https://slowly.fandom.com/wiki/List_of_stamps_on_Slowly)

How to get user images? Simple! Open the slowly [web_app](https://web.getslowly.com/), click on the user and right-click save image!

All your data is being stored locallly in the `resources` directory. Remember to keep it safe!

Have fun! :grin:

Made with :heart: using :snake:
