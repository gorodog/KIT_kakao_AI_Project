from flask import Flask, jsonify
import sys
import random
application = Flask(__name__)


@application.route("/random", methods=["POST"])
def random_function():
    response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": str(random.randint(1, 10))
                    }
                }
            ]
        }
    }
    return jsonify(response)


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=int(sys.argv[1]), debug=True)