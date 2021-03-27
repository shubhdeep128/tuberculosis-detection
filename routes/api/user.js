const express = require("express");
const router = express.Router();
const { loginUser } = require("../../utils/user");

router.post("/login", loginUser);

module.exports = router;
