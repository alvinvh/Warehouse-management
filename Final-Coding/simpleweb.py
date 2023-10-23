from flask import Flask, redirect, url_for, render_template, request, session
from insert_data import insert_data
from barcode_scanner import barcode_scan
from show_table import get_table, get_dropdownlist_name, get_dropdownlist_barcode, get_barcode, get_name, check_contain, get_table_all, get_login
from update_table import update_contain, delete_db
import hashlib

app = Flask(__name__)
app.secret_key = "group5"

@app.route("/")
def home():     #home page
    if "user" in session:
        return render_template("index.html")
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():    #login page
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["pwd"]
        hash = hashlib.md5(str(pwd).encode('utf-8'))    #hashing the user input password
        a = get_login(user)
        b = hash.hexdigest()
        if a == b:      #comparing password input with stored password
            session["user"] = user
            return redirect("/")
        else:
            return render_template("login.html", message = "Login Error")
    else:
        if "user" in session:
            return redirect("/")

        return render_template("login.html")

@app.route("/logout")       #logout function
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/scan_item_page")
def scan_item_page():       #scan item page
    if "user" in session:
        list_name = get_dropdownlist_name("item")   #generating drop down list
        for i in get_dropdownlist_name("shelve"):
            list_name.append(i)
        list_barcode = get_dropdownlist_barcode("item")
        for i in get_dropdownlist_barcode("shelve"):
            list_barcode.append(i)
        return render_template("scan_item_page.html", type='scan', list_barcode=list_barcode, list_name=list_name)
    else:
        return redirect(url_for("login"))


@app.route("/scan_item_page/<message>", methods=['POST', 'GET'])
def scan_item_page_2(message):      #scan item with message variable
    if "user" in session:
        list_name = get_dropdownlist_name("item")
        for i in get_dropdownlist_name("shelve"):
            list_name.append(i)
        list_barcode = get_dropdownlist_barcode("item")
        for i in get_dropdownlist_barcode("shelve"):
            list_barcode.append(i)
        return render_template("scan_item_page.html", type='scan', list_barcode=list_barcode, list_name=list_name,
                               message=message)
    else:
        return redirect(url_for("login"))


@app.route("/register_item", methods=['POST', 'GET'])       #register page
def register_item():
    if "user" in session:
        return render_template("register_item.html", type='register')
    else:
        return redirect(url_for("login"))


@app.route("/register_item/<message>", methods=['POST', 'GET'])     #register item page with message
def register_item_2(message):
    if "user" in session:
        return render_template("register_item.html", type='register', message=message)
    else:
        return redirect(url_for("login"))


@app.route("/register_item/auto/<barcode>")
def register_item_auto(barcode):    #register using barcode scanner
    if "user" in session:
        return render_template("register_item_auto.html", barcode=barcode)
    else:
        return redirect(url_for("login"))


@app.route("/manual_scan", methods=['POST', 'GET'])
def manual_scan():      #find an item/shelf manually
    if "user" in session:
        type = request.form.get("type")
        if type == "register":      #register function for manual input
            item_name = request.form.get("item_name")
            barcode = request.form.get("item_barcode")
            if item_name == '' or barcode == '':        #checking if user enter correct form
                message = "Please fill name, barcode!"
            else:
                table = request.form.get("table")
                if table == '':
                    message = "Please choose the type!"
                else:
                    message = insert_data(table, (barcode, item_name))      #registering to the DB
            return redirect(url_for("register_item_2", message=message))
        elif type == "scan":        #scan function for manual input
            name = request.form.get("name")
            barcode_scan = request.form.get("barcode")
            if name != '' and barcode_scan == '':       #checking if user enter correct form
                barcode = get_barcode('item', name)     #function to return barcode
                table = "item"
                if barcode == None:
                    barcode = get_barcode('shelve', name)
                    table = "shelve"
                return render_template("scan_item_page_choice.html", barcode=barcode, table=table)
            elif name == '' and barcode_scan != '':     #checking if user enter correct form
                name = get_name('item', barcode_scan)
                table = "item"
                if name == None:
                    name = get_name('shelve', barcode_scan)     #function to return name
                    table = "shelve"
                return render_template("scan_item_page_choice.html", barcode=barcode_scan, table=table)
            else:
                message = "Please select either name or barcode!"
                return redirect(url_for("scan_item_page_2", message=message))
    else:
        return redirect(url_for("login"))



