using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CheckPoint : MonoBehaviour
{
    public AudioClip CheckPointSE;

    void OnTriggerEnter(Collider other)
    {
        AudioSource.PlayClipAtPoint(CheckPointSE, other.gameObject.transform.position);
        transform.parent.GetComponent<LevelManager>().LoadCheckPoint();
    }
}
