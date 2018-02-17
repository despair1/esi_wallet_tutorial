import oauth_models
import requests
import config_init

configuration = config_init.config_init


def refresh_token(r_token):
    r = requests.post(configuration.get("refresh_token_url"),
                      auth=(
                          configuration.get("ClientID"),
                          configuration.get("SecretKey")
                      ),
                      data={"grant_type": "refresh_token",
                            "refresh_token": r_token})
    print(r.status_code)
    print(r.text)
    return r.json()


for i in oauth_models.Tokens.select():
    resp = refresh_token(i.refresh_token)
    i.access_token = resp["access_token"]
    i.save()

