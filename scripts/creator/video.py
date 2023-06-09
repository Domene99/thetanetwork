import requests


class ThethaVideoWrapper:
    def __init__(self, sa_id, sa_secret, data):
        self.sa_id = sa_id
        self.sa_secret = sa_secret
        self.data = data
        self.headers_theta = {"x-tva-sa-id": self.sa_id, "x-tva-sa-secret": self.sa_secret}
        self.create_uri = "https://api.thetavideoapi.com/upload"
        self.transcode_uri = "https://api.thetavideoapi.com/video"
    
    def createUploadId(self):
        response = requests.post(self.create_uri, headers=self.headers_theta)
        # print(response.json())
        self.url_id = response.json()["body"]["uploads"][0]["id"]
        self.presigned_url = response.json()["body"]["uploads"][0]["presigned_url"]
    
    def upload(self):
        requests.put(self.presigned_url,
                                headers = {"Content-Type": "application/octet-stream"},
                                data = self.data)
    
    def transcode(self):
        self.headers_theta["Content-Type"] = "application/json"
        response = requests.post(self.transcode_uri, 
                             json = {"source_upload_id": self.url_id, "playback_policy":"public"},
                             headers = self.headers_theta)
        print(response.json())
        self.play_id = response.json()["body"]["videos"][0]["id"]
    
    def waitForPlaybackUrl(self):
        url = "https://api.thetavideoapi.com/video/" + self.play_id
        response = requests.get(url, headers = self.headers_theta)
        if response.json()["body"]["videos"][0]["state"] == "error":
            return False
        if response.json()["body"]["videos"][0]["state"] != "success":
            return self.waitForPlaybackUrl()
        self.player_url = response.json()["body"]["videos"][0]["player_uri"]
        self.playback_url = response.json()["body"]["videos"][0]["playback_uri"]
        return True