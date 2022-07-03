var AWS = require('aws-sdk');
var s3 = new AWS.S3();

exports.handler = (event) => {

    var listParams = {
        Bucket: "ee-assets-prod-us-east-1",
        Prefix: "modules/7009d8e656004426b1ea6f27f0487d56/v1/sisdemo/"
    };

    s3.listObjectsV2(listParams, function(err, data) {
        if (err) console.log(err, err.stack); // an error occurred
        else {
            if (data.Contents.length) {
                data.Contents.forEach(file => {
                    console.log(file);
                    var copyParams = {
                        Bucket: process.env.BUCKET,
                        CopySource: "ee-assets-prod-us-east-1" + '/' + file.Key,
                        Key: file.Key.replace("modules/7009d8e656004426b1ea6f27f0487d56/v1/sisdemo/", "sisdemo/")
                    };
                    console.log(copyParams);
                    s3.copyObject(copyParams, function(copyErr, copyData) {
                        if (copyErr) {
                            console.log(copyErr);
                        }
                        else {
                            console.log('Copied: ', copyParams.Key);
                        }
                    });
                });
            }
        }
    });
};