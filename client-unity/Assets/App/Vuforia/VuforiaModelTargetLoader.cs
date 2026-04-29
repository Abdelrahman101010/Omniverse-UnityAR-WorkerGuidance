using System;
using System.Collections;
using System.IO;
using UnityEngine;

#if VUFORIA_ENGINE
using Vuforia;
#endif

namespace Guidance.Runtime
{
    /// <summary>
    /// Loads a Vuforia Model Target database downloaded at runtime from the FastAPI server.
    /// Uses VuforiaBehaviour.Instance.ObserverFactory.CreateModelTarget — the official
    /// Vuforia Engine 11 API for runtime dataset loading (replaces the removed ObjectTracker/DataSet API).
    /// </summary>
    public static class VuforiaModelTargetLoader
    {
#if VUFORIA_ENGINE
        public static IEnumerator LoadModelTargetDatabaseAsync(
            string datFilePath,
            string targetNameFallback,
            Action<ObserverBehaviour> onLoaded,
            Action<string> onError)
        {
            if (string.IsNullOrEmpty(datFilePath))
            {
                onError?.Invoke("VuforiaModelTargetLoader: datFilePath is null or empty");
                yield break;
            }

            var xmlPath = Path.ChangeExtension(datFilePath, ".xml");
            var datPath = Path.ChangeExtension(datFilePath, ".dat");

            if (!File.Exists(xmlPath) || !File.Exists(datPath))
            {
                onError?.Invoke(
                    $"VuforiaModelTargetLoader: files missing — " +
                    $"xml={File.Exists(xmlPath)} dat={File.Exists(datPath)} ({xmlPath})");
                yield break;
            }

            var exactTargetName = ExtractTargetNameFromXml(xmlPath, targetNameFallback);

            bool done = false;
            string capturedError = null;
            ObserverBehaviour capturedObserver = null;

            void TryCreate()
            {
                // If a ModelTargetBehaviour already exists in the scene (e.g. the static
                // StreamingAssets one), reuse it — Vuforia throws if you try to create a
                // second observer for the same database name.
                var existing = UnityEngine.Object.FindFirstObjectByType<ModelTargetBehaviour>();
                if (existing != null)
                {
                    Debug.Log($"[VuforiaModelTargetLoader] Reusing existing scene observer '{existing.TargetName}'");
                    capturedObserver = existing;
                    done = true;
                    return;
                }

                try
                {
                    var modelTarget = VuforiaBehaviour.Instance.ObserverFactory
                        .CreateModelTarget(xmlPath, exactTargetName);
                    if (modelTarget != null)
                    {
                        Debug.Log($"[VuforiaModelTargetLoader] Runtime target created: '{modelTarget.TargetName}' from {xmlPath}");
                        capturedObserver = modelTarget;
                    }
                    else
                    {
                        capturedError = $"VuforiaModelTargetLoader: CreateModelTarget returned null for '{exactTargetName}'";
                    }
                }
                catch (Exception ex)
                {
                    capturedError = $"VuforiaModelTargetLoader: {ex.Message}";
                }
                done = true;
            }

            if (VuforiaApplication.Instance.IsInitialized)
            {
                TryCreate();
            }
            else
            {
                VuforiaApplication.Instance.OnVuforiaStarted += TryCreate;

                float waited = 0f;
                while (!done && waited < 10f)
                {
                    yield return null;
                    waited += Time.deltaTime;
                }

                VuforiaApplication.Instance.OnVuforiaStarted -= TryCreate;

                if (!done)
                {
                    onError?.Invoke("VuforiaModelTargetLoader: timed out waiting for Vuforia (10s)");
                    yield break;
                }
            }

            if (capturedError != null)
                onError?.Invoke(capturedError);
            else
                onLoaded?.Invoke(capturedObserver);
        }

        private static string ExtractTargetNameFromXml(string xmlPath, string fallback)
        {
            try
            {
                var content = File.ReadAllText(xmlPath);
                const string tag = "<ModelTarget name=\"";
                int start = content.IndexOf(tag, StringComparison.Ordinal);
                if (start >= 0)
                {
                    start += tag.Length;
                    int end = content.IndexOf('"', start);
                    if (end > start) return content.Substring(start, end - start);
                }
            }
            catch { }
            return fallback;
        }

#else
        public static IEnumerator LoadModelTargetDatabaseAsync(
            string datFilePath,
            string targetNameFallback,
            Action<UnityEngine.Object> onLoaded,
            Action<string> onError)
        {
            Debug.LogWarning("[VuforiaModelTargetLoader] VUFORIA_ENGINE not defined — skipped.");
            onLoaded?.Invoke(null);
            yield break;
        }
#endif
    }
}
