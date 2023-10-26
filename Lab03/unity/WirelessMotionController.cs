using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using UnityEngine;

public class WirelessMotionController : MonoBehaviour
{

    const string hostIP = "192.168.43.121";
    const int port = 80;

    private SocketClient socketClient;


    private void Awake() {
        socketClient = new SocketClient(hostIP, port);
    }

    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
       
    }

    void OnDestroy () {
        socketClient.Close();
    }
}
