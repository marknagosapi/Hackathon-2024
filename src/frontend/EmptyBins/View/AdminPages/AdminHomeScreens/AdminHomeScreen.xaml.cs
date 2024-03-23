namespace EmptyBins.View.AdminPages.AdminHomeScreens;
using EmptyBins.View.AuthPages;
using EmptyBins.View.AdminPages.CameraScreens;


public partial class AdminHomeScreen : ContentPage
{
    public AdminHomeScreen()
    {
        InitializeComponent();
    }

    private async void OnLogOutClicked(object sender, EventArgs e)
    {
        await Navigation.PushAsync(new LoginScreen());
    }

    // Add this method
    private async void OnScanQRCodeClicked(object sender, EventArgs e)
    {
        // Navigate to CameraScreen for QR code scanning
        await Navigation.PushAsync(new CameraScreens());
    }
}
