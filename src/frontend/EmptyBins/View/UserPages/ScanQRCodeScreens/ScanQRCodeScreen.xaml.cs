using System.ComponentModel;
using System.Reflection.Emit;
using System.Runtime.CompilerServices;
using EmptyBins.Models;
using EmptyBins.Services;
using Microsoft.Maui.ApplicationModel;
using QRCoder;
 // Note: Usage might be restricted based on platform in .NET MAUI

namespace EmptyBins.View.UserPages;

public partial class ScanQRCodeScreen : ContentPage
{
    private UserDataService userManager;
    private UserData userData;
    public ScanQRCodeScreen()
    {
        userManager = new UserDataService();
     
        InitializeComponent();
      
    }

    private void GenerateAndDisplayQRCode(string content)
    {
        QRCodeGenerator qrGenerator = new QRCodeGenerator();
        QRCodeData qrCodeData = qrGenerator.CreateQrCode(content, QRCodeGenerator.ECCLevel.Q);
        using (PngByteQRCode qrCode = new PngByteQRCode(qrCodeData)) // Using PngByteQRCode to comply with MAUI
        {
            byte[] qrCodeBytes = qrCode.GetGraphic(20);
            DisplayQRCode(qrCodeBytes);
        }
    }
    protected override async void OnAppearing()
    {
        base.OnAppearing();
        await FetchUser();
        GenerateAndDisplayQRCode(userData.id.ToString());

    }

    private async Task FetchUser()
    {
        userData = await userManager.GetUserDataAsync();
    }

    private void DisplayQRCode(byte[] qrCodeBytes)
    {
        Stream stream = new MemoryStream(qrCodeBytes);
        Image qrImage = new Image
        {
            Source = ImageSource.FromStream(() => stream),
            VerticalOptions = LayoutOptions.Center,
            HorizontalOptions = LayoutOptions.Center,
            WidthRequest = 250,  
            HeightRequest = 250
        };
        var mainLayout = this.FindByName<VerticalStackLayout>("MainLayout");
        mainLayout.Children.Insert(0, qrImage);
        //this.Content = qrImage; // Set the Page's Content to the QR Image, or add it to an existing layout
    }

    private async void BackButton_Clicked(object sender, EventArgs e)
    {
        // Navigate back to the previous page
        await Navigation.PushAsync(new UserHomeScreen());
    }
}
