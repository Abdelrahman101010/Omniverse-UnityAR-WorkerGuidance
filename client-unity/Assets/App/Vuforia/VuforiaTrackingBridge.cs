using UnityEngine;

#if VUFORIA_ENGINE
using Vuforia;
#endif

namespace Guidance.Runtime
{
    public sealed class VuforiaTrackingBridge : MonoBehaviour
    {
        [SerializeField] private AppBootstrap appBootstrap;

#if VUFORIA_ENGINE
        private ObserverBehaviour _observerBehaviour;

        private void Awake()
        {
            if (appBootstrap == null)
                appBootstrap = FindFirstObjectByType<AppBootstrap>();
        }

        private void OnDisable()
        {
            if (_observerBehaviour != null)
                _observerBehaviour.OnTargetStatusChanged -= HandleTargetStatusChanged;
        }

        public void AssignObserver(ObserverBehaviour newObserver)
        {
            if (_observerBehaviour == newObserver) return;
            if (_observerBehaviour != null)
                _observerBehaviour.OnTargetStatusChanged -= HandleTargetStatusChanged;
            _observerBehaviour = newObserver;
            if (_observerBehaviour != null && isActiveAndEnabled)
                _observerBehaviour.OnTargetStatusChanged += HandleTargetStatusChanged;
        }

        private void HandleTargetStatusChanged(ObserverBehaviour behaviour, TargetStatus status)
        {
            if (appBootstrap == null) return;
            var tracked = status.Status == Status.TRACKED
                       || status.Status == Status.EXTENDED_TRACKED
                       || status.Status == Status.LIMITED;
            var pose = behaviour != null ? behaviour.transform : transform;
            appBootstrap.OnTargetTrackingUpdated(pose.position, pose.rotation, tracked);
        }
#else
        private void Awake()
        {
            if (appBootstrap == null)
                appBootstrap = FindFirstObjectByType<AppBootstrap>();
        }
#endif
    }
}
