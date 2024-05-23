.. _dev_guide:

=========
Dev Guide
=========

This part contains useful information for the developers who wish or are working on RiverApp such as how to generate
documentation or how to add new screens to the app.
This documentation also contain a page for each screen to know how each screen is working.

.. note::

    #. It is suggested to read the screens documentation in the right order to understand how the application works.
    #. It is important to know that the back-end files do not really follow any logic, some functions should have their own file and some classes does not make sens at the moment. That is why this documentation is here to help you understand the code.

.. note::
    The project uses Kivy in the following way: each screen has a python file linked to a Kivy file, the python file contains all the dynamic part of the screen, as well as project data management, and the Kivy file contains the static part of the screen (in some way, the "skeleton" which contains the basic components of the screen).


Coding Standard
===============

- argument naming : ``snake_case``
- attribute naming : ``snake_case``
- constant naming : ``UPPER_CASE``
- class attribute naming : ``snake_case``
- class constant naming : ``UPPER_CASE``
- class naming : ``PascalCase``
- function naming : ``snake_case``

.. note::
    This is a non-exhaustive list of coding standards.

.. note::
    By using ``pylint``, you can test if the standard are respected or not with this line :

    ``pylint --recursive=y riverapp --disable=R0901,W0613,C0114,E0611 --fail-under=7 --class-attribute-naming-style=snake_case``

ADD Screen to App
=================

You have created a new screen and you want to add it to the app. To do this, go through these steps :

1. Add the screen to the ``src/front/screens/__init__.py`` file.

.. code-block:: python

    from .screen_folder.screen_py_file import SCREEN_CLASS

For exemple, if your screen is named ``BABA``, the line you need to add looks like this.

.. code-block:: python

    from .baba.baba import BABA

2. Import the screen in the ``src/riverapp_controller/riverapp_controller.kv`` file.

.. code-block:: console

    #:import SCREEN_CLASS src.front.screens.SCREEN_CLASS

For exemple, if your screen is named ``BABA``, the line you need to add looks like this.

.. code-block:: console

    #:import BABA src.front.screens.BABA

3. Add the screen within the screen list.

.. code-block:: console

    <RiverappController>:
        MDScreenManager:
            id: screen_manager
            DummyScreen:
            SCREEN_CLASS:

For exemple, if your screen is named ``BABA``, the line you need to add looks like this.

.. code-block:: console

    <RiverappController>:
        MDScreenManager:
            id: screen_manager
            DummyScreen:
            BABA:

.. note::
    By doing these steps, your screen is now loaded by the app. It does not mean you can access it, you still have to setup a button or a link somewhere in the app. 
 

BackEnd Calls
=============

Currently, there is no server. Everything in the app is local but sometime, we need to make heavy calculation that most likely takes time.
Those calculations are defined within PY-file in the ``src/back`` folder. To make sure, we don't lock the app until the calculations are done, 
we need to use Thread. 

The best way to do this is shown with the exemple bellow. 

Call exemples
-------------

1. We have a function called ``heavy_calc`` that takes time to complete. To use it within a screen, you need to do it like this:

.. code-block:: python

    from threading import Thread
    from kivymd.uix.screen import MDScreen
    from src.back import heavy_calc

    class MyScreen(MDScreen):

        def do_calculation(self):
            Thread(target=heavy_calc).start()

2. We have a function called ``heavy_calc`` that takes time to complete. Completing it trigger a display change
within the screen :

.. code-block:: python

    from threading import Thread
    from kivy.clock import Clock
    from kivymd.uix.screen import MDScreen
    from src.back import heavy_calc

    class MyScreen(MDScreen):

        def launch_calc(self):
            Thread(target=self.do_calculation).start()

        def do_calculation(self):
            calc = heavy_calc()
            Clock.schedule_once(lambda dt: self.display_calculation(calc))
        
        def display_calculation(self, calc_result):
            # code to display the results

.. note::
    The code displayed is not optimal and can be clearly improved but it is the same as the code used in the project for this case.

Call summary
------------

- Use ``Thread`` to execute long and heavy code. **EVEN** if you need to do it before displaying something on the screen. Not doing this will freeze the app utile the code is done which is a bad user experience.
- Use ``Clock`` from kivy.clock (ClockDoc_) to display something comming from a Thread. By doing this, you let kivy synchronise nicely and avoid freeze or conclit within the main app Thread.

Documentation
=============

By default, dependencies and tools to generate documentation are not installed with RiverApp dependencies. 
It works like this because they are not needed to work on the project and it makes it easier to automate documentation deployment. 

Dependencies installation
-------------------------

Setup the environment with all dependencies as follows : 

.. code-block:: console

    $ pip install -r docs/requirements.txt

.. note::
    You can install these dependencies in the RiverApp environment without any problem. 
    You don't need to maintain 2 separate environments for everything to work.


Create documentation
--------------------

TODO

Generate HTML-files documentation
---------------------------------

To generate the HTML-files, go through these steps:

.. code-block:: console

    $ cd docs
    $ make html

In case of Windows does not recognise the command, go through these steps:

.. code-block:: console

    $ cd docs
    $ ./make html

.. note:: 
    The files can be found and viewed within the ``docs/build`` folder 

.. _ClockDoc : https://kivy.org/doc/stable/api-kivy.clock.html

.. toctree::
   :hidden:
   :caption: Dev guide contents:

   api
   gitlab_runner
   projects_management
   project_details
   video_configuration
   bathymetry_configuration
   beacons_configuration
   filters_configuration
   piv_analysis
   transect_and_discharge
   back_files




