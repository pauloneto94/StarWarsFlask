from config.db import db
import requests

class PlanetModel(db.Model):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    climate = db.Column(db.String(20))
    terrain = db.Column(db.String(20))
    nMovies = db.Column(db.Integer)

    def __init__(self, name, climate, terrain):
        self.name = name
        self.climate = climate
        self.terrain = terrain
        self.nMovies = self.find_nMovies_by_name(self.name)

    def json(self):
        return {'name': self.name, 'climate': self.climate, 'terrain': self.terrain, 'nMovies': self.nMovies}    

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def find_nMovies_by_name(self, name):
        planetList = requests.get("https://swapi.dev/api/planets/")
        if planetList.status_code == 200:
            for i in range(0, len(planetList.json()['results'])):
                if name == planetList.json()['results'][i]['name']:
                    return len(planetList.json()['results'][i]['films'])
                else:
                    return 0    


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()    