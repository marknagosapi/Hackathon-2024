using System;
using ZXing.Net.Maui.Controls;
using Microsoft.Maui.Controls;
using ZXing.Net.Maui;

namespace EmptyBins.View.AdminPages.CameraScreens;

public partial class CameraScreens : ContentPage
{
    public CameraScreens()
    {
        InitializeComponent();
    }

    // Event handler for barcode detection
    private void barcodeReader_BarcodeDetected(object sender, BarcodeDetectionEventArgs e)
    {
        // Assuming you want to handle the first detected barcode
        var firstBarcode = e.Results[0];
        if (firstBarcode != null)
        {
            // Perform your logic with the detected barcode

            Device.BeginInvokeOnMainThread(async () =>
            {
                await DisplayAlert("Barcode Detected", $"Type: {firstBarcode.Format} - Value: {firstBarcode.Value}", "OK");

               

               
            });
        }
    }
}
