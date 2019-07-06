import numpy as np
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask import Flask, flash, request, redirect, url_for, jsonify, Response


class GenerateGrade(Resource):
    def centroid(musics):
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
            print(args)
            tracks = dict()
            trackList = []
            for id, track_id, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature, duration_ms, active, createdAt, updatedAt in args:
                trackList.append(track_id)
                t = [danceability, energy, instrumentalness, liveness, speechiness, valence, acousticness, mode, sigmoid(
                    duration_ms), sigmoid(key), sigmoid(time_signature), sigmoid(tempo), sigmoid(loudness)]
                tracks[track_id] = np.array(t)
        # features = args["feature"]
        except Exception as e:
            return {'error': str(e)}
