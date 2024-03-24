using EmptyBins.View;
using EmptyBins.View.AdminPages.AdminHomeScreens;


namespace EmptyBins
{
    public partial class App : Application
    {
        public App()
        {
            InitializeComponent();

            // Set the start page to LoginScreen wrapped in a NavigationPage for navigation support
            MainPage = new NavigationPage(new SplashScreen());

        }
    }
}
