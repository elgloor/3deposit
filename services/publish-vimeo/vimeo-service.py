import os
import json
import requests
import vimeo
from flask import Flask, request, jsonify

'''
Flask app that takes in 360 video file, JSON data, and credentials 
and publishes to Vimeo. 
'''

app = Flask(__name__)

@app.route('/vimeo', methods=['POST', 'GET'])


def get_keys():
    try:
        config = json.loads(request.form.get('config'))
        auth = config.get('auth')
        access_token = auth.get('access_token')
        client_id = auth.get('client_id')          
        client_secret = auth.get('client_secret')
        channel_id = auth.get('channel_id')
        video_id = auth.get('video_id')
    except Exception as err:
        return jsonify({'err': str(err)})

def post_file():
    if request.method == 'POST':
        # construct request
        client = vimeo.VimeoClient(
            token=access_token,
            key=client_id,
            secret=client_secret
        )

        try:
            # unpack payload
            data = json.loads(request.form.get('data'))
            name = data.get('name')
            description = data.get('description')
            filename = data.get('filename')
            projection = data.get('projection')
            stereo_format = data.get('stereo_format')

            file = request.files.get('file')
            if file and filename:
                file.save(filename)

                uri = client.upload(filename, data={
                    'name': name,
                    'description': description,
                    'spatial.projection': projection,
                    'spatial.stereo_format': stereo_format
                })

                os.remove(filename)
                return jsonify({'res': {'uri': uri}})
            else:
                return jsonify({'err': 'No file provided'})
        except Exception as err:
            return jsonify({'err': str(err)})

def get_data():
    if request.method == 'GET':
        # construct request
        client = vimeo.VimeoClient(
            token=access_token,
            key=client_id,
            secret=client_secret
        )

        try:
            if:
                videos = client.get('https://api.vimeo.com/channels/' + channel_id + '/videos')
                followers = client.get('https://api.vimeo.com/channels/' + channel_id + '/users')
                comments = client.get('https://api.vimeo.com/videos/' + video_id + '/comments')
                return jsonify({'res': {
                                    'videos': videos,
                                    'followers': followers,
                                    'comments': comments
                        })
            else:
                return jsonify({'err': 'No data provided'})
        except Exception as err:
            return jsonify({'err': str(err)})

if __name__ == '__main__':
    app.run(debug=True)
