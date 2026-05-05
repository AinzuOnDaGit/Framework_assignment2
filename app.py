app = Flask(
__name__,
template_folder="../client/templates", # define the route for pages
)
app.secret_key = "secretkeyforapplication"
