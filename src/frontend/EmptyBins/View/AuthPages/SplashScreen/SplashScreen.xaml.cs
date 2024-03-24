using Microsoft.Maui.Controls;
using System.Threading.Tasks;

using EmptyBins.View.AuthPages;


namespace EmptyBins.View
{
    public partial class SplashScreen : ContentPage
    {
        public SplashScreen()
        {
            InitializeComponent();
            NavigateToLogin();
        }


        private async void NavigateToLogin()
        {
            await Task.Delay(3000);
            Application.Current.MainPage = new NavigationPage(new LoginScreen());
        }
    }
}
