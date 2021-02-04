const awsSDK = require("aws-sdk");
const fs = require("fs");
const mime = require("mime-types");
const { isImage } = require("./fileExtension");
const axios = require("axios");

exports.uploadS3 = async function (req, res, next) {
    if (req.files) {
        try {
            let isValid = true;

            await req.files.forEach(function (file) {
                if (!isImage(file.path)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                await req.files.forEach(function (file) {
                    fs.unlinkSync(file.path);
                });
                return next({
                    message: "One of the files is not a valid image file",
                });
            }

            let URLs = [];
            let cannyURLs = [];

            req.files.forEach(async (file) => {
                await uploadFile(file.filename, file.path);
                URLs.push(process.env.CLOUDFRONT_URL + file.filename);
                let canny = await axios({
                    method: "post",
                    url: "http://127.0.0.1:5000/canny",
                    data: {
                        url: process.env.CLOUDFRONT_URL + file.filename, // This is the body part
                        filename: file.filename
                    },
                });
                cannyURLs.push(canny.data.url);
                fs.unlinkSync(file.path);
                if (cannyURLs.length === req.files.length) {
                    return res.status(200).json({ URLs, cannyURLs });
                }
            });
        } catch (e) {
            req.files.forEach(file => fs.unlinkSync(file.path));
            return next(e)
        }
    } else {
        return next("File not upladed");
    }
}

// exports.uploadS3 = async function (req, res, next) {
//     try {
//         await uploadFile(req.file.filename, req.file.path);
//         let urlResponse = process.env.CLOUDFRONT_URL + req.file.filename;
//         fs.unlinkSync(req.file.path);
//         return res.status(200).json(urlResponse);
//     } catch (e) {
//         return next(e);
//     }
// };

async function uploadFile(filename, fileDirectoryPath) {
    awsSDK.config.update({
        accessKeyId: process.env.S3_ACCESS_KEY_ID,
        secretAccessKey: process.env.S3_SECRET_ACCESS_KEY,
    });
    const s3 = new awsSDK.S3();

    return new Promise(function (resolve, reject) {
        fs.readFile(fileDirectoryPath.toString(), function (err, data) {
            if (err) {
                reject(err);
            }
            const conType = mime.lookup(fileDirectoryPath);
            s3.putObject(
                {
                    Bucket: "" + process.env.S3_BUCKET_NAME,
                    Key: filename,
                    Body: data,
                    ContentType: conType,
                    ACL: "public-read",
                },
                function (err, data) {
                    if (err) reject(err);
                    resolve("successfully uploaded");
                }
            );
        });
    });
}
