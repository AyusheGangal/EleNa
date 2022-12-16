"""
Flask API launcher
"""
from flask import Flask, request
import worker_funcs

app = Flask(__name__)

app.add_url_rule('/download_graph', view_func=worker_funcs.download_graph, methods=['POST'])
app.add_url_rule('/get_shortest_path', view_func=worker_funcs.get_shortest_path, methods=['POST'])

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=7007)
