using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    // Player Property Variable
    private Rigidbody _rb;

    // Forward Speed Variables
    private float _currentSpeed = 0f;
    [Tooltip("The maximum forward speed the kart can reach.")]
    public float MaxSpeed;
    [Tooltip("The minimum backward speed the kart can reach.")]
    public float MinSpeed;
    [Tooltip("The acceleration")]
    public float Acceleration;

    // Rotate Speed Variables
    Vector3 _turnAngle;
    [Tooltip("Max angular speed for rotations.")]
    public float MaxRotationAngle;
    [Tooltip("Rotation Speed.")]
    public float RotationSpeed;
    [Tooltip("Hand use to show rotations.")]
    public Transform Hands;
    [Tooltip("Front left wheel.")]
    public Transform FrontLeftWheel;
    [Tooltip("Front right wheel.")]
    public Transform FrontRightWheel;

    // Start is called before the first frame update
    void Start()
    {
        _rb = GetComponent<Rigidbody>();   
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        Steer();
        Move();
    }

    void Move()
    {
        if(Input.GetKey(KeyCode.W))
        {
            _currentSpeed = Mathf.Lerp(_currentSpeed, MaxSpeed, Time.fixedDeltaTime * Acceleration * 1f);
        }
        else if(Input.GetKey(KeyCode.S))
        {
            _currentSpeed = Mathf.Lerp(_currentSpeed, MinSpeed, Time.fixedDeltaTime * Acceleration * 2f);
        }
        else
        {
            _currentSpeed = Mathf.Lerp(_currentSpeed, 0, Time.fixedDeltaTime * Acceleration * 6f);
        }
        
        RotateRigidbody();

        Vector3 vel = transform.forward * _currentSpeed;
        vel.y = _rb.velocity.y;
        _rb.velocity = vel;
    }
    
    float RegularizeAngle(float angle)
    {
        // equivalent to angle = (angle + 540) % 360 - 180;
        angle = (angle > 180) ? angle - 360 : angle;
        angle = (angle < -180) ? angle + 360 : angle;
        return angle;
    }

    private void RotateVisual(float targetAngle, float rotateSpeed)
    {
        float handAngle = RegularizeAngle(Hands.localRotation.eulerAngles.z);
        float wheelAngle = RegularizeAngle(FrontLeftWheel.localRotation.eulerAngles.y);

        Hands.Rotate(0, 0, (targetAngle - handAngle) * Time.fixedDeltaTime * rotateSpeed, Space.Self);
        FrontLeftWheel.Rotate(0, (-targetAngle - wheelAngle) * Time.fixedDeltaTime * rotateSpeed, 0, Space.Self);
        FrontRightWheel.Rotate(0, (-targetAngle - wheelAngle) * Time.fixedDeltaTime * rotateSpeed, 0, Space.Self);
    }

    private void Steer()
    {
        if(Input.GetKey(KeyCode.A))
        {
            RotateVisual(MaxRotationAngle, RotationSpeed * 1f);
        }
        else if(Input.GetKey(KeyCode.D))
        {
            RotateVisual(-MaxRotationAngle, RotationSpeed * 1f);
        }
        else
        {
            RotateVisual(0, RotationSpeed * 3f);
        }
    }

    private void RotateRigidbody()
    {
        _turnAngle = FrontLeftWheel.eulerAngles - transform.eulerAngles;
        _turnAngle.y = RegularizeAngle(_turnAngle.y);
        Quaternion deltaRotation = Quaternion.Euler(Mathf.Sign(_currentSpeed) * _turnAngle * Time.fixedDeltaTime);
        _rb.MoveRotation(_rb.rotation * deltaRotation);
    }
}
