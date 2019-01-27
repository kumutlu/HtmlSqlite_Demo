from flask import Flask, render_template, request
import sqlite3
import sqlite3 as sql
app = Flask(__name__)

conn = sqlite3.connect('database.db')
print ("Opened database successfully")

#conn.execute('CREATE TABLE cars (brand TEXT, model TEXT, price TEXT, year TEXT)')
#print ("Table created successfully")
#conn.close()



@app.route('/')
def home():
    #return 'hey'
    return render_template('home.html')


@app.route('/enternew')
def new_car():
    return render_template('cars.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            brand = request.form['brand']
            model = request.form['model']
            year = request.form['year']
            price = request.form['price']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO cars (brand,model,year,price) "
                            "VALUES(?, ?, ?, ?)", (brand, model, year, price))

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
            con.close()


@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from cars")

    rows = cur.fetchall()
    return render_template("list.html", rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
