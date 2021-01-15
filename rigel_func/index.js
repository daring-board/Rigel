const {Storage} = require('@google-cloud/storage');
const bucketName = 'rigel-b11c1.appspot.com';
var fs = require('fs');

exports.uploadKNN = (req, res) => {
    res.set('Access-Control-Allow-Origin', '*');
    const storage = new Storage();
    switch (req.method) {
        case 'POST':
            const filename = 'ml1/knn.json';
            const data = req.body['JsonString'];
            storage.bucket(bucketName)
                .file(filename)
                .save(data, function(err) {
                    if (!err) {
                        console.log(`Successfully uploaded.`)
                    }
                });
            res.status(200).send('');
            break;
        case 'OPTIONS':
            res.set('Access-Control-Allow-Methods', '*');
            res.set('Access-Control-Allow-Headers', '*');
            res.set('Access-Control-Max-Age', '3600');
            res.status(204).send('');
            break;
        default:
            res.status(405).send({error: 'Something blew up!'});
            break;
    }
};

exports.getKNN = (req, res) => {
    res.set('Access-Control-Allow-Origin', '*');
    const storage = new Storage();

    switch (req.method) {
        case 'GET':
            const filename = 'ml1/knn.json';
            storage.bucket(bucketName)
                .file(filename)
                .download()
                .then((data) => {
                    res.status(200).json(data.toString());
                });
            break;
        case 'PUT':
            res.status(403).send('Forbidden!');
            break;
        case 'OPTIONS':
            res.set('Access-Control-Allow-Methods', '*');
            res.set('Access-Control-Allow-Headers', '*');
            res.set('Access-Control-Max-Age', '3600');
            res.status(204).send('');
            break;
        default:
            res.status(405).send({error: 'Something blew up!'});
            break;
    }
};