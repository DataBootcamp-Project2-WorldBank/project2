from app.plotlydash.plot_projects import init_projectchart
from app import create_app, db
from app.models import User, Logon

flask_app = create_app()

app = init_projectchart(flask_app)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Logon': Logon}
