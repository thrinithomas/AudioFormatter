from flask import Flask, request
from werkzeug.utils import secure_filename
from pydub import AudioSegment
import os.path
import traceback

app = Flask(__name__)

audio_format_set = {'.m4a', '.mp3', '.aiff', '.wav'}


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/format', methods=['GET', "POST"])
def upload_file():
    if request.method == 'POST':
        f = request.files['audio_file']
        print(f.filename)
        if f:
            f_format = os.path.splitext(f.filename)[-1]

            # San check
            if f_format not in audio_format_set:
                return '{} is not support'.format(f_format)

            sound = AudioSegment.from_file(f, format="mp3")  # hardcode

            sound = sound[:9000]
            export_f = "test.m4a"
            # Why mp4 but not m4a? Is it related to codec in ffmpeg?
            file_handle = sound.export(export_f, format="mp4")

            # for i, chunk in enumerate(file_handle[::9000]):
            #     chunk.export(export_f, format="mp4")

            # f.save(secure_filename(export_f))
            return '{} uploaded successfully'.format(f_format)

        return 'No file attached'

    if request.method == 'GET':
        return 'Please submit an audio file!'

    @app.errorhandler(500)
    def internal_error(exception):
        print("Internal Server Error")
        print(traceback.format_exc())


if __name__ == '__main__':
    app.run(debug=True)
