app = Flask(
__name__,
template_folder="./templates", # define the route for pages
)
app.secret_key = "secretkeyforapplication"
