from flask import Flask, jsonify, request, abort

app = Flask(__name__)

class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Missing 'title' in request"}), 400
    new_id = max([event.id for event in events]) + 1 if events else 1
    new_event = Event(new_id, data["title"])
    events.append(new_event)
    return jsonify(new_event.to_dict()), 201


@app.route("/events/<int:id>", methods=["PATCH"])
def update_event(id):
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Missing 'title' in request"}), 400
    for event in events:
        if event.id == id:
            event.title = data["title"]
            return jsonify(event.to_dict()), 200
    return jsonify({"error": "Event not found"}), 404


@app.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    for i, event in enumerate(events):
        if event.id == id:
            del events[i]
            return jsonify({"message": "Event deleted"}), 204
    return jsonify({"error": "Event not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
