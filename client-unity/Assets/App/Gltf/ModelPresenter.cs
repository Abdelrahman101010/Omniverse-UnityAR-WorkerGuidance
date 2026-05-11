using System.IO;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;

namespace Guidance.Runtime
{
    /// <summary>
    /// Owns one-active-model lifecycle and dispatches model loading to available loaders.
    /// </summary>
    public sealed class ModelPresenter
    {
        private GameObject _activeModelRoot;
        private CancellationTokenSource _loadCts;
        private readonly List<IModelLoader> _loaders;

        public ModelPresenter()
        {
            _loaders = new List<IModelLoader>
            {
                new GltfFastModelLoader(),
                new PrimitiveFallbackModelLoader(),
            };
        }

        /// <summary>
        /// Synchronous model presentation kept for replay paths. Production step activations
        /// should use <see cref="PresentModelAsync"/> to avoid blocking the main thread.
        /// </summary>
        public void PresentModel(string modelFilePath, StepActivationDto activation, Vector3 positionOffset = default, float animationSpeed = 1f)
        {
            ClearActiveModel();

            if (string.IsNullOrEmpty(modelFilePath) || !File.Exists(modelFilePath))
            {
                Debug.LogWarning($"[ModelPresenter] Model file missing: {modelFilePath}");
                return;
            }

            _activeModelRoot = new GameObject($"Model_{activation.PartId}_{activation.StepId}");
            _activeModelRoot.transform.localPosition = positionOffset;

            IModelLoader selectedLoader = null;
            foreach (var loader in _loaders)
            {
                if (loader.CanLoad(modelFilePath))
                {
                    selectedLoader = loader;
                    break;
                }
            }

            if (selectedLoader == null)
            {
                Debug.LogWarning($"[ModelPresenter] No model loader available for {modelFilePath}");
                return;
            }

            selectedLoader.LoadModel(
                modelFilePath,
                _activeModelRoot.transform,
                error => Debug.LogWarning($"[ModelPresenter] Loader error: {error}")
            );

            ApplyAnimationSpeed(_activeModelRoot, animationSpeed);
            HologramApplier.Apply(_activeModelRoot.transform);
            Debug.Log($"[ModelPresenter] Presented model for step {activation.StepId} from {modelFilePath}");
        }

        /// <summary>
        /// Asynchronously loads and presents the model. Cancels any in-flight load from
        /// the previous step activation before starting a new one.
        /// </summary>
        /// <param name="parentTransform">
        /// Optional parent for the model root.  When a Vuforia <c>ObserverBehaviour</c>
        /// is provided here the model will move with the tracked physical object.
        /// Pass <c>null</c> to place the model at world origin (desktop test fallback).
        /// </param>
        public async Task PresentModelAsync(
            string modelFilePath,
            StepActivationDto activation,
            CancellationToken ct,
            Transform parentTransform = null,
            Vector3 positionOffset = default,
            float animationSpeed = 1f)
        {
            ClearActiveModel();

            if (string.IsNullOrEmpty(modelFilePath) || !File.Exists(modelFilePath))
            {
                Debug.LogWarning($"[ModelPresenter] Model file missing: {modelFilePath}");
                return;
            }

            _activeModelRoot = new GameObject($"Model_{activation.PartId}_{activation.StepId}");

            if (parentTransform != null)
            {
                _activeModelRoot.transform.SetParent(parentTransform, worldPositionStays: false);
                _activeModelRoot.transform.localPosition = positionOffset;
                _activeModelRoot.transform.localRotation = Quaternion.identity;
                _activeModelRoot.transform.localScale    = Vector3.one;
            }

            IModelLoader selectedLoader = null;
            foreach (var loader in _loaders)
            {
                if (loader.CanLoad(modelFilePath))
                {
                    selectedLoader = loader;
                    break;
                }
            }

            if (selectedLoader == null)
            {
                Debug.LogWarning($"[ModelPresenter] No model loader available for {modelFilePath}");
                return;
            }

            try
            {
                await selectedLoader.LoadModelAsync(modelFilePath, _activeModelRoot.transform, ct);
                ApplyAnimationSpeed(_activeModelRoot, animationSpeed);
                HologramApplier.Apply(_activeModelRoot.transform);
                Debug.Log($"[ModelPresenter] Async-loaded model for step {activation.StepId} from {modelFilePath}");
            }
            catch (TaskCanceledException)
            {
                Debug.Log($"[ModelPresenter] Load cancelled for step {activation.StepId}");
                ClearActiveModel();
            }
        }

        private static void ApplyAnimationSpeed(GameObject root, float speed)
        {
            foreach (var anim in root.GetComponentsInChildren<Animation>(includeInactive: true))
                foreach (AnimationState state in anim)
                    state.speed = speed;

            foreach (var animator in root.GetComponentsInChildren<Animator>(includeInactive: true))
                animator.speed = speed;
        }

        public void ClearActiveModel()
        {
            _loadCts?.Cancel();
            _loadCts?.Dispose();
            _loadCts = null;

            if (_activeModelRoot == null)
            {
                return;
            }

            Object.Destroy(_activeModelRoot);
            _activeModelRoot = null;
            Debug.Log("[ModelPresenter] Cleared active model");
        }
    }
}
