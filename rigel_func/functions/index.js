const functions = require('firebase-functions');
const admin = require('firebase-admin');
admin.initializeApp()
const path = require('path');
const os = require('os');
const fs = require('fs')
const cors = require('cors')({origin: true});

// // Create and Deploy Your First Cloud Functions
// // https://firebase.google.com/docs/functions/write-firebase-functions
//
exports.helloWorld = functions.https.onRequest((request, response) => {
    response.send("Hello from Firebase!");
});

exports.getData = functions.https.onRequest((request, response) => {
    cors(request, response, async () => {
        const fileName = 'knn.json'
        const filePath = 'ml1/'
        const bucket = admin.storage().bucket();
        const tempFilePath = path.join(os.tmpdir(), fileName);
        await bucket.file(filePath+fileName).download({destination: tempFilePath});

        fs.readFile(tempFilePath, 'utf8', function (err, text) {
            console.log('text file!');
            console.log(text);
            console.log('error!?');
            console.log(err);
            response.send(text);
        })
        response.send(text);
    });
})
