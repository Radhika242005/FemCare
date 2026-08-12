from flask import Blueprint, jsonify

from services.menstrual_dataset_service import (
    get_menstrual_dataset_summary
)


datasets_bp = Blueprint(
    "datasets",
    __name__
)


# ============================================================
# MENSTRUAL DATASET SUMMARY
# ============================================================

@datasets_bp.route(
    "/menstrual",
    methods=["GET"]
)
def menstrual_dataset():

    try:

        summary = (
            get_menstrual_dataset_summary()
        )


        return jsonify({

            "success": True,

            "dataset": summary

        }), 200


    except Exception as error:

        print(
            "Dataset error:",
            error
        )


        return jsonify({

            "success": False,

            "message":
                "Unable to load menstrual dataset."

        }), 500
    # ============================================================
# MENSTRUAL DATASET ANALYSIS
# ============================================================

@datasets_bp.route(
    "/menstrual/analysis",
    methods=["GET"]
)
def menstrual_dataset_analysis():

    try:

        from services.menstrual_dataset_service import (
            get_menstrual_dataset_analysis
        )


        analysis = (
            get_menstrual_dataset_analysis()
        )


        return jsonify({

            "success": True,

            "analysis": analysis

        }), 200


    except Exception as error:

        print(
            "Dataset analysis error:",
            error
        )


        return jsonify({

            "success": False,

            "message":
                "Unable to analyze menstrual dataset."

        }), 500
    # ============================================================
# PERSONALIZED MENSTRUAL ANALYSIS
# ============================================================

@datasets_bp.route(
    "/menstrual/personal/<int:user_id>",
    methods=["GET"]
)
def personalized_menstrual_analysis(user_id):

    try:

        from services.menstrual_dataset_service import (
            get_personalized_menstrual_analysis
        )

        result = get_personalized_menstrual_analysis(
            user_id
        )

        if not result.get("success"):

            return jsonify(result), 404

        return jsonify(result), 200

    except Exception as error:

        print(
            "Personal dataset analysis error:",
            error
        )

        return jsonify({

            "success": False,

            "message":
                "Unable to perform personalized analysis."

        }), 500