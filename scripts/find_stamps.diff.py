import json
import os
import sqlite3
import sys
import unicodedata
import urllib.request
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional

#### ------------------------ README -------------------------------------------
# This script fetches the user's stamps from Slowly and compares them with the
# ones I have. It uses the Slowly API to fetch user's stamps and compares them
# with my own stamps.

### Config file structure
# {
#     "auth_token": "Bearer ...", # Mandatory. Replace with your own auth token
#     "ignored_stamps": [] # Optional. List of stamp names to ignore
# }
#### ---------------------------------------------------------------------------

STAMPS_INFO_URL = "https://api.getslowly.com/slowly"
MY_INFO_URL = "https://api.getslowly.com/web/me"

CHAR_TRANSLATION = str.maketrans(
    {
        # smart apostrophes → ASCII
        "’": "'",
        "‘": "'",
        "‚": "'",
        "‛": "'",
        # smart quotes → ASCII
        "“": '"',
        "”": '"',
        # dashes → hyphen
        "–": "-",
        "—": "-",
        # invisible / special spaces → normal space
        "\u00a0": " ",  # NBSP
        "\u200b": " ",  # ZWSP
        "\u200c": " ",  # ZWNJ
        "\u200d": " ",  # ZWJ
        "\ufeff": " ",  # BOM
    }
)
ROOT_DIR_PATH = os.path.join(os.path.dirname(__file__), "..")


def normalize_text(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.translate(CHAR_TRANSLATION)
    return " ".join(s.split())


def measure_similarity(a, b):
    return SequenceMatcher(None, normalize_text(a), normalize_text(b)).ratio()


if __name__ == "__main__":
    config_path = os.path.join(ROOT_DIR_PATH, "scripts", "find_stamps_diff_config.json")
    if not os.path.exists(config_path):
        print("config file not found at: {}".format(config_path))
        sys.exit(-1)

    config_data: Optional[Dict[str, Any]] = None
    with open(config_path, "r") as fr:
        config_data = json.load(fr)
    auth_token: str = config_data["auth_token"]
    ignored_stamps: List[str] = config_data.get("ignored_stamps", [])

    # 1. Get the general info of the stamps
    stamps_data: List[Any] = []
    try:
        with urllib.request.urlopen(
            urllib.request.Request(
                STAMPS_INFO_URL,
                headers={"User-Agent": "python3"},
            )
        ) as fr:
            stamps_data = json.load(fr)["items"]
    except Exception as e:
        sys.exit("error while fetching STAMPS INFO data: {}".format(e))

    # 2. Get info about my stamps
    my_data: List[Any] = []
    try:
        with urllib.request.urlopen(
            urllib.request.Request(
                MY_INFO_URL,
                headers={
                    "user-agent": "python3",
                    "authorization": auth_token,
                    "content-type": "application/json",
                },
                method="POST",
            )
        ) as fr:
            my_data = json.load(fr)["items"]
    except Exception as e:
        sys.exit("error while fetching MY INFO data: {}".format(e))

    # 3. Get the stamps which I currently have by reading the db.
    db_path = os.path.join(ROOT_DIR_PATH, "resources", "data.db")

    my_current_stamps_in_db: List[str] = []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM stamps")
        for row in cursor.fetchall():
            my_current_stamps_in_db.append(row[0])
        conn.close()
    except Exception as e:
        sys.exit(f"error while reading stamps from database: {e}")

    # 4. Find the differences.
    stamps_data_owned_indexes: List[int] = []
    for i, stamp_item in enumerate(my_data):
        item_slug = stamp_item["item_slug"]
        for j, stamp_info in enumerate(stamps_data):
            if stamp_info["slug"] == item_slug:
                stamps_data_owned_indexes.append(j)
                break
        else:
            print(f"[WARN] stamp {item_slug} not found in the STAMPS INFO data")

    diff_count = len(stamps_data_owned_indexes) - len(my_current_stamps_in_db)
    if diff_count == 0:
        print("No differences found")
        sys.exit(0)

    print(f"Differences found: {diff_count}")

    stamp_similarities: Dict[int, float] = {}
    for index in stamps_data_owned_indexes:
        stamp_info = stamps_data[index]
        owned_stamp_name: str = stamp_info["name"]

        if owned_stamp_name in ignored_stamps:
            print(f"[IGNORED] {owned_stamp_name}")
            continue

        stamp_similarities.clear()
        for i, stamp_name in enumerate(my_current_stamps_in_db):
            similarity_score = measure_similarity(owned_stamp_name, stamp_name)
            if similarity_score == 1.0:
                print(f"[FOUND] {owned_stamp_name}")
                break
            stamp_similarities[i] = similarity_score
        else:
            print(f"[NOT FOUND] {owned_stamp_name}")
            similarities_sorted = sorted(
                stamp_similarities,
                key=stamp_similarities.get,
                reverse=True,
            )
            for j, s_index in enumerate(similarities_sorted):
                print(
                    f'Option [{j}]: with similarity = {stamp_similarities[s_index]:.2f}, name = "{my_current_stamps_in_db[s_index]}"'
                )
                g_input = input("show next [Y/n]: ")
                if g_input.lower() == "n":
                    break
