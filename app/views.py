# -*- coding:utf-8 -*-
from . import application, BASE_URL
from flask import render_template, request, json, flash, redirect, session
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from os import path
import uuid
from app.utility import visit_directory


mysql = MySQL()
mysql.init_app(application)


@application.route("/index")
@application.route("/")
def index():
    return render_template("index.html")


@application.route("/join", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        # Read the posted values from the UI
        _name = request.form.get("inputName", None)
        _email = request.form.get("inputEmail", None)
        _password = request.form.get("inputPassword", None)
        # Validate the received values
        if _name and _email and _password:
            try:
                _hashed_password = generate_password_hash(_password)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc(
                    "sp_Create_User",
                    (
                        _name, _email,
                        _hashed_password
                    )
                )
                data = cursor.fetchall()
                if len(data) == 0:
                    conn.commit()
                    flash("The user:{0} had been created successfully!!!"
                          .format(str(_name)), "success")
                    return json.dumps({"status": {"0": "The user:{0} had been \
                        created successfully!!!".format(str(_name))}})
                else:
                    flash("Error:{0} occured!!!"
                          .format(str(data[0])), "warning")
                    return json.dumps({"status": {"1": {"Error: {0} occured!!! \
                        ".formant(str(data[1]))}}})
            except Exception as e:
                flash("Error:{0} occured!!".format(str(e), "error"))
                return json.dumps({"status": {"1": {"Error: {0} occured!!"
                                                    .formant(str(e))}}})
            finally:
                cursor.close()
                conn.close()
        else:
            flash("Info:{}".format("Enter the required fields!!"), "info")
            return json.dumps({"status": {"2": {"Info: Enter the required \
                  fields!!"}}})
    else:
        return render_template("join.html")


@application.route("/login", methods=["POST", "GET"])
def sign_in():
    if request.method == "POST":
        _username = request.form.get("inputUsername", None)
        _password = request.form.get("inputPassword", None)

        if _username and _password:
            try:
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_Validate_Login', (_username, ))
                data = cursor.fetchall()
                if len(data) > 0:
                    conn.commit()
                    if check_password_hash(data[0][3], _password):
                        # 存储的是登录的用户在数据库中的id,主键
                        session["user_id"] = data[0][0]
                        return redirect("/userHome")
                    else:
                        return render_template("error.html", error="Wrong \
                              username or password")
                else:
                    flash("Info:{0}".format("The user is not existed, please \
                          sign up fisrt!!"), "info")
                    return redirect("signUp")
            except Exception as e:
                return render_template("error.html", error=str(e))
            finally:
                cursor.close()
                conn.close()
    return render_template("login.html")


@application.route("/home", methods=["POST", "GET"])
def home():
    if session.get("user_id"):
        return render_template("home.html")
    else:
        return render_template("error.html", error="Unauthorized Access!!!")


@application.route("/logout")
def sign_out():
    session.pop("user_id", None)
    return redirect("index")


@application.route("/addwish", methods=["POST", "GET"])
def add_wish():
    if request.method == "POST":
        try:
            _title = request.form.get("inputTitle", None)
            _description = request.form.get("inputDescription", None)
            _file_path = request.form.get("filePath", None)
            _is_done = 1 if request.form.get("isDone", None) == "on" else 0
            _is_private = 1 if request.form.get("isPrivate", None) == "on" \
                             else 0
            if session.get("user_id"):
                _user_id = session.get("user_id", None)
                conn = mysql.connect()
                cursor = conn.cursor()
                if not _title or not _description:
                    flash("Pleased complete the required fields!!!", "info")
                    return redirect("add_wish")
                cursor.callproc(
                    "sp_Add_Wish",
                    (
                        _title, _description,
                        _user_id, _file_path,
                        _is_done, _is_private
                    )
                )
                data = cursor.fetchall()
                if len(data) == 0:
                    conn.commit()
                    return redirect("home")
                else:
                    return render_template(
                        "error.html", error="Some errors occurred!!!")
            else:
                return render_template("error.html", error="Unauthorized \
                      access!!!")
        except Exception as e:
            return render_template("error.html", error=str(e))
        finally:
            cursor.close()
            conn.close()
    return render_template("add_wish.html")


@application.route("/get_wish_by_user_to_paginate", methods=["POST", "GET"])
def get_wish_by_user_to_paginate():
    if request.method == "POST":
        try:
            if session.get("user_id", None):
                _user_id = session.get("user_id")
                _page_limit = application.config.get("PAGELIMIT", 10)
                _offset = request.form.get("offset", None)
                _total_records = 0
                if _offset:
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.callproc(
                        "sp_Get_Wish_By_User_To_Paginate",
                        (
                            _user_id,
                            _page_limit,
                            _offset,
                            _total_records
                        )
                    )
                    data = cursor.fetchall()
                    #  @sp_getWishByUserToPaginate_3
                    #  @: prefix, the procedure variable
                    #  _3:suffix, the third parameter in the procedure
                    #  "sp_getWishByUserToPaginate", "OUT p_total bigint"
                    cursor.execute("SELECT @_sp_Get_Wish_By_User_To_Paginate_3"
                                   )
                    #  outParam: the total count received from the table
                    outParam = cursor.fetchall()
                    if len(data) is not 0:
                        conn.commit()
                        response = []
                        response.append({"status": {"0": "Get user's wishs \
                              successfully!!!"}})
                        wishs_dict = []
                        for wish in data:
                            wish_dict = {
                                "Id": wish[0],
                                "Title": wish[1],
                                "Description": wish[2],
                                "Time": wish[4]
                            }
                            wishs_dict.append(wish_dict)
                        response.append(wishs_dict)
                        response.append({"Total": outParam[0][0]})
                        return json.dumps(response)
                    else:
                        return json.dumps([{"status": {"1": "The result is \
                              empty!!!"}}])
                else:
                    return json.dumps([{"status": {"2": "Sorry, you are not \
                          authorized yet!!!"}}])
            else:
                return redirect("addwish")
        except Exception as e:
            return render_template("error.html", error=str(e))
        finally:
            cursor.close()
            conn.close()


@application.route("/getwishbyid", methods=["POST", "GET"])
def get_wish_by_id():
    if request.method == "POST":
        try:
            if session.get("user_id"):
                _id = request.form.get("id", None)
                _user_id = session.get("user_id")
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc("sp_Get_Wish_By_Id", (_id, _user_id))
                data = cursor.fetchall()
                wish = {
                            "title": data[0][1],
                            "description": data[0][2],
                            "filePath": data[0][5],
                            "accomplished": True if data[0][6] == 1 else False,
                            "private": True if data[0][7] == 1 else False
                }
                return json.dumps({"status": {"0": "Get wish by wisd id \
                      succussfully!!"}, "wish": wish})
        except Exception as e:
            return render_template("error.html", error=str(e))
        finally:
            cursor.close()
            conn.close()


@application.route("/updatewish", methods=["POST", "GET"])
def update_wish():
    if request.method == "POST":
        try:
            if session.get("user_id", None):
                _title = request.form.get("title", None)
                _description = request.form.get("description", None)
                _wish_id = request.form.get("wish_id", None)
                _user_id = session.get("user_id")
                _file_path = request.form.get("filePath", None)
                _accomplished = 1 if request.form.get("accomplished", None) \
                    == "true" else 0
                _private = 1 if request.form.get("private", None) == "true" \
                    else 0
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc(
                    "sp_Update_Wish",
                    (
                        _title,
                        _description,
                        _user_id,
                        _wish_id,
                        _file_path,
                        _accomplished,
                        _private
                    )
                )
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    return json.dumps({"status": {"o": "Update wish \
                          successfully!!!"}})
                else:
                    return json.dumps({"status": {"1": "Failed to update \
                          wish!!!"}})
            else:
                return render_template("error.html", error="Unauthorized \
                      access!!!")
        except Exception as e:
            return render_template("error.html", error=str(e))
        finally:
            cursor.close()
            conn.close()


@application.route("/deletewish", methods=["POST", "GET"])
def delete_wish():
    if request.method == "POST":
        try:
            if session.get("user_id", None):
                _wish_id = request.form.get("id", None)
                _user_id = session.get("user_id", None)
                _wish_file_path = ""
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc(
                    "sp_Delete_Wish",
                    (
                        int(_user_id),
                        int(_wish_id),
                        _wish_file_path
                    )
                )
                data = cursor.fetchall()
                cursor.execute("SELECT @_sp_Delete_Wish_2")
                outParam = cursor.fetchall()
                if len(data) is 0 and len(outParam) is not 0:
                    conn.commit()
                    return json.dumps({"status": {"0": "Delete wish \
                          successfully!!!"}, "wishFilePath": outParam[0][0]})
                else:
                    return json.dumps({"status": {"1": "Failed to delete \
                          wish!!!"}})
            else:
                return render_template("error.html", error="Unauthorized \
                      access!!!")
        except Exception as e:
                return render_template("error.html", error=str(e))
                return json.dumps({"error": str(e)})
        finally:
            cursor.close()
            conn.close()


@application.route("/uploadfile", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["fileUpload"]
        extension = path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        UPLOAD_FOLDER = path.join(BASE_URL, application.config[
              "UPLOAD_FOLDER"])
        try:
            file.save(path.join(UPLOAD_FOLDER, f_name))
            return json.dumps({"status": {"0": "Upload file {0} \
                  successfully!!!".format(f_name)}, "fileName": f_name})
        except Exception as e:
            return render_template("error.html", error=str(e))


@application.route("/deleteoldfile", methods=["GET", "POST"])
def delete_old_file():
    if request.method == "POST":
        oldFileName = request.form.get("oldFile", None)
        if visit_directory(BASE_URL, oldFileName):
            return json.dumps({"status": {"0": "Delete file {0} \
                  successfully!!!".format(oldFileName)}})
        else:
            return json.dumps({"status": {"1": "File {0} doesn't exists!!!"
                                          .format(oldFileName)}})
