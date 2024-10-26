# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The definition of the NVIDIA Conversational RAG API server."""

import os

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.responses import PlainTextResponse, RedirectResponse
from langserve import add_routes
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from . import errors
from .chain import my_chain  # type: ignore

# Get the proxy prefix from the environment variables, if any
PROXY_PREFIX = os.environ.get("PROXY_PREFIX", None)

# Create the FastAPI app with the specified title, version, and description
app = FastAPI(
    title="NVIDIA Conversational RAG",
    version="0.1.0",
    description="More advanced conversational RAG using NVIDIA components.",
    root_path=PROXY_PREFIX or "",
    middleware=[Middleware(errors.ErrorHandlerMiddleware)],
)

# Add routes to the app using the my_chain object
add_routes(
    app,
    my_chain,
)

# Add a health check endpoint
@app.get("/healthz", response_class=PlainTextResponse)
def healthz() -> str:
    """Report on the liveness of the server."""
    return "success"

# Add a root endpoint that redirects to the playground
@app.get("/", response_class=RedirectResponse)
def root() -> str:
    """Handle requests to the root directory."""
    return f"{PROXY_PREFIX or ''}/playground/"

# Enable telemetry for the FastAPI app
FastAPIInstrumentor.instrument_app(app)
