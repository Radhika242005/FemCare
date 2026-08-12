from flask import Blueprint, jsonify

from services.pcos_engine import (
    analyze_pcos_user
)


pcos_bp = Blueprint(
    "pcos",
    __name__
)


# ============================================================
# PERSONALIZED PCOS REFERENCE ANALYSIS
# ============================================================

@pcos_bp.route(
    "/analyze/<int:user_id>",
    methods=["GET"]
)
def analyze_pcos(user_id):

    try:

        result = analyze_pcos_user(
            user_id
        )


        if not result.get(
            "success",
            False
        ):

            return jsonify(
                result
            ), 404


        return jsonify(
            result
        ), 200


    except Exception as error:

        # IMPORTANT:
        # Show the real error while we are debugging.

        import traceback

        print(
            "\n========== PCOS ERROR =========="
        )

        print(
            "Error:",
            error
        )

        traceback.print_exc()

        print(
            "================================\n"
        )


        return jsonify({

            "success":
                False,

            "message":
                "PCOS analysis error.",

            "error":
                str(error)

        }), 500