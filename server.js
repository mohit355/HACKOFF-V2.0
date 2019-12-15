const express = require("express");
const bodyParser = require("body-parser");
const mongoose = require("mongoose");
const ejs = require("ejs");
const md5 = require("md5");
var uniqueValidator = require('mongoose-unique-validator');
var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/";

const app = express();

app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static("public"));
app.set('view engine', 'ejs');
mongoose.connect("mongodb://localhost:27017/EyeDB", {useNewUrlParser: true, useUnifiedTopology: true });

const registerSchema = mongoose.Schema({
    fname: String,
    lname: String,
    email: {type:String, unique:true, required: true},
    password: {type:String, required: true}
});
registerSchema.plugin(uniqueValidator);

const Register = mongoose.model("Register", registerSchema);

app.get("/", function(req,res){
    res.render("index");
});


app.get("/login", function(req,res){
    res.render("login", {pass:"", noUser:""});
});

app.post("/register", function(req,res){
    const registerUser = new Register({
        fname: req.body.fname,
        lname: req.body.lname,
        email: req.body.email,
        password: md5(req.body.password)
    });

    registerUser.save(function(err){
        if(!err){
            res.send("User Registered Successfully");
        }else{
            res.send("0");
            
        }
    });
});

const loginSchema = mongoose.Schema({
    email: String,
    password: String,

    
});

const Login = mongoose.model("Login", loginSchema);

app.post("/login", function(req,res){
   Register.findOne({email: req.body.email}, function(err,result){
       if(result){
           if(result.password === md5(req.body.password)){
            MongoClient.connect(url, function(err, db) {
                if(db){
                var dbo = db.db("EyeDB");
                dbo.collection("newData").findOne({email:req.body.email}, function(err, data) {
                  if(data){
                    
                    res.render("showcase", {data: data.time});
                    db.close();
                  }else{
                      console.log(err);
                      
                  }
                  
                });
                }else{
                    console.log(err);
                    
                }
                
              });
           }else{
               res.render("login", {pass: "Incorrect Password", noUser: ""});
           }
       }else{
           res.render("login", { pass: "", noUser: "No user found"});
       }
   })
});



app.listen(3000, function(){
    console.log("Server is running on port http://localhost:3000");
});
