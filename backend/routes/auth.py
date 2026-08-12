from flask import Blueprint, request, jsonify
import bcrypt

from database import get_db_connection


auth_bp = Blueprint(
    "auth",
    __name__
)


# ============================================================
# REGISTER
# ============================================================

@auth_bp.route(
    "/register",
    methods=["POST"]
)
def register():

    connection = None
    cursor = None

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "message": "No data received."
            }), 400


        name = str(
            data.get("name", "")
        ).strip()


        email = str(
            data.get("email", "")
        ).strip().lower()


        password = data.get(
            "password",
            ""
        )


        # ====================================================
        # VALIDATION
        # ====================================================

        if not name:

            return jsonify({
                "success": False,
                "message": "Name is required."
            }), 400


        if not email:

            return jsonify({
                "success": False,
                "message": "Email is required."
            }), 400


        if not password:

            return jsonify({
                "success": False,
                "message": "Password is required."
            }), 400


        if len(password) < 6:

            return jsonify({
                "success": False,
                "message":
                    "Password must contain at least 6 characters."
            }), 400


        # ====================================================
        # DATABASE
        # ====================================================

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        # ====================================================
        # CHECK EXISTING USER
        # ====================================================

        cursor.execute(
            """
            SELECT
                id,
                name,
                email
            FROM users
            WHERE email = %s
            """,
            (email,)
        )


        existing_user = cursor.fetchone()


        if existing_user:

            return jsonify({
                "success": False,
                "message":
                    "An account with this email already exists."
            }), 409


        # ====================================================
        # HASH PASSWORD
        # ====================================================

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")


        # ====================================================
        # CREATE USER
        # ====================================================

        cursor.execute(
            """
            INSERT INTO users
            (
                name,
                email,
                password_hash
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """,
            (
                name,
                email,
                password_hash
            )
        )


        new_user_id = cursor.lastrowid


        connection.commit()


        # ====================================================
        # IMPORTANT
        # RETURN CREATED USER
        # ====================================================

        return jsonify({

            "success": True,

            "message":
                "Registration successful!",

            "user": {

                "id":
                    new_user_id,

                "name":
                    name,

                "email":
                    email
            }

        }), 201


    except Exception as error:

        if connection:
            connection.rollback()


        print(
            "Registration error:",
            error
        )


        return jsonify({

            "success": False,

            "message":
                "Server error during registration.",

            "error":
                str(error)

        }), 500


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# LOGIN
# ============================================================

@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    connection = None
    cursor = None

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "message": "No data received."
            }), 400


        email = str(
            data.get("email", "")
        ).strip().lower()


        password = data.get(
            "password",
            ""
        )


        # ====================================================
        # VALIDATION
        # ====================================================

        if not email or not password:

            return jsonify({
                "success": False,
                "message":
                    "Email and password are required."
            }), 400


        # ====================================================
        # DATABASE
        # ====================================================

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        # ====================================================
        # FIND USER
        # ====================================================

        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                password_hash
            FROM users
            WHERE email = %s
            """,
            (email,)
        )


        user = cursor.fetchone()


        if not user:

            return jsonify({
                "success": False,
                "message":
                    "Invalid email or password."
            }), 401


        # ====================================================
        # PASSWORD CHECK
        # ====================================================

        password_hash = user["password_hash"]


        if isinstance(
            password_hash,
            str
        ):

            password_hash = password_hash.encode(
                "utf-8"
            )


        password_valid = bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash
        )


        if not password_valid:

            return jsonify({
                "success": False,
                "message":
                    "Invalid email or password."
            }), 401


        # ====================================================
        # LOGIN SUCCESS
        # ====================================================

        logged_user = {

            "id":
                int(user["id"]),

            "name":
                user["name"],

            "email":
                user["email"]
        }


        return jsonify({

            "success": True,

            "message":
                "Login successful!",

            "user":
                logged_user

        }), 200


    except Exception as error:

        print(
            "Login error:",
            error
        )


        return jsonify({

            "success": False,

            "message":
                "Server error during login.",

            "error":
                str(error)

        }), 500


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()