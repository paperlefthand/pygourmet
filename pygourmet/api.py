"""pygourmet.api module
"""
import json

import requests

from pygourmet.exceptions import PyGourmetError

# logger = logging.getLogger(__name__)


def radius_to_range(radius: int) -> int:
    if radius <= 300:
        return 1
    elif radius <= 500:
        return 2
    elif radius <= 1000:
        return 3
    elif radius <= 2000:
        return 4
    else:
        return 5


class Api:
    """Api class

    API 呼び出しクラス

    Attributes:

    """

    BASE_URL = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"

    def __init__(self, keyid: str) -> None:
        """

        Init the Api instance

        Args:
            keyid (str): Key ID assigned to the user
        """
        if bool(keyid):
            self.keyid = keyid
        else:
            raise PyGourmetError("keyidを指定してください")

    def search(
        self,
        lat: float,
        lng: float,
        keyword: str = "",
        radius: int = 500,
        count: int = 10,
    ) -> dict:
        """

        Search restaurants by params

        Args:
            lat (float): latitude of POI
            lng (float): longitude of POI
            radius (int): radius[m] of search range from POI
            count (int): max result counts

        Returns:
            dict: search result

        Raises:
            PyGourmetError: if arguments have an invalid value

        """

        if count < 0:
            raise PyGourmetError("Invalid count value (must be >= 0)")

        if radius < 0:
            raise PyGourmetError("Invalid radius value (must be >= 0)")

        params = {
            "key": self.keyid,
            "lat": lat,
            "lng": lng,
            "range": radius_to_range(radius),
            "count": count,
            "keyword": keyword,
            "format": "json",
        }

        resp = requests.get(
            url=self.BASE_URL,
            params=params,
        )

        resp_dict = json.loads(resp.text)

        return resp_dict["results"]["shop"]
