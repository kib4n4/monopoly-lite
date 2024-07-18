import random
import uuid
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
    token = request.form.get('token')
    if token:
        game_state = GameState(room=uuid.uuid4().__str__())
        db.session.add(game_state)
        db.session.commit()

        player1 = Player(name='Player 1', token=token,
                         game_state_id=game_state.id)
        db.session.add(player1)
        db.session.commit()

        remaining_tokens = [t for t in ['Iron Man', 'Captain America', 'Thor', 'Hulk',
                                        'Black Widow', 'Hawkeye', 'Spider-Man', 'Captain Marvel'] if t != token]
        player2 = Player(name='Computer', token=random.choice(
            remaining_tokens), is_computer=True, game_state_id=game_state.id)
        db.session.add(player2)
        db.session.commit()

        game_state.current_player_id = player1.id
        db.session.commit()
        
        room_id = game_state.room
        return redirect(url_for('rooms', room=room_id))
    

@app.route('/rooms/<string:room>', methods=['GET'])
def rooms(room):
        game_state = GameState.query.filter_by(room=room).first()
        current_player = Player.query.get(game_state.current_player_id)
        
        if current_player.is_computer:
            die1, die2 = roll_dice()
            move_player(current_player, die1 + die2)

            game_state.status = 'waiting'
                      
            # switching to user
            next_player = Player.query.filter(
                Player.game_state_id == game_state.id, Player.id != game_state.current_player_id).first()
            game_state.status = 'ongoing'
            game_state.current_player_id = next_player.id
            db.session.commit()

        
        return render_template('dice_result.html', game_state=game_state,board=board)


@app.route('/tokens')
def tokens():
    players = Player.query.all()
    return render_template('tokens.html', players=players)


@app.route('/roll_dice', methods=['POST'])
def roll_dice_route():
    room_id = request.form.get('room_id')
    current_game = GameState.query.filter_by(room=room_id).first()

    if current_game:
        current_player = Player.query.get(current_game.current_player_id)
        die1, die2 = roll_dice()
        move_player(current_player, die1 + die2)
        
        current_game.status = 'waiting'
        db.session.commit()
        
    return redirect(url_for('rooms', room=room_id))


@app.route('/switch_turn', methods=['POST'])
def switch_turn():
    room_id = request.form.get('room_id')
    current_game = GameState.query.filter_by(room=room_id).first()

    if current_game:
        current_player = Player.query.filter(Player.game_state_id == current_game.id, Player.id != current_game.current_player_id).first()
        current_game.status = 'ongoing'
        current_game.current_player_id = current_player.id
        db.session.commit()

    return redirect(url_for('rooms', room=room_id))

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
