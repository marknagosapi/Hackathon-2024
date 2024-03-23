using Microsoft.Maui.Controls;
using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using Newtonsoft.Json;
using EmptyBins.View.UserPages;
using EmptyBins.View.AdminPages.AdminHomeScreens;
using EmptyBins.Models;


namespace EmptyBins.View.AuthPages;

public partial class RegisterScreen : ContentPage
{

    private HttpClient _httpClient = new HttpClient();

    public RegisterScreen()
    {
        InitializeComponent();
    }

    //regisztracios logika
    private async void OnRegisterClicked(object sender, EventArgs e)
    {
        var userData = new
        {
            first_name = firstnameEntry.Text,
            last_name = lastnameEntry.Text,
            email = emailEntry.Text,
            password = passwordEntry.Text,
            points = 0,
            level_id = 0,

        };

        var adminData = new
        {
            first_name = firstnameEntry.Text,
            last_name = lastnameEntry.Text,
            email = emailEntry.Text,
            market_name = marketNameEntry.Text,
            password = passwordEntry.Text,
        };



        var content = new StringContent(JsonConvert.SerializeObject(userData), Encoding.UTF8, "application/json");

        try
        {
            //http url
            var response = await _httpClient.PostAsync("http://localhost:8000/users/add", content);

            if (response.IsSuccessStatusCode)
            {
                var responseContent = await response.Content.ReadAsStringAsync();
                var registrationResponse = JsonConvert.DeserializeObject<RegistrationResponse>(responseContent);

                await DisplayAlert("Success", "Registration successful.", "OK");

                // UserType alapján döntés
                if (registrationResponse.UserType == "user")
                {
                    await Navigation.PushAsync(new UserHomeScreen());
                }
                else if (registrationResponse.UserType == "admin")
                {
                    await Navigation.PushAsync(new AdminHomeScreen());
                }
            }
            else
            {
                // Sikertelen regisztráció
                await DisplayAlert("Registration Failed", "Please try again.", "OK");
            }
        }
        catch (Exception ex)
        {
            // Hiba kezelése
            await DisplayAlert("Error", $"An error occurred: {ex.Message}", "OK");
        }
    }


    private async void OnLoginLabelClicked(object sender, EventArgs e)
    {
        // navigacio
        await Navigation.PopAsync();
    }

    private string _selectedUserType = "user"; // Alapértelmezett érték

    private void UserButton_Clicked(object sender, EventArgs e)
    {
        userButton.BackgroundColor = Colors.Orange;
        adminButton.BackgroundColor = Colors.Transparent;
        _selectedUserType = "user";
        marketNameEntry.IsVisible = false; // Rejtjük el, ha "user" a választás
    }

    private void AdminButton_Clicked(object sender, EventArgs e)
    {
        adminButton.BackgroundColor = Colors.DarkCyan;
        userButton.BackgroundColor = Colors.Transparent;
        _selectedUserType = "admin";
        marketNameEntry.IsVisible = true; // Megjelenítjük, ha "admin" a választás
    }


}