using System;
using System.Configuration;
using System.Data;
using System.IO;
using System.Threading;
using System.Windows;
using System.Windows.Threading;

namespace AIOS.UI;

/// <summary>
/// Interaction logic for App.xaml
/// </summary>
public partial class App : Application
{
	private string _logDir = Path.Combine("runtime_intelligence", "logs", "ui");
	private string _logFile => Path.Combine(_logDir, "ui_startup.log");
	private bool _headlessMode;

	protected override void OnStartup(StartupEventArgs e)
	{
		// Determine headless flag early
		_headlessMode = Array.Exists(e.Args, a => string.Equals(a, "--headless", StringComparison.OrdinalIgnoreCase));

		Directory.CreateDirectory(_logDir);
		SafeLog("=== UI STARTUP === " + DateTime.UtcNow.ToString("o"));
		SafeLog("Args: " + string.Join(" ", e.Args));

		// Global exception handlers
		this.DispatcherUnhandledException += OnDispatcherUnhandledException;
		AppDomain.CurrentDomain.UnhandledException += OnDomainUnhandledException;
		TaskScheduler.UnobservedTaskException += OnUnobservedTaskException;

		// If in explicit headless mode or GUI environment unavailable, start headless loop
		if (_headlessMode || !Environment.UserInteractive)
		{
			SafeLog("Entering headless fallback mode (UserInteractive=" + Environment.UserInteractive + ")");
			// Prevent WPF from auto-shutting down because no window is created
			this.ShutdownMode = ShutdownMode.OnExplicitShutdown;
			_ = global::AIOS.UI.HeadlessHost.RunAsync(_logFile, CancellationToken.None);
			// Do not call base (prevents default StartupUri handling) – keep process alive
			return; // process stays via background loop (RunAsync has its own keep-alive timer)
		}

		try
		{
			base.OnStartup(e); // will create window via StartupUri
			SafeLog("StartupUri window created.");
		}
		catch (Exception ex)
		{
			SafeLog("Window creation failed: " + ex.GetType().Name + ": " + ex.Message);
			// Fallback: launch headless mode instead of immediate process exit
			SafeLog("Fallback to headless loop after window creation failure.");
			_ = global::AIOS.UI.HeadlessHost.RunAsync(_logFile, CancellationToken.None);
		}
	}

	private void OnDispatcherUnhandledException(object sender, DispatcherUnhandledExceptionEventArgs e)
	{
		SafeLog("[DispatcherUnhandledException] " + e.Exception);
		e.Handled = true; // prevent crash
	}

	private void OnDomainUnhandledException(object? sender, UnhandledExceptionEventArgs e)
	{
		SafeLog("[DomainUnhandledException] " + e.ExceptionObject);
	}

	private void OnUnobservedTaskException(object? sender, UnobservedTaskExceptionEventArgs e)
	{
		SafeLog("[UnobservedTaskException] " + e.Exception);
		e.SetObserved();
	}

	private void SafeLog(string line)
	{
		try
		{
			File.AppendAllText(_logFile, line + Environment.NewLine);
		}
		catch { /* ignore logging failures */ }
	}
}

