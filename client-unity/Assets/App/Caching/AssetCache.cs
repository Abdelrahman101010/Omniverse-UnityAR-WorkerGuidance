using System;
using System.Collections;
using System.IO;
using UnityEngine;
using UnityEngine.Networking;

namespace Guidance.Runtime
{
    /// <summary>
    /// Downloads and caches immutable step assets by asset version.
    /// </summary>
    public sealed class AssetCache
    {
        private readonly string _cacheRoot;

        public AssetCache(string cacheRoot = null)
        {
            _cacheRoot = string.IsNullOrEmpty(cacheRoot)
                ? Path.Combine(Application.persistentDataPath, "guidance-cache")
                : cacheRoot;
            Directory.CreateDirectory(_cacheRoot);
        }

        public bool TryGetCachedFile(string assetVersion, string fileName, out string fullPath)
        {
            fullPath = GetAssetPath(assetVersion, fileName);
            return File.Exists(fullPath);
        }

        public IEnumerator GetOrDownloadFile(
            string url,
            string assetVersion,
            string fileName,
            Action<string> onReady,
            Action<string> onError)
        {
            if (TryGetCachedFile(assetVersion, fileName, out var cachedPath))
            {
                onReady?.Invoke(cachedPath);
                yield break;
            }

            Debug.Log($"[AssetCache] Downloading {fileName} from {url}");
            using var request = UnityWebRequest.Get(url);
            request.timeout = 180;
            yield return request.SendWebRequest();

            if (request.result != UnityWebRequest.Result.Success)
            {
                onError?.Invoke($"Asset download failed [{request.responseCode}] {request.error} — url={url}");
                yield break;
            }

            var outputPath = GetAssetPath(assetVersion, fileName);
            Directory.CreateDirectory(Path.GetDirectoryName(outputPath) ?? _cacheRoot);
            File.WriteAllBytes(outputPath, request.downloadHandler.data);
            Debug.Log($"[AssetCache] Cached {fileName} ({request.downloadHandler.data.Length / 1024}KB) → {outputPath}");
            onReady?.Invoke(outputPath);
        }

        private string GetAssetPath(string assetVersion, string fileName)
        {
            var safeVersion = (assetVersion ?? "unknown").Replace(":", "_");
            return Path.Combine(_cacheRoot, safeVersion, fileName);
        }
    }
}
