from flask import Flask, request
from flask_json import FlaskJSON, as_json
from .optimize_route import optimize_route

app = Flask(__name__)
FlaskJSON(app)

@app.route('/simulate_individual_influence', methods=['POST'])
@as_json
def individual_influence_simulate():

    config = request.get_json(force=True)

    ret = optimize_route(config)

    return {ret}

