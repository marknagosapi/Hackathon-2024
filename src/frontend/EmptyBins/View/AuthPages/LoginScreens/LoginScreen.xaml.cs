
using System.Net.Http;
using System.Text;
using System.Text.Json;
using Newtonsoft.Json;

namespace EmptyBins.View.AuthPages;
using EmptyBins.View.UserPages;
using EmptyBins.Models;
using EmptyBins.View.AdminPages.AdminHomeScreens;
using Microsoft.Maui.Storage;




public partial class LoginScreen : ContentPage
{
    private HttpClient _httpClient = new HttpClient();

    public LoginScreen()
    {
        InitializeComponent();
    }

    private async void OnLoginClicked(object sender, EventArgs e)
    {
        // Az adatok összeállítása a kéréshez
        var loginData = $"grant_type=&username={Uri.EscapeDataString(emailEntry.Text)}&password={Uri.EscapeDataString(passwordEntry.Text)}&scope=&client_id=&client_secret=";

        // A StringContent létrehozása 'application/x-www-form-urlencoded' MIME típussal
        var content = new StringContent(loginData, Encoding.UTF8, "application/x-www-form-urlencoded");

        try
        {
            // A POST kérés küldése
            var response = await _httpClient.PostAsync("http://localhost:8000/token", content);

            if (response.IsSuccessStatusCode)
            {
                var responseContent = await response.Content.ReadAsStringAsync();
                var tokenResponse = JsonConvert.DeserializeObject<TokenResponse>(responseContent);

                // Az access token elmentése a SecureStorage-ba
                await SecureStorage.SetAsync("AccessToken", tokenResponse.AccessToken);

                // Navigáció a felhasználó típusa alapján
                if (tokenResponse.UserType == "User")
                {
                    await Navigation.PushAsync(new UserHomeScreen());
                }
                else if (tokenResponse.UserType == "Admin")
                {
                    await Navigation.PushAsync(new AdminHomeScreen());
                }
            }
            else
            {
                // Sikertelen bejelentkezés kezelése
                await DisplayAlert("Login Failed", "Invalid email or password.", "OK");
            }
        }
        catch (Exception ex)
        {
            // Hiba kezelése
            await DisplayAlert("Error", $"An error occurred: {ex.Message}", "OK");
        }
    }




    private async void OnRegisterLabelClicked(object sender, EventArgs e)
    {
        // Navigálás a regisztrációs képernyőre.
        await Navigation.PushAsync(new RegisterScreen());
    }
}