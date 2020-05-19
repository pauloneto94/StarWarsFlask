from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.planet import PlanetModel


class PlanetController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This field cannot be empity")
    parser.add_argument('climate', type=str, required=True, help="This field cannot be empity")
    parser.add_argument('terrain', type=str, required=True, help="This field cannot be empity")

    @jwt_required()
    def get(self, name):
        planet = PlanetModel.find_by_name(name)
        if planet:
            return planet.json()
        return {'message': 'Planet not found'}, 404

    @jwt_required()
    def post(self, name):
        if PlanetModel.find_by_name(name):
            return {'message': 'The {} planet already exists'.format(name)}, 400
        
        data = PlanetController.parser.parse_args()
        planet = PlanetModel(name, data['climate'], data['terrain'])

        try:
            planet.save_to_db()
        except Exception:
            return {'message': 'An error occurred saving the planet'}, 500

        return planet.json(), 201                      

    @jwt_required()
    def delete(self, name):
        planet = PlanetModel.find_by_name(name)
        if not planet:
            return {'message': 'No {} planet exists'.format(name)}

        try:
            planet.delete_from_db()
        except Exception:
            return {'message': 'An error occurred deleting the planet'}, 500


class PlanetListController(Resource):
    @jwt_required()
    def get(self):
        return {'planets': [planet.json() for planet in PlanetModel.query.all()]}                          