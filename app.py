from flask import render_template
import config
from models import Person

app = config.connex_app
app.add_api('swagger.yml')

@app.route('/')
def index():
    people = Person.query.all()
    return render_template('index.html', people=people)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)

