using UnityEngine;

namespace Guidance.Runtime
{
    /// <summary>
    /// Lightweight composition root that wires runtime modules for the guidance app.
    /// </summary>
    public sealed class AppRuntimeContext
    {
        public SessionClient SessionClient { get; }
        public StepCoordinator StepCoordinator { get; }
        public AssetCache AssetCache { get; }
        public TargetPayloadCache TargetPayloadCache { get; }
        public TargetManager TargetManager { get; }
        public TelemetryClient TelemetryClient { get; }
        public DiagnosticsBundleExporter DiagnosticsExporter { get; }
        public StepAssetManifestClient ManifestClient { get; }
        public ModelPresenter ModelPresenter { get; }
#if !UNITY_ANDROID
        public GrpcAssetTransferClient GrpcAssetTransfer { get; }
#endif

        public AppRuntimeContext(
            SessionClient sessionClient,
            StepCoordinator stepCoordinator,
            AssetCache assetCache,
            TargetPayloadCache targetPayloadCache,
            TargetManager targetManager,
            TelemetryClient telemetryClient,
            DiagnosticsBundleExporter diagnosticsExporter,
            StepAssetManifestClient manifestClient,
            ModelPresenter modelPresenter
#if !UNITY_ANDROID
            , GrpcAssetTransferClient grpcAssetTransfer = null
#endif
            )
        {
            SessionClient = sessionClient;
            StepCoordinator = stepCoordinator;
            AssetCache = assetCache;
            TargetPayloadCache = targetPayloadCache;
            TargetManager = targetManager;
            TelemetryClient = telemetryClient;
            DiagnosticsExporter = diagnosticsExporter;
            ManifestClient = manifestClient;
            ModelPresenter = modelPresenter;
#if !UNITY_ANDROID
            GrpcAssetTransfer = grpcAssetTransfer;
#endif
        }

        /// <summary>
        /// Creates a default runtime graph with either native gRPC or HTTP bridge transport.
        /// </summary>
        public static AppRuntimeContext CreateDefault(
    bool useNativeGrpcTransport,
    string grpcTarget,
    string httpBridgeBaseUrl,
    bool supportsDraco, Transform modelAnchor = null)
        {
            ISessionTransport transport;
#if !UNITY_ANDROID
            if (useNativeGrpcTransport)
            {
                transport = new GrpcSessionTransport(
                    target: grpcTarget,
                    deviceId: SystemInfo.deviceUniqueIdentifier,
                    appVersion: Application.version
                );
            }
            else
#endif
            {
                transport = new HttpBridgeSessionTransport(
                    baseUrl: httpBridgeBaseUrl,
                    deviceId: SystemInfo.deviceUniqueIdentifier,
                    appVersion: Application.version
                );
            }

#if !UNITY_ANDROID
            GrpcAssetTransferClient grpcAssetTransfer = useNativeGrpcTransport
                ? new GrpcAssetTransferClient(grpcTarget)
                : null;
#endif

            return new AppRuntimeContext(
                sessionClient: new SessionClient(supportsDraco: supportsDraco, transport: transport),
                stepCoordinator: new StepCoordinator(),
                assetCache: new AssetCache(),
                targetPayloadCache: new TargetPayloadCache(),
                targetManager: new TargetManager(),
                telemetryClient: new TelemetryClient(),
                diagnosticsExporter: new DiagnosticsBundleExporter(),
                manifestClient: new StepAssetManifestClient(httpBridgeBaseUrl),
                modelPresenter: new ModelPresenter(modelAnchor)
#if !UNITY_ANDROID
                , grpcAssetTransfer: grpcAssetTransfer
#endif
            );
        }

    }
}
