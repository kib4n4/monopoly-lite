from flask import Flask, render_template, request, redirect, url_for
from board import *
from models import *
from dice import roll_dice, result

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monopoly.db'
app.config['SECRET_KEY'] = 'ultrasecretkey'



def move_player(player, steps):
    player.position = (player.position + steps) % len(board)
    if player.position < steps:
        player.money += 200


@app.route('/')
def home():
    tokens = ['Iron Man', 'Captain America', 'Thor', 'Hulk',
              'Black Widow', 'Hawkeye', 'Spider-Man', 'Captain Marvel']
    return render_template('index.html', tokens=tokens)


@app.route('/select_token', methods=['POST'])
def select_token():
    game_state = GameState.query.filter()
    if not game_state:
        game_state = GameState()
        db.session.add(game_state)
        db.session.commit()

    token = request.form.get('token')
    if token:
        player = Player(name=f'Player {Player.query.count() + 1}', token=token)
        db.session.add(player)
        db.session.commit()
    return redirect(url_for('tokens.html'),token=token)


@app.route('/tokens')
def tokens():
    players = Player.query.all()
    return render_template('tokens.html', players=players)

@app.route('/rooms/<str:room>/>',methods=['GET','POST'])
def rooms(room):
    game_state=GameState.query.filter_by(room)
    if not game_state:
        game_state=GameState(room=room)
        db.session.add(game_state)
        db.session.commit()
        return render_template('player_actions.html',game_state=game_state)

@app.route('/rooms/>',methods=['POST'])
def lobby():
    player=
    game_state=GameState.query.filter_by(room)
    if not game_state:
        game_state=GameState(room=room)
        db.session.add(game_state)
        db.session.commit()
        return render_template('player_actions.html',game_state=game_state)



@app.route('/roll_dice', methods=['POST'])
def roll_dice_route():   
    current_game = GameState.query.first()
    current_player = Player.query.get(current_game.current_player_id)
    result = roll_dice()
    move_player(current_player, result)
    db.session.commit()
    return render_template('dice_result.html', result=result, player=current_player)


@app.route('/end_turn', methods=['POST'])
def end_turn():
    current_game = GameState.query.first()
    current_game.current_player_id = (
        current_game.current_player_id % Player.query.count()) + 1
    db.session.commit()
    return redirect(url_for('roll_dice_route'))


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
