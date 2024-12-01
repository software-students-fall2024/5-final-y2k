import os
from datetime import datetime
from io import BytesIO
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session,
    flash,
)
from flask_login import (
    LoginManager,
    UserMixin,
    login_required,
    login_user,
    current_user,
    logout_user,
)
from pymongo import MongoClient
from gridfs import GridFS
from pymongo.errors import PyMongoError
from bson import ObjectId
from bson.errors import InvalidId
from werkzeug.security import generate_password_hash, check_password_hash
from pydub import AudioSegment
import speech_recognition as sr

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET")

client = MongoClient(os.getenv("DB_URI"))
db = client["audio_db"]
grid_fs = GridFS(db)
metadata_collection = db["audio_metadata"]
users_collection = db["users"]


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Handles registration.
    """
    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"]
    password = request.form["password"]

    if not username or not password:
        flash("Username and password are required.", "error")
        return redirect(url_for("register"))

    if users_collection.find_one({"username": username}):
        flash("Username already exists. Please choose a different one.", "error")
        return redirect(url_for("register"))

    password_hash = generate_password_hash(password)
    new_user = {"username": username, "password_hash": password_hash}

    try:
        users_collection.insert_one(new_user)
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))
    except PyMongoError as e:
        flash("Database error occurred. Please try again.", "error")
        return str(e), 500


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles  login
    """
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    if not username or not password:
        flash("Username and password are required.", "error")
        return redirect(url_for("login"))

    user = users_collection.find_one({"username": username})
    if not user:
        flash("Invalid username or password.", "error")
        return redirect(url_for("login"))

    if not check_password_hash(user["password_hash"], password):
        flash("Invalid username or password.", "error")
        return redirect(url_for("login"))

    login_user(User(user["username"]))
    session["username"] = username
    flash("Login successful.", "success")
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    """
    Handles logout
    """
    logout_user()
    session.pop("username", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("login"))


class User(UserMixin):
    """
    User class
    """

    def __init__(self, username):
        self.id = username


def fetch_and_convert_to_wav(file_id):
    """
    Fetch binary audio from GridFS and convert it to WAV format.
    """
    grid_file = grid_fs.get(file_id)
    content_type = grid_file.content_type

    file_data = grid_file.read()
    audio = AudioSegment.from_file(
        BytesIO(file_data), format=content_type.split("/")[-1]
    )
    wav_io = BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)

    return wav_io


def perform_speech_recognition(wav_io):
    """
    Perform speech-to-text on a WAV file.
    """
    recognizer = sr.Recognizer()

    print(f"Buffer size: {len(wav_io.getvalue())} bytes")
    try:
        print("Starting speech recognition...")

        with sr.AudioFile(wav_io) as source:
            print("Audio file opened successfully.")
            audio_data = recognizer.record(source)
            print("Audio data recorded successfully.")
            transcription = recognizer.recognize_sphinx(audio_data)
            print("Transcription completed successfully:", transcription)
            return transcription

    except sr.UnknownValueError:
        print("CMU Sphinx could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"CMU Sphinx request failed: {e}")
        return None
    except Exception as e:
        print("Error during speech recognition:")
        print(str(e))
        raise


def transcribe(file_id):
    """
    Predict transcription for the given file_id.
    """
    if not file_id:
        return jsonify({"error": "file_id is required"}), 400

    try:
        file_id = ObjectId(file_id)
        print("trying to fetch file")
        wav_io = fetch_and_convert_to_wav(file_id)
        print("file loaded and converted")
        transcription = perform_speech_recognition(wav_io)
        print("Transcription loaded:", transcription)

        result = metadata_collection.update_one(
            {"file_id": str(file_id)},
            {
                "$set": {
                    "transcription": transcription,
                    "processed_time": datetime.utcnow(),
                    "status": "completed",
                }
            },
        )

        if result.matched_count == 0:
            print("No document matched the query. Update failed.")
        elif result.modified_count == 0:
            print("Document matched, but no changes were made.")
        else:
            print("Document updated successfully.")
        return (
            jsonify(
                {
                    "message": "Prediction completed successfully",
                    "file_id": str(file_id),
                    "status": "completed",
                    "transcription": transcription,
                }
            ),
            200,
        )
    except InvalidId:
        print("Invalid file_id format. Could not convert to ObjectId.")
        return jsonify({"error": "Invalid file_id format"}), 400

    except FileNotFoundError:
        print("The file could not be found in GridFS.")
        return jsonify({"error": "File not found in GridFS"}), 404

    except PyMongoError as e:
        print("Database operation failed:", str(e))
        return jsonify({"error": "Database operation failed"}), 500


@app.route("/")
def index():
    print("printing documents")
    for document in metadata_collection.find():
        print(document)
    return render_template("index.html")


@app.route("/record")
def record():
    """
    Record route
    """
    return render_template("record.html")


@app.route("/upload-audio", methods=["POST"])
def upload_audio():
    """
    Endpoint to upload files and store raw binary in GridFS with metadata.
    Notifies the ML client upon successful storage.
    """
    if "audio" not in request.files or "name" not in request.form:
        return jsonify({"error": "Audio file and name are required"}), 400

    audio_file = request.files["audio"]
    file_name = request.form["name"]

    gridfs_id = grid_fs.put(
        audio_file,
        filename=file_name,
        content_type=audio_file.mimetype,
    )

    if not gridfs_id:
        return jsonify({"error": "Failed to store the audio file in GridFS"}), 500

    metadata = {
        "file_id": str(gridfs_id),
        "name": file_name,
        "upload_time": datetime.utcnow(),
        "transcription": "",
    }

    metadata_result = metadata_collection.insert_one(metadata)

    if not metadata_result.acknowledged:
        return jsonify({"error": "Failed to store the metadata in the database"}), 500

    print("File successfully uploaded with GridFS ID:", gridfs_id)
    return transcribe(gridfs_id)


if __name__ == "__main__":
    app.run(port=8080, debug=True)