@app.route("/auto_scan", methods=['POST', 'GET'])
def auto_scan():
    if "user" in session:
        type = request.form.get("type")
        print(type)
        if type == "register":      #checking the type of a function
            scan = barcode_scan()       #function to scan a barcode
            if scan == None:        #check if the scan is success or not
                message = "Barcode not identified"
                return redirect(url_for("register_item_2", message=message))
            else:
                type, barcode = scan
                return redirect(url_for('register_item_auto', barcode=barcode))
        elif type == "scan":        #checking the type of a function
            scan = barcode_scan()       #function to scan a barcode
            if scan == None:        #check if the scan is success or not
                message = "Barcode not identified"
                return redirect(url_for("scan_item_page_2", message=message))
            else:
                a, barcode_scanned = scan       #unpacking
                barcode_scanned = str(barcode_scanned)
                barcode_scanned = barcode_scanned.lstrip("'b'").rstrip("'")     #cleaning the barcode data
                name = get_name('item', barcode_scanned)
                table = "item"
                if name == None:
                    name = get_name('shelve', barcode_scanned)
                    table = "shelve"
                return render_template("scan_item_page_choice.html", barcode=barcode_scanned, table=table)
    else:
        return redirect(url_for("login"))



@app.route("/auto_scan_input", methods=['POST', 'GET'])
def auto_scan_input():      #function to input data to the DB
    if "user" in session:
        item_name = request.form.get("item_name")
        table = request.form.get("table")
        barcode = request.form.get("barcode")
        message = insert_data(table, (barcode, item_name))      #insert a data to the DB
        return redirect(url_for("register_item_2", message=message))
    else:
        return redirect(url_for("login"))



@app.route("/action", methods=['POST', 'GET'])
def action():       #function to do in, out, or location option
    if "user" in session:
        table = request.form.get("table")
        action = request.form.get("action")
        barcode = request.form.get("barcode")
        if action == "in":      #checking which option did the user choose
            if table == "item":
                return render_template("in.html", barcode=barcode, dropdownlist=get_dropdownlist_name("shelve"),
                                       name="shelve")
            elif table == "shelve":
                return render_template("in.html", barcode=barcode, dropdownlist=get_dropdownlist_name("item"),
                                       name="item")
        elif action == "out":       #checking which option did the user choose
            if table == "item":
                list = get_table_all("shelve")
                for i in list:
                    if i[3] == barcode:
                        message = update_contain("", i[0], "", "")
                        return redirect(url_for("scan_item_page_2", message=message))
                return redirect(url_for("scan_item_page_2", message="Iten is not located anywhere"))
            elif table == "shelve":
                list = get_table_all("shelve")
                for i in list:
                    if i[0] == barcode:
                        if i[3] != None or i[3] != '':
                            message = update_contain("", i[0], "", "")
                            return redirect(url_for("scan_item_page_2", message=message))
                return redirect(url_for("scan_item_page_2", message="the shelf is empty"))

        elif action == "location":      #checking which option did the user choose
            if table == "item":
                list = get_table_all("shelve")
                for i in list:
                    if i[3] == barcode:
                        location = i[1]
                        item_name = i[3]
                        last_user = i[2]
                        message1 = "Item : {}".format(item_name)
                        message2 = "Location : {}".format(location)
                        message3 = "Last User : {}".format(last_user)
                        return render_template("location.html", location=location, message1=message1, message2=message2,
                                               message3=message3)
                message1 = "Item {} is not located anyhwere".format(get_name("item", barcode))
                return render_template("location.html", message1=message1, location="")
            elif table == "shelve":
                list = get_table_all("shelve")
                for i in list:
                    if i[0] == barcode:
                        if i[3] != None or i[3] != '':
                            location = i[1]
                            item_name = i[3]
                            last_user = i[2]
                            message1 = "Shelve : {}".format(location)
                            message2 = "Contain : {}".format(item_name)
                            message3 = "Last User : {}".format(last_user)
                            return render_template("location.html", location=location, message1=message1,
                                                   message2=message2, message3=message3)
                message1 = "Shelve {} does not contain anything".format(get_name("shelve", barcode))
                return render_template("location.html", message1=message1, location="")
    else:
        return redirect(url_for("login"))



