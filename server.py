import sqlite3
from flask import Flask, request


DB_FILE = "inventory.db"

app = Flask(__name__)


@app.route("/create_item", methods=["POST"])
def create_item():
    request_data = request.get_json(silent=True)
    if isinstance(request_data, dict):
        if (
            "ID" in request_data
            and type(request_data["ID"]) is str
            and "Description" in request_data
            and type(request_data["Description"]) is str
        ):
            ID = request_data["ID"]
            Description = request_data["Description"]
            Quantity = 1
            if "Quantity" in request_data and type(request_data["Quantity"]) is int:
                Quantity = request_data["Quantity"]

            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO Inventory VALUES (?, ?, ?, date('now'))", (ID, Quantity, Description))
                except:
                    return {"success": False}, 409

            return {"success": True}, 200

    return {"success": False}, 400


@app.route("/update_item", methods=["PATCH"])
def update_item():
    request_data = request.get_json(silent=True)
    if isinstance(request_data, dict):
        if "ID" in request_data and type(request_data["ID"]) is str:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()

                ID = request_data["ID"]
                Description = None
                Quantity = None

                try:
                    Quantity, Description = cursor.execute(
                        "SELECT Quantity, Description FROM Inventory WHERE ID = ?",
                        (ID,),
                    ).fetchone()
                except:
                    return {"success": False}, 404

                if "Description" in request_data and type(request_data["Description"]) is str:
                    Description = request_data["Description"]
                if "Quantity" in request_data and type(request_data["Quantity"]) is int:
                    Quantity = request_data["Quantity"]
                if "Quantity_change" in request_data and type(request_data["Quantity_change"]) is int:
                    Quantity += request_data["Quantity_change"]

                try:
                    cursor.execute(
                        "UPDATE Inventory SET Quantity = ?, Description = ? WHERE ID = ?",
                        (Quantity, Description, ID),
                    )
                except:
                    return {"success": False}, 409

                return {"success": True}, 200

    return {"success": False}, 400


@app.route("/delete_item", methods=["DELETE"])
def delete_item():
    request_data = request.get_json(silent=True)
    if isinstance(request_data, dict):
        if "ID" in request_data and type(request_data["ID"]) is str:
            ID = request_data["ID"]

            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                rowcount = cursor.execute("DELETE FROM Inventory WHERE ID = ?", (ID,)).rowcount

                if rowcount > 0:
                    return {"success": True}, 200
                else:
                    return {"success": False}, 404

    return {"success": False}, 400


@app.route("/get_items", methods=["GET"])
def get_items():
    request_data = request.get_json(silent=True)
    if isinstance(request_data, dict):
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            ID = None
            Description_match = None
            Quantity_min = None
            Quantity_max = None
            Date_after = None
            Date_before = None

            if "ID" in request_data and type(request_data["ID"]) is str:
                ID = request_data["ID"]
            if "Description_match" in request_data and type(request_data["Description_match"]) is str:
                Description_match = request_data["Description_match"]
            if "Quantity_min" in request_data and type(request_data["Quantity_min"]) is int:
                Quantity_min = request_data["Quantity_min"]
            if "Quantity_max" in request_data and type(request_data["Quantity_max"]) is int:
                Quantity_max = request_data["Quantity_max"]
            if "Date_after" in request_data and type(request_data["Date_after"]) is str:
                Date_after = request_data["Date_after"]
            if "Date_before" in request_data and type(request_data["Date_before"]) is str:
                Date_before = request_data["Date_before"]

            items = []

            try:
                sql_query = "SELECT * FROM InventoryFTS WHERE ID IS NOT NULL "
                sql_args = []

                if ID is not None:
                    sql_query += "AND ID = ? "
                    sql_args.append(ID)
                if Description_match is not None:
                    sql_query += "AND Description MATCH ? "
                    sql_args.append(Description_match)
                if Quantity_min is not None:
                    sql_query += "AND Quantity >= ? "
                    sql_args.append(Quantity_min)
                if Quantity_max is not None:
                    sql_query += "AND Quantity <= ? "
                    sql_args.append(Quantity_max)
                if Date_after is not None:
                    sql_query += "AND DateAdded >= ? "
                    sql_args.append(Date_after)
                if Date_before is not None:
                    sql_query += "AND DateAdded <= ? "
                    sql_args.append(Date_before)

                print(sql_query)

                items = list(
                    map(
                        lambda row: dict(row),
                        cursor.execute(sql_query, sql_args).fetchall(),
                    )
                )
            except:
                return {"success": False}, 404

            return {"success": True, "items": items}, 200

    return {"success": False}, 400
