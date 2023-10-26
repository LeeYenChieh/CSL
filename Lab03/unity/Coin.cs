using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Coin : MonoBehaviour
{
    public float Speed;
    public AudioClip CoinSE;
    public ParticleSystem CoinVFX;
    private bool _isCollected = false;

    void Start()
    {

    }

    void Update()
    {
        transform.Rotate(Vector3.up * Speed * Time.deltaTime);
    }
    private void OnTriggerEnter(Collider other)
    {
        Renderer coinVisual = transform.GetComponent<Renderer>();
        var emission = CoinVFX.emission;
        var duration = CoinVFX.main.duration;
        if (!_isCollected)
        {
            _isCollected = true;
            emission.enabled = true;
            CoinVFX.Play();
            AudioSource.PlayClipAtPoint(CoinSE, other.gameObject.transform.position);
            coinVisual.enabled = false;
            Invoke("DestroyObj", duration);
        }
    }

    private void DestroyObj()
    {
        Destroy(gameObject);
    }
}

