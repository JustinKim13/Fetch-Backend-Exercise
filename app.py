from flask import Flask, request, jsonify
from collections import deque, defaultdict
from datetime import datetime

app = Flask(__name__)

transactions = deque()  # we'll use a double-ended queue to track transactions and their timestamps in their correct order
balances = defaultdict(int)  # keep track of each payer's balance, defaultdict will automatically initialize a payer's balance to 0 if it doesn't exist yet

# Add Points
@app.route('/add', methods=['POST'])
def add_points():
    data = request.json # data added as json request for POST method
    payer = data.get('payer')
    points = data.get('points')
    timestamp = data.get('timestamp')

    # append transaction to the deque as a hashmap
    transactions.append({
        'payer': payer,
        'points': points,
        'timestamp': datetime.fromisoformat(timestamp.replace("Z", "+00:00")) # make sure it's formatted correctly
    })

    # update our payer's balance by adding the points
    balances[payer] += points 
    return '', 200

@app.route('/spend', methods=['POST'])
def spend_points():
    data = request.json
    remaining_to_spend = data.get('points')  # how much we have to spend
    
    if sum(balances.values()) < remaining_to_spend: # check if we have enough points to begin with before spending them, otherwise we can reutrn a 400 error
        return "User doesn't have enough points", 400

    spend_summary = [] # we can use this to track where points were spent from
    total_spent = defaultdict(int)
    
    # now we can spend our points
    while remaining_to_spend > 0 and transactions:
        transaction = transactions.popleft()  # get oldest transaction from the left
        payer = transaction['payer']
        points = transaction['points']
        timestamp = transaction['timestamp']

        if remaining_to_spend >= points: # if we have to spend more than our current transaction's points, then we can spend the full thingg and update balances and remaining to spend
            total_spent[payer] += points
            remaining_to_spend -= points
            balances[payer] -= points
        else:
            total_spent[payer] += remaining_to_spend # don't need to update remaining_to_spend, since we know we're going to use the rest
            balances[payer] -= remaining_to_spend

            # now we can reappend any points remaining for the transactions
            transactions.appendleft({
                'payer': payer,
                'points': points - remaining_to_spend,
                'timestamp': timestamp
            })
            remaining_to_spend = 0 # reset to 0 to end while statement, as we're not changing it above

    for payer, points in total_spent.items():
        spend_summary.append({
            "payer": payer,
            "points": -points
        })

    return jsonify(spend_summary), 200

# Get Balance
@app.route('/balance', methods=['GET'])
def get_balance():
    return jsonify(balances), 200

if __name__ == '__main__':
    app.run(port=8000)
