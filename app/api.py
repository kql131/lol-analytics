from flask import Flask
from flask_restful import Resource, Api 
from flask_sqlalchemy import SQLAlchemy
import click, datetime
from sqlalchemy.dialects.postgresql import JSONB
import requests



app = Flask(__name__) 
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


from app import models, riot


@app.cli.command()
def init_db():
    click.echo('init db')
    meta = db.metadata
    db.drop_all()
    # for table in reversed(meta.sorted_tables):
    #     print ('Clear table %s' % table)
    #     table.delete()
    #     db.session.commit()
    db.create_all()

@app.cli.command('init_data')
def init_data():
    click.echo('generate dummy data')
    


class User(Resource):
    def get(self, name):
        return "user: " + user


class SummonerAPI(Resource):

    def get(self, name):
        app.logger.debug("Summoner API endpoint called")
        name = name.lower()
        summoner = models.Summoner.query.filter(models.Summoner.name == name).first()
        status = {}
        status['summoner_name'] = name
        status['saved_matches'] = 0
        print(summoner)
        if summoner:
            status['exist'] = True
            return status
        else:
            s = riot.get_basic_summoner_info(name)
            s['matches'] = riot.get_matches(s['account_id'], app.config['FETCH_MATCH_COUNT'])
            summoner = models.Summoner(name=s['name'], account_id=int(s['account_id']), id=int(s['summoner_id'])   , level=int(s['level']))
            if 'lp' in s:
                summoner.lp = s['lp']
                summoner.rank = s['rank']

            status['downloaded_matches'] = len(s['matches'])
            for key, value in s['matches'].items():
                try:
                    match_id = int(key)
                    status['saved_matches'] += 1
                    game_time = int(value['match_info']['gameCreation'])
                    iso8650 = datetime.datetime.utcfromtimestamp(game_time/1000).strftime('%Y-%m-%d %H:%M:%S')
                    match = models.Match(id=match_id, datetime=iso8650, info=value['match_info'], timeline=value['timeline'])
                    summoner.matches.append(match)
                except:
                    print(value)
            db.session.merge(summoner)
            db.session.commit()

            return status


api = Api(app)
api.add_resource(SummonerAPI, '/summoner/<string:name>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)