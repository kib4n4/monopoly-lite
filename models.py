from flask_sqlalchemy import SQLAlchemy

# models.py
db = SQLAlchemy()


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    token = db.Column(db.String(50), nullable=False)
    money = db.Column(db.Integer, default=1500)
    position = db.Column(db.Integer, default=0)
    in_jail = db.Column(db.Boolean, default=False)
    get_out_of_jail_free = db.Column(db.Boolean, default=False)
    properties = db.relationship('Property', backref='owner', lazy=True)
    is_computer = db.Column(db.Boolean, default=False)
    game_state_id = db.Column(db.Integer, db.ForeignKey('game_state.id'))


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    rent = db.Column(db.PickleType, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)


class GameState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current_player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    room = db.Column(db.String(50))
    players = db.relationship(
        'Player', backref='game_state', lazy=True, foreign_keys='Player.game_state_id')
