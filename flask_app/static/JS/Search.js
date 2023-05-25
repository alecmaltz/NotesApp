const express = require("express");
const mysql = require("mysql");

const app = express();
app.use(express.json());

//searchTerms is the name of the input field in the form

//also need to change the db_name to the name of your database

//also don't forget: npm install mysql


const db = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "root",
  database: "db_name"
});

app.post("/search", (req, res) => {
  let searchTerms = req.body.searchTerms.replace(/\s/g, ""); // Remove spaces
  let sql = "SELECT * FROM Items WHERE name LIKE ?";
  let query = "%" + searchTerms + "%";

  db.query(sql, query, (error, results) => {
    if (error) {
      res.send({ error: error });
    } else {
      res.send({ results: results });
    }
  });
});


