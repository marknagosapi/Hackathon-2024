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
        object data = _selectedUserType == "user" ? new
        {
            first_name = firstnameEntry.Text,
            last_name = lastnameEntry.Text,
            email = emailEntry.Text,
            password = passwordEntry.Text,
            points = 0,
            level_id = 0,
        } : new
        {
            first_name = firstnameEntry.Text,
            last_name = lastnameEntry.Text,
            email = emailEntry.Text,
            market_name = marketNameEntry.Text, // Csak az adminisztrátorokhoz
            password = passwordEntry.Text,
        };


        var url = _selectedUserType == "user" ? "http://localhost:8000/users/add" : "http://localhost:8000/admins/add";
        var content = new StringContent(JsonConvert.SerializeObject(data), Encoding.UTF8, "application/json");

        try
        {
            //http url
            var response = await _httpClient.PostAsync(url, content);

            if (response.IsSuccessStatusCode)
            { 
                await DisplayAlert("Success", "Registration successful.", "OK");

                // UserType alapján döntés
                if (_selectedUserType == "user")
                {
                    await Navigation.PushAsync(new UserHomeScreen());
                }
                else if (_selectedUserType == "admin")
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