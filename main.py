import subprocess
import time

import requests
from tqdm import tqdm


def get_extensions() -> list[str]:
    extensions = subprocess.run(
        ["code", "--list-extensions"],
        capture_output=True,
        text=True,
        check=True,
        shell=True,
    )
    return extensions.stdout.splitlines()


def get_risk_for_extension(extension: str) -> dict:
    url = "https://app.extensiontotal.com/api/getExtensionRisk"
    headers = {"Content-Type": "application/json", "Cookie": "SameSite=None"}
    payload = {"q": extension}
    response = requests.post(url, json=payload, headers=headers, timeout=5)
    response.raise_for_status()
    return response.json()


def main() -> None:
    list_of_extensions = get_extensions()
    extension_risks = []

    for extension in tqdm(list_of_extensions):
        risk_info = get_risk_for_extension(extension)
        extension_risks.append(risk_info)
        time.sleep(2)

    sorted_risks = sorted(extension_risks, key=lambda x: x["risk"], reverse=True)

    print(
        "{:<40} {:<10} {:<10} {:<20}".format(
            "Extension", "Version", "Risk", "Updated At"
        )
    )
    for risk_info in sorted_risks:
        print(
            "{:<40} {:<10} {:<10} {:<20}".format(
                risk_info["display_name"],
                risk_info["version"],
                risk_info["risk"],
                risk_info["updated_at"],
            )
        )


if __name__ == "__main__":
    main()
