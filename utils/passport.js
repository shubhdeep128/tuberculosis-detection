const mongoose = require("mongoose");
const User = require("../models/User")
const passport = require("passport");
const GoogleStrategy = require("passport-google-oauth20").Strategy;

require("dotenv/config")

passport.serializeUser((user, done) => {
  const session = {
      id: user.gooogleID,
      token: user.accessToken,
      name: user.name,
      displayPicture: user.url,
      email: user.email
  }
  done(null, session);
});


passport.deserializeUser((sessionUser, done) => {
  done(null, sessionUser)
});

passport.use('google',
  new GoogleStrategy(
    {
      clientID: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
      callbackURL: "/auth/google/callback",
      passReqToCallback: true
    },
    (req,accessToken, refreshToken, profile, done) => {
      req.session.accessToken = accessToken
      req.session.refreshToken = refreshToken
      console.log(req.session)
      User.findOne({ email: profile.emails[0].value }).then(existingUser => {
        if (existingUser) {
          done(null, existingUser);
        } else {
          new User({
            googleId: profile.id,
            name: profile.displayName,
            email: profile.emails[0].value,
            photo: profile.photos[0].value.split("?")[0]
          })
            .save()
            .then((user)=>{
              console.log("New User Created")
              done(null,user);
          });
        }
      });


    }
  )
);
