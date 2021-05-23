# -*- coding: utf-8 -*-
import csv
import os
import wget
import io
# import firebase-admin

from google.cloud import storage, firestore


# GOOGLE_APPLICATION_CREDENTIALS="C:\Users\Arkhi\Documents\ФКН\2 курс\Проект\kino-locations-2a1cc9439381.json"

# cred = credentials.RefreshToken('path/to/refreshToken.json')
# default_app = firebase_admin.initialize_app(cred)

storageClient = storage.Client()
storageBucket = storageClient.get_bucket("kino-locations.appspot.com")

firestoreClient = firestore.Client()
db = firestoreClient.collection("kino-locations")

with io.open("all.csv", "r", newline="", encoding='utf-8') as cian:
    data = csv.DictReader(cian)
    folder_idx = 0
    for row in data:
        if folder_idx == 5:  # for testing
            break
        doc = db.document(str(folder_idx))
        # print(row)
        doc.set(
            {
                "title": row["title"],
                "address": row["address"],
                "price": int(row["price"].replace(" ", "")),
                "floor": int(row["floor"].replace(" ", "")),
                "overall floor": int(row["overall floor"].replace(" ", "")),
                "rooms": int(row["rooms"].replace(" ", "")),
                "square": int(row["square"].replace(" ", "")),
                "contact": row["contact"],
            }
        )
        image_idx = 0
        images = row["images"].split()
        for image_url in images:
            print (image_url)
            try:
                filename = wget.download(image_url)
                print()
            except:
                print('fall')
                continue
            image = storageBucket.blob(
                str(folder_idx) + "/" + str(image_idx) + "." + filename.split(".")[-1]
            )
            image.upload_from_filename(filename)
            os.remove(filename)
            image_idx += 1
        folder_idx += 1
    doc = db.document("counter")
    doc.set({"count": folder_idx})
