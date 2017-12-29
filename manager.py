from flask_script import Manager
from flask_jsglue import JSGlue
from app import application


manager = Manager(application)
jsglue = JSGlue(application)

if __name__ == "__main__":
    manager.run()
