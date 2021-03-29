var mongoose = require("mongoose");
var Schema = mongoose.Schema;

var RecordSchema = new Schema({
  imageUrl: {
    type: String,
  },
  cannyUrl: {
    type: String,
  },
  sobelXUrl: {
    type: String,
  },
  sobelYUrl: {
    type: String,
  },
  laplacianUrl: {
    type: String,
  },
  otsuUrl: {
    type: String,
  },
  points: {
    type: Object,
  },
  numberOfPoints: {
    type: Number,
  },
  originalArea: {
    type: Number,
  },
  originalPerimeter: {
    type: Number,
  },
  cannyArea: {
    type: Number,
  },
  cannyPerimeter: {
    type: Number,
  },
  laplacianArea: {
    type: Number,
  },
  laplacianPerimeter: {
    type: Number,
  },
  sobelXArea: {
    type: Number,
  },
  sobelXPerimeter: {
    type: Number,
  },
  sobelYArea: {
    type: Number,
  },
  sobelYPerimeter: {
    type: Number,
  },
  otsuArea: {
    type: Number,
  },
  otsuPerimeter: {
    type: Number,
  },
});

module.exports = Record = mongoose.model("records", RecordSchema);
