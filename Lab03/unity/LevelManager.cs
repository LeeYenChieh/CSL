using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;
using UnityEngine.UI;

public class LevelManager : MonoBehaviour
{
    [Tooltip("The start/finish line")]
    public GameObject StartFinishLine;
    [Tooltip("The list of checkpoints")]
    public GameObject[] CheckPointList;

    private int _gameState = -1;
    int _checkPointNow;
    Collider _startLineCollider;

    float _startTime;
    bool _isPlaying = false;
    public Text TimerText;

    // Start is called before the first frame update
    void Start()
    {
        _checkPointNow = CheckPointList.Count();
        for(int i = 0; i < _checkPointNow; i++)
        {
            CheckPointList[i].SetActive(false);
        }

        _startLineCollider = StartFinishLine.GetComponent<Collider>();
    }

    void Update()
    {
        if(_isPlaying)
        {
            UpdateTimer();
        }
    }

    public void LoadCheckPoint()
    {
        if(_gameState == -1)
        {
            _startTime = Time.time;
            _isPlaying = true;
            _startLineCollider.enabled = false;
        }
        else if(_gameState == _checkPointNow)  
        {
            Debug.Log("Finish!");
            _isPlaying = false;
            _startLineCollider.enabled = false;
            return;
        }
        else
        {
            Debug.Log(_gameState);
            CheckPointList[_gameState].SetActive(false);
        }

        _gameState++;

        if(_gameState == _checkPointNow)
        {
            _startLineCollider.enabled = true;
        }
        else
        {
            CheckPointList[_gameState].SetActive(true);
        }
    }

    void UpdateTimer()
    {
        float currentTime = Time.time - _startTime;
        currentTime = Mathf.Max(0, currentTime);
        float minutes = (int)(currentTime / 60);
        float seconds = currentTime % 60;
        TimerText.text = string.Format("{0:0}:{1:00.00}", minutes, seconds);
    }
}
