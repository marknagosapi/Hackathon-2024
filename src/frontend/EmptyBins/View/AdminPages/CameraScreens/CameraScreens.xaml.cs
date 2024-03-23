using System;
using ZXing.Net.Maui.Controls;
using Microsoft.Maui.Controls;
using ZXing.Net.Maui;

namespace EmptyBins.View.AdminPages.CameraScreens;

using System;
using System.Net.Http;
using ZXing.Net.Maui.Controls;
using Microsoft.Maui.Controls;
using ZXing.Net.Maui;



public partial class CameraScreens : ContentPage
{
    private readonly HttpClient httpClient = new HttpClient();

    public CameraScreens()
    {
        InitializeComponent();
    }

    // Event handler for barcode detection
    private async void barcodeReader_BarcodeDetected(object sender, BarcodeDetectionEventArgs e)
    {
        // Assuming you want to handle the first detected barcode
        var firstBarcode = e.Results[0];
        if (firstBarcode != null)
        {
            // Perform your logic with the detected barcode
            var userId = firstBarcode.Value; // Assuming the barcode value is the user ID

            try
            {
                var response = await httpClient.GetStringAsync($"http://localhost:8000/admin/scan_qr/?user_id={userId}");
                // Handle the response here
                Device.BeginInvokeOnMainThread(async () =>
                {
                    await DisplayAlert("User Data", response, "OK");
                });
            }
            catch (Exception ex)
            {
                // Handle any errors here
                Device.BeginInvokeOnMainThread(async () =>
                {
                    await DisplayAlert("Error", "Failed to get user data.", "OK");
                });
            }
        }
    }
}

