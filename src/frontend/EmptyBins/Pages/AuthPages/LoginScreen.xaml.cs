using Microsoft.Maui.Controls;
using System;

namespace EmptyBins.Pages.AuthPages;
using EmptyBins.Pages.UserPages;

public partial class LoginScreen : ContentPage
{
    public LoginScreen()
    {
        InitializeComponent();
    }


    private async void OnLoginClicked(object sender, EventArgs e)
    {
        // Itt történhetne a bejelentkezési logika validálása
        // Ha a bejelentkezés sikeres:
        //await DisplayAlert("Login", "Login attempt...", "OK");
        await Navigation.PushAsync(new UserHomeScreen());
    }

    private async void OnRegisterLabelClicked(object sender, EventArgs e)
    {
        // Navigálás a regisztrációs képernyőre.
        // Feltételezve, hogy van egy RegisterScreen nevű ContentPage-ed.
        await Navigation.PushAsync(new RegisterScreen());
    }
}
