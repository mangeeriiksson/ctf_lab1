from flask import Flask, request, jsonify
from guardian_validator import validate_offering

app = Flask(__name__)

@app.route('/validate_offering', methods=['POST'])
def validate():
    data = request.get_json()
    password = data.get('password')
    code = int(data.get('code'))

    if validate_offering(password, code):
        return jsonify({"message": "Correct! The Pharaoh's Gate is unlocked."})
    return jsonify({"message": "Incorrect. The guardians deny your passage."})

if __name__ == '__main__':
    app.run(debug=True)
