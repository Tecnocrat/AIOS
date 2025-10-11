using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using AIOS.Services;

namespace AIOS.UI
{
    internal static class HeadlessHost
    {
        public static async Task RunAsync(string logFile, CancellationToken token)
        {
            SafeLog(logFile, "HeadlessHost.RunAsync starting.");
            var ai = new AIServiceManager();
            var maint = new MaintenanceService();
            int iteration = 0;
            while (!token.IsCancellationRequested)
            {
                try
                {
                    var health = await ai.GetSystemHealthAsync();
                    var maintStatus = await maint.GetMaintenanceStatusAsync();
                    SafeLog(logFile, $"tick={iteration} health={health.HealthStatus} score={health.HealthScore:F2} maintDocs={maintStatus.DocumentationFragmentation}");
                }
                catch (Exception ex)
                {
                    SafeLog(logFile, "tick_error=" + ex.GetType().Name + ":" + ex.Message);
                }
                iteration++;
                await Task.Delay(TimeSpan.FromSeconds(10), token).ContinueWith(_ => { });
            }
            SafeLog(logFile, "HeadlessHost.RunAsync stopping.");
        }

        private static void SafeLog(string path, string line)
        {
            try
            {
                Directory.CreateDirectory(Path.GetDirectoryName(path)!);
                File.AppendAllText(path, DateTime.UtcNow.ToString("o") + " " + line + Environment.NewLine);
            }
            catch { }
        }
    }
}
