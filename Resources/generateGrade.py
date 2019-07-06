import os
import json
import urllib.request
import ssl
import numpy as np

from flask_restful import Resource, Api
from flask_restful import reqparse
from flask import Flask, flash, request, redirect, url_for, jsonify, Response


class GenerateGrade(Resource):
    def centroid(self, musics):
        n = len(musics)  # numero de musicas
        m = len(musics[0])  # numero de caracteristicas
        center = np.zeros(m)  # vetor centro das caracteristicas

        for music in musics:
            for i in range(m):
                center[i] = music[i] + center[i]

        center = center/n

        return center

    def sigmoid(self, x):
        return 1/(1+np.exp(-x))

    def post(self):
        try:
            parser = reqparse.RequestParser()
            args = parser.parse_args()
            data = request.data
            dataDict = json.loads(data)
            roomCode = dataDict['code']
            url = os.environ.get(
                "MAINAPI", "http://localhost:3001/v1")+"/rooms/"+roomCode+"/ia"
            body = {}

            req = urllib.request.Request(url)
            req.add_header('Content-Type', 'application/json; charset=utf-8')

            jsondata = json.dumps(body)
            jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
            req.add_header('Content-Length', len(jsondataasbytes))
            response = urllib.request.urlopen(req, jsondataasbytes)
            string = response.read().decode('utf-8')
            json_obj = json.loads(string)

            # prints the string with 'source_name' key
            tracks = dict()
            trackList = []
            for track in json_obj:
                trackList.append(track['track_id'])
                t = [track['danceability'], track['energy'], track['instrumentalness'], track['liveness'], track['speechiness'], track['valence'], track['acousticness'],
                     track['mode'], sigmoid(track['duration_ms']), sigmoid(track['key']), sigmoid(track['time_signature']), sigmoid(track['tempo']), sigmoid(track['loudness'])]
                tracks[track['track_id']] = np.array(t)

            print(tracks)

        except Exception as e:
            return {'error': str(e)}
