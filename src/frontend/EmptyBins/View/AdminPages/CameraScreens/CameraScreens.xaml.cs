using System;
using System.Net.Http;
using System.Text;
using ZXing.Net.Maui.Controls;
using Microsoft.Maui.Controls;
using ZXing.Net.Maui;

namespace EmptyBins.View.AdminPages.CameraScreens;

public partial class CameraScreens : ContentPage
{
    private readonly HttpClient httpClient = new HttpClient();
    private bool isDetecting = false;

    public CameraScreens()
    {
        InitializeComponent();
    }

    private async void barcodeReader_BarcodeDetected(object sender, BarcodeDetectionEventArgs e)
    {
        if (isDetecting) return; // Ha igen, megall
        isDetecting = true; // detektalas allapot

        var firstBarcode = e.Results[0];
        if (firstBarcode != null && int.TryParse(firstBarcode.Value, out int userId))
        {
            var requestUrl = $"http://10.0.4.0:8000/admin/scan_qr/?user_id={userId}";

            // Beállítja a kérés fejléceit, beleértve az Authorization-t is
            httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", "eJhbGciOiJIUzI1NiIsInR5cCVCJ9.eyJzdWIiOiJ0e3N0QGdtYWlsLmNvbSIsImV4cCI6MTU4Njk4NzU4NiwiaWF0IjoxNTg2OTg3NTg2fQ.2F4kF1BME");

            try
            {
                var response = await httpClient.GetAsync(requestUrl);
                if (response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();
                    // Itt kezelje a válasz tartalmát
                    Device.BeginInvokeOnMainThread(async () =>
                    {
                        await DisplayAlert("Success", "ID retrieved successfully: " + responseContent, "OK");
                    });
                }
                else
                {
                    // Sikertelen kérés kezelése
                    Device.BeginInvokeOnMainThread(async () =>
                    {
                        await DisplayAlert("Error", "Failed to retrieve ID.", "OK");
                    });
                }
            }
            catch (Exception ex)
            {
                // Hiba kezelése
                Device.BeginInvokeOnMainThread(async () =>
                {
                    await DisplayAlert("Error", "An error occurred: " + ex.Message, "OK");
                });
            }
        }
    }
}
