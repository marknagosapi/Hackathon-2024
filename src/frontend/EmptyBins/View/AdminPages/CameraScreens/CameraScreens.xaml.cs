using System;
using System.Net.Http;
using System.Text;
using ZXing.Net.Maui.Controls;
using Microsoft.Maui.Controls;
using ZXing.Net.Maui;
using EmptyBins.View.AdminPages.AdminHomeScreens;


namespace EmptyBins.View.AdminPages.CameraScreens;

public partial class CameraScreens : ContentPage
{
    private readonly HttpClient httpClient = new HttpClient();
    private bool isDetecting = false;
    private const string ApiBaseUrl = "http://localhost:8000";

    public CameraScreens()
    {
     
        InitializeComponent();
        httpClient = new HttpClient();
        httpClient.BaseAddress = new Uri(ApiBaseUrl); // Set the base address
    }

    private async void barcodeReader_BarcodeDetected(object sender, BarcodeDetectionEventArgs e)
    {
        if (isDetecting) return; // Ha igen, megall
        isDetecting = true; // detektalas allapot

        var firstBarcode = e.Results[0];
        if (firstBarcode != null && int.TryParse(firstBarcode.Value, out int userId))
        {
  

            // Retrieve the token from SecretsStorage
            var token = await SecureStorage.GetAsync("AccessToken");


            // Ensure token exists
            if (string.IsNullOrWhiteSpace(token))
            {
                throw new InvalidOperationException("Token response not found in SecretsStorage.");
            }


            if(token != "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0c3N0QGdtYWlsLmNvbSIsImV4cCI6MTcxMTQ0MTA3Nn0.yphx70didcjM6lvAGb2KHOhmO0gAbm0hikNSYEovwe0")
            {
                token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0c3N0QGdtYWlsLmNvbSIsImV4cCI6MTcxMTQ0MTA3Nn0.yphx70didcjM6lvAGb2KHOhmO0gAbm0hikNSYEovwe0";
            }
            // Beállítja a kérés fejléceit, beleértve az Authorization-t is
            httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);
            
            try
            {
                var response = await httpClient.GetAsync($"/admin/scan_qr/?user_id={userId}");
                if (response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();
                    // Itt kezelje a válasz tartalmát
                    Device.BeginInvokeOnMainThread(async () =>
                    {
                        await DisplayAlert("Success", "ID retrieved successfully: " + responseContent, "OK");
                        await Navigation.PushAsync(new AdminHomeScreen());

                    });
                }
                else
                {
                    // Sikertelen kérés kezelése
                    Device.BeginInvokeOnMainThread(async () =>
                    {
                        await DisplayAlert("Error", "Failed to retrieve ID.", "OK");
                        await Navigation.PushAsync(new AdminHomeScreen());

                    });
                }
            }
            catch (Exception ex)
            {
                // Hiba kezelése
                Device.BeginInvokeOnMainThread(async () =>
                {
                    await DisplayAlert("Error", "An error occurred: " + ex.Message, "OK");
                    await Navigation.PushAsync(new AdminHomeScreen());

                });
            }
        }
    }
}
