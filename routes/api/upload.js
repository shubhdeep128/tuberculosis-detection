const express = require("express");
const app = express();
const multer = require("multer");
const { uploadS3 } = require("../../utils/uploadS3");
const router = express.Router();

const storage = multer.diskStorage({
    destination: "./files",
    filename(req, file, cb) {
        let newName = Date.now() + "-" + file.originalname;
        newName = newName.split(" ").join("_");
        cb(null, newName);
    },
});

const upload = multer({ storage });

router.post("/upload", upload.array("files", 5), uploadS3);

module.exports = router;
