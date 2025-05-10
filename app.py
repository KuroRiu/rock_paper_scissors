from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import random
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app)

CHOICES = ['rock', 'paper', 'scissors']

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('game'))
    return render_template('index.html')

@app.route('/game')
def game():
    username = session.get('username', None)
    if not username:
        return redirect(url_for('home'))
    return render_template('game.html', username=username)

@app.route('/play', methods=['POST'])
def play():
    data = request.json
    user_choice = data['choice']
    difficulty = data['difficulty']

    def determine_computer_choice(user_choice, difficulty):
        outcome_weights = {
            'easy': [0.1, 0.2, 0.7],
            'medium': [0.5, 0.3, 0.2],
            'hard': [0.4, 0.15, 0.45]
        }

        win_map = {
            'rock': 'scissors',
            'scissors': 'paper',
            'paper': 'rock'
        }

        lose_map = {v: k for k, v in win_map.items()}
        draw_map = {k: k for k in CHOICES}

        options = [
            win_map[user_choice],     # комп виграє
            draw_map[user_choice],   # нічия
            lose_map[user_choice]    # комп програє
        ]
        choice = random.choices(options, weights=outcome_weights[difficulty])[0]
        return choice

    computer_choice = determine_computer_choice(user_choice, difficulty)

    if user_choice == computer_choice:
        result = 'draw'
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'scissors' and computer_choice == 'paper') or \
         (user_choice == 'paper' and computer_choice == 'rock'):
        result = 'win'
    else:
        result = 'lose'

    return jsonify({
        'user_choice': user_choice,
        'computer_choice': computer_choice,
        'result': result
    })

if __name__ == '__main__':
    app.run(debug=True)
