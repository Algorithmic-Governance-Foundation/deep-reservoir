from enum import Enum
from typing import List
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
from attrs import define


class Status(str, Enum):
    YES = "YES"
    NO = "NO"
    PARTIAL = "PARTIAL"
    UNKNOWN = "UNKNOWN"


@define
class Research:
    """Research results from a researcher agent

    Attributes:
        prompt: The prompt used for the research
        policy: The policy being researched
        country: The country being researched
        data: The raw JSON response from the researcher model
    """

    prompt: str
    policy: str
    country: str
    data: str


@define
class Summary:
    """Summary of research results"""

    status: Status
    explanation: str
    sources: List[str]
    dump: str


def remove_utm_source(url: str) -> str:
    """Remove utm_source query parameter from a URL"""

    # Parse the URL
    parsed = urlparse(url)

    # Parse query parameters into a dictionary
    query_params = parse_qs(parsed.query)

    # Remove utm_source parameter
    query_params.pop("utm_source", None)

    # Rebuild the query string
    new_query = urlencode(query_params, doseq=True)

    # Reconstruct the URL
    new_parsed = parsed._replace(query=new_query)
    return urlunparse(new_parsed)
