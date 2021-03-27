const User = require("../models/User");

exports.loginUser = async function (req, res, next) {
  //console.log(req.body);
  const user = await User.find({ email: req.body.email });
  if (user.length === 0) {
    //console.log("1");
    await User.create({
      name: req.body.name,
      email: req.body.email,
      photo: req.body.photoUrl,
    });
  }
};
