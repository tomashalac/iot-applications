using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class IoT : MonoBehaviour {

    public string Token = "Fl401z1mzl074xj1lzdm4slslL2iO";
    public string URL = "https://povyqz20wl.execute-api.us-east-1.amazonaws.com/prod/HttpIoT";

    private string url => URL + "?token=" + Token + "&command=";

    public GameObject On, Off, ToDesactivate;
    
	void Start () {
        StartCoroutine(GetText());
    }
    
    public void SendCommand(string command) {
        Debug.Log("The following command was sent to the light: " + command);
        var request = new UnityWebRequest(url + command);
        request.SendWebRequest();
    }
    

    IEnumerator GetText() {
        UnityWebRequest request = UnityWebRequest.Get(url + "ping");
        yield return request.SendWebRequest();

        if (request.isNetworkError || request.isHttpError) {
            Debug.Log(request.error);
        } else {
            string text = request.downloadHandler.text;
            Debug.Log("The state of light was received which is: " + text);

            ToDesactivate.SetActive(false);

            if(text == "True") {
                SetOn(true);
            }else if(text == "False") {
                SetOn(false);
            } else {
                Debug.LogError(text);
            }

        }
    }

    private void SetOn(bool on) {
        On.SetActive(on);
        Off.SetActive(!on);
    }
}
