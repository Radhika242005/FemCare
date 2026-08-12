from flask import Flask

from flask_cors import CORS

from routes.auth import auth_bp
from routes.users import users_bp
from routes.periods import periods_bp
from routes.recommendations import recommendations_bp
from routes.datasets import datasets_bp
from routes.pcos import pcos_bp
from routes.trends import trends_bp
from routes.health_logs import health_logs_bp
from routes.thyroid import thyroid_bp
from routes.early_puberty import early_puberty_bp
from routes.perimenopause import perimenopause_bp
from routes.menopause import menopause_bp
from routes.postmenopause import postmenopause_bp
from routes.pregnancy import pregnancy_bp
from routes.food import food_bp
from routes.analysis_summary import analysis_summary_bp

app = Flask(__name__)

CORS(app)

app.register_blueprint(
    thyroid_bp,
    url_prefix="/api/thyroid"
)

# Authentication
app.register_blueprint(
    auth_bp,
    url_prefix="/api/auth"
)


# User profile
app.register_blueprint(
    users_bp,
    url_prefix="/api/users"
)
# Period tracking
app.register_blueprint(
    periods_bp,
    url_prefix="/api/periods"
)
app.register_blueprint(
    recommendations_bp,
    url_prefix="/api/recommendations"
)
app.register_blueprint(
    datasets_bp,
    url_prefix="/api/datasets"
)
app.register_blueprint(
    pcos_bp,
    url_prefix="/api/pcos"
)
app.register_blueprint(
    trends_bp,
    url_prefix="/api/trends"
)
app.register_blueprint(
    health_logs_bp,
    url_prefix="/api/health-logs"
)
app.register_blueprint(
    early_puberty_bp,
    url_prefix="/api/early-puberty"
)
app.register_blueprint(
    perimenopause_bp,
    url_prefix="/api/perimenopause"
)
app.register_blueprint(
    menopause_bp,
    url_prefix="/api/menopause"
)
app.register_blueprint(
    postmenopause_bp,
    url_prefix="/api/postmenopause"
)
app.register_blueprint(
    pregnancy_bp,
    url_prefix="/api/pregnancy"
)
app.register_blueprint(
    food_bp,
    url_prefix="/api/food"
)
app.register_blueprint(
    analysis_summary_bp,
    url_prefix="/api/analysis"
)
@app.route("/")
def home():

    return "FemCare Backend is Running!"


if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )