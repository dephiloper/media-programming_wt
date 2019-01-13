from flask import render_template, Flask, jsonify, request
from sqlalchemy.orm import sessionmaker
from entities import get_engine, Region

Session = sessionmaker(bind=get_engine())
session = Session()

app = Flask(__name__, static_url_path='/static')  # static url only used in development


@app.route('/', methods=['GET'])
def index():
    main_region = session.query(Region).first()
    return render_template('index.html', main_region=main_region)


@app.route('/states', methods=['GET'])
def show_states():
    main_region = session.query(Region).first()
    return jsonify(sub_regions=[i.to_json() for i in main_region.sub_regions])


@app.route('/states/<state>/constituencies', methods=['GET'])
def show_constituencies(state):
    state = session.query(Region).filter(Region.name == state).first()
    return jsonify(constituencies=[i.to_json() for i in state.sub_regions])


app.run()
