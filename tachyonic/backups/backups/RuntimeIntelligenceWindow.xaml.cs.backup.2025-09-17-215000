using System;
using System.Threading.Tasks;
using System.Windows;
using AIOS.UI.Controls;

namespace AIOS.UI
{
    public partial class RuntimeIntelligenceWindow : Window
    {
        public RuntimeIntelligenceWindow()
        {
            InitializeComponent();
            InitializeAsync();
        }

        private async void InitializeAsync()
        {
            try
            {
                // Update status to show initialization
                UpdateStatus("Initializing Runtime Intelligence...", false);
                
                // Initialize the Runtime Intelligence control
                await RuntimeControl.InitializeAsync();
                
                // Update status to show ready state
                UpdateStatus("Active", true);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error initializing Runtime Intelligence: {ex.Message}", 
                               "Initialization Error", MessageBoxButton.OK, MessageBoxImage.Error);
                UpdateStatus("Error", false);
            }
        }

        private void UpdateStatus(string statusText, bool isActive)
        {
            StatusText.Text = statusText;
            StatusIndicator.Fill = isActive ? 
                System.Windows.Media.Brushes.LimeGreen : 
                System.Windows.Media.Brushes.Orange;
        }

        private void CloseButton_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
        }

        protected override void OnClosed(EventArgs e)
        {
            // Clean up any ongoing operations
            RuntimeControl?.Dispose();
            base.OnClosed(e);
        }
    }
}