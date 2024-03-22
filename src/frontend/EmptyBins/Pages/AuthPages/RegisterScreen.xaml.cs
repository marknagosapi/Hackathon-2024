using Microsoft.Maui.Controls;
using System;

namespace EmptyBins.Pages.AuthPages;

public partial class RegisterScreen : ContentPage
{
    public RegisterScreen()
    {
        InitializeComponent();
    }

    private async void OnRegisterClicked(object sender, EventArgs e)
    {
        //logika
        await DisplayAlert("Register", "Registration attempt...", "OK");
    }

    private async void OnLoginLabelClicked(object sender, EventArgs e)
    {
        // navigacio
        await Navigation.PopAsync();
    }

    private void UserButton_Clicked(object sender, EventArgs e)
    {
        userButton.BackgroundColor = Colors.Orange;
        adminButton.BackgroundColor = Colors.Transparent;
        // Itt állítsd be a felhasználó típusát "User"-re
    }

    private void AdminButton_Clicked(object sender, EventArgs e)
    {
        adminButton.BackgroundColor = Colors.IndianRed;
        userButton.BackgroundColor = Colors.Transparent;
        // Itt állítsd be a felhasználó típusát "Admin"-re
    }

}