@app.route("/action_in", methods=['POST', 'GET'])
def action_in():
    if "user" in session:
        type = request.form.get("type")
        barcode = request.form.get("barcode")
        selection = request.form.get("selection")
        if type == "item":
            barcode_item = get_barcode("item", selection)
            #print(selection)
            if check_contain(barcode) == "empty":
                message = update_contain(barcode_item, barcode, selection, session["user"])
                return redirect(url_for("scan_item_page_2", message=message))
            elif check_contain(barcode) == "fill":
                message = "Shelve is occupied! Please do Shelve-OUT!"
                return redirect(url_for("scan_item_page_2", message=message))
        elif type == "shelve":
            barcode_shelve = get_barcode("shelve", selection)
            if check_contain(barcode_shelve) == "empty":
                item_name = get_name("item", barcode)
                message = update_contain(barcode, barcode_shelve, item_name, session["user"])
                return redirect(url_for("scan_item_page_2", message=message))
            elif check_contain(barcode_shelve) == "fill":
                message = "Shelve is occupied! Please do Shelve-OUT!"
                return redirect(url_for("scan_item_page_2", message=message))
    else:
        return redirect(url_for("login"))


@app.route("/action_in_auto", methods=['POST', 'GET'])
def action_in_auto():
    if "user" in session:
        type = request.form.get("type")
        barcode = request.form.get("barcode")
        scan = barcode_scan()
        if scan == None:
            return redirect(url_for("scan_item_page_2", message="Barcode not identified!"))
        else:
            barcode_type, scanned_barcode = scan
            scanned_barcode = str(scanned_barcode)
            scanned_barcode = scanned_barcode.lstrip("'b'").rstrip("'")
            selection = get_name("item", barcode)
            if type == "item":
                print(1)
                if check_contain(barcode) == "empty":
                    message = update_contain(scanned_barcode, barcode, selection, session["user"])
                    return redirect(url_for("scan_item_page_2", message=message))
                elif check_contain(barcode) == "fill":
                    message = "Shelve is occupied! Please do Shelve-OUT!"
                    return redirect(url_for("scan_item_page_2", message=message))
            elif type == "shelve":
                print(2)
                if check_contain(scanned_barcode) == "empty":
                    message = update_contain(barcode, scanned_barcode, selection, session["user"])
                    return redirect(url_for("scan_item_page_2", message=message))
                elif check_contain(scanned_barcode) == "fill":
                    message = "Shelve is occupied! Please do Shelve-OUT!"
                    return redirect(url_for("scan_item_page_2", message=message))
    else:
        return redirect(url_for("login"))


@app.route("/show_database", methods=['POST', 'GET'])
def show_database():
    if "user" in session:
        list_item = get_table_all("item")
        list_shelve = get_table_all("shelve")
        dropdownlist = get_dropdownlist_barcode("item")
        for i in get_dropdownlist_barcode("shelve"):
            dropdownlist.append(i)
        return render_template("show_database.html", list_item=list_item, list_shelve=list_shelve,
                               dropdownlist=dropdownlist)
    else:
        return redirect(url_for("login"))


@app.route("/show_database/<message>", methods=['POST', 'GET'])
def show_database_2(message):
    if "user" in session:
        list_item = get_table_all("item")
        list_shelve = get_table_all("shelve")
        dropdownlist = get_dropdownlist_barcode("item")
        for i in get_dropdownlist_barcode("shelve"):
            dropdownlist.append(i)
        return render_template("show_database.html", list_item=list_item, list_shelve=list_shelve,
                               dropdownlist=dropdownlist, message=message)
    else:
        return redirect(url_for("login"))


@app.route("/update_db", methods=['POST', 'GET'])
def update_db():
    if "user" in session:
        barcode = request.form.get("barcode")
        list = get_dropdownlist_barcode("item")
        list2 = get_dropdownlist_barcode("shelve")
        if barcode in list:
            message = delete_db("item", barcode)
        elif barcode in list2:
            message = delete_db("shelve", barcode)
        else:
            message = "Error"
        return redirect(url_for("show_database_2", message=message))
    else:
        return redirect(url_for("login"))




if __name__ == "__main__":
    app.run()