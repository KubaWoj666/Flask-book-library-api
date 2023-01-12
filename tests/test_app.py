from  flask import Flask

def test_app(app):
    assert isinstance(app, Flask)
    assert app.config['TESTING'] == True
    assert app.config['DEBUG'] == True