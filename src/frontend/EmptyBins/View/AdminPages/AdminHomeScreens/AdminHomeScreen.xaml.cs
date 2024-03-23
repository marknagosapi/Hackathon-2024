namespace EmptyBins.View.AdminPages.AdminHomeScreens;
using EmptyBins.View.AuthPages;

public partial class AdminHomeScreen : ContentPage
{
	public AdminHomeScreen()
	{
		InitializeComponent();
	}

    private async void OnLogOutClicked(object sender, EventArgs e)
    {
        // Navig�l�s a ScanQRCodeScreen-re
        await Navigation.PushAsync(new LoginScreen());
    }
}