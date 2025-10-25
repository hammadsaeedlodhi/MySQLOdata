from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection settings
db_config = {
    "host": "myhsldb.cjsysowmeja2.us-east-2.rds.amazonaws.com",
    "user": "admin",
    "password": "Mmahin2006",
    "database": "myhsldb",
    "port": 3306
}


@app.route('/odata/Accounts', methods=['GET'])
def get_accounts():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        query = "SELECT id AS ID, Name, Phone, Industry, Rating FROM Account"
        cursor.execute(query)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            "@odata.context": "/odata/$metadata#Accounts",
            "value": rows
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/odata/$metadata', methods=['GET'])
def metadata():
    return """<?xml version="1.0" encoding="utf-8"?>
<edmx:Edmx Version="4.0"
 xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
  <edmx:DataServices>
    <Schema Namespace="Default" xmlns="http://docs.oasis-open.org/odata/ns/edm">
      <EntityType Name="Account">
        <Key>
          <PropertyRef Name="ID"/>
        </Key>
        <Property Name="ID" Type="Edm.Int32"/>
        <Property Name="Name" Type="Edm.String"/>
        <Property Name="Phone" Type="Edm.String"/>
        <Property Name="Industry" Type="Edm.String"/>
        <Property Name="Rating" Type="Edm.String"/>
      </EntityType>
      <EntityContainer Name="Container">
        <EntitySet Name="Accounts" EntityType="Default.Account"/>
      </EntityContainer>
    </Schema>
  </edmx:DataServices>
</edmx:Edmx>
""", 200, {"Content-Type": "application/xml"}


@app.route('/')
def home():
    return "✅ OData Server is running. Try /odata/Accounts or /odata/$metadata"
