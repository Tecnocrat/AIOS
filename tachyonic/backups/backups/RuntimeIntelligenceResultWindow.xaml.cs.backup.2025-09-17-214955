using System.Windows;
using AIOS.Models;
using AIOS.Services;

namespace AIOS.UI.Controls
{
    /// <summary>
    /// Interaction logic for RuntimeIntelligenceResultWindow.xaml
    /// </summary>
    public partial class RuntimeIntelligenceResultWindow : Window
    {
        public RuntimeIntelligenceResultWindow()
        {
            InitializeComponent();
        }

        public void DisplayResult(RuntimeIntelligenceResult result)
        {
            // Display the result in the window
            // This method will be called from the main control
            DataContext = result;
        }

        private void CloseButton_Click(object sender, RoutedEventArgs e)
        {
            Close();
        }
    }
}