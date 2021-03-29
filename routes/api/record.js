const express = require("express");
const router = express.Router();
const { postRecord, getRecord } = require("../../utils/record");

router.post("/update", postRecord);
router.get("/get/:id", getRecord);

module.exports = router;
