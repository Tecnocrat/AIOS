using System;
using System.Linq;
using System.Reflection;
using System.Windows;
namespace AIOS.UI.Diagnostics {
  internal static class Program {
    [STAThread]
    static int Main(string[] args) {
      try {
        var asm = Assembly.Load("AIOS.UI");
        var windowTypes = asm.GetTypes().Where(t => t.IsSubclassOf(typeof(Window))).ToList();
        Console.WriteLine($"WINDOW_COUNT={windowTypes.Count}");
        foreach(var wt in windowTypes) Console.WriteLine("WINDOW_TYPE="+wt.FullName);
        // Instantiate first window in hidden mode
        if(windowTypes.Count>0) {
          var w = (Window)Activator.CreateInstance(windowTypes[0])!;
          Console.WriteLine("INSTANTIATED="+w.GetType().FullName);
          w.SourceInitialized += (_,__) => { Console.WriteLine("SOURCE_INITIALIZED"); w.Close(); };
          var app = new Application();
          app.Startup += (_,__) => { app.ShutdownMode = ShutdownMode.OnExplicitShutdown; app.Dispatcher.InvokeAsync(() => { /* noop */ }); };
          app.Run(w);
        }
        Console.WriteLine("HARNESS_SUCCESS");
        return 0;
      } catch(Exception ex) {
        Console.WriteLine("HARNESS_ERROR="+ex.GetType().Name+":"+ex.Message);
        return 1;
      }
    }
  }
}
